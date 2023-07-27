import sys
import logging
import time
import os
import random
from pathlib import Path
import platform
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from utils.scraping import generate_user_agent

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)

sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class WebDriverFactory:
    def __init__(self, user_agent, download_dir):
        self.user_agent = user_agent
        self.download_dir = download_dir

    def get_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={self.user_agent}")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option(
            "prefs", {"download.default_directory": self.download_dir}
        )

        driver = webdriver.Chrome(options=chrome_options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver


class ScraperClient:
    def __init__(self, url: str, steps: list, case: str, data: str):
        self.url = url
        self.steps = steps
        self.case = case
        self.data = data
        self.bot_detected = False
        self.user_agent = generate_user_agent()
        self.download_dir = self._prepare_download_directory()

    def _prepare_download_directory(self):
        today = datetime.today().strftime("%Y-%m-%d")
        download_dir = f"{root_dir}/downloads/{today}"
        os.makedirs(download_dir, exist_ok=True)
        return download_dir

    def handle_key_event(self, driver, key: str, action: str):
        if action == "keyDown":
            ActionChains(driver).key_down(getattr(Keys, key.upper())).perform()
        elif action == "keyUp":
            ActionChains(driver).key_up(getattr(Keys, key.upper())).perform()

    def wait_for_element(self, driver, selector, by, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                actions = ActionChains(driver)
                actions.pause(1)
                actions.move_to_element(element)
                actions.click()
                actions.perform()
                return element
            except:
                attempt += 1
                time.sleep(3)
                logger.info(
                    f"Attempt {attempt} to find element {selector} failed. Retrying..."
                )
        logger.info(f"Failed to find element {selector} after {retries} attempts.")
        return None

    def handle_captcha(self, driver):
        for i in range(5):
            try:
                captcha_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "px-captcha"))
                )
                ActionChains(driver).click_and_hold(captcha_element).perform()
                time.sleep(random.randint(1, 13))
                ActionChains(driver).release().perform()
            except Exception as e:
                logger.error(
                    "Attempt %s: Could not solve the captcha. Error: %s", i + 1, e
                )
                if i == 4:
                    self.bot_detected = True

    async def extract_blob(self) -> dict:
        driver_factory = WebDriverFactory(self.user_agent, self.download_dir)
        driver = driver_factory.get_driver()
        driver.get(self.url)
        driver.set_window_size(
            self.steps["steps"][0]["width"], self.steps["steps"][0]["height"]
        )

        logger.info(self.steps)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        for step in self.steps["steps"]:
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")
            if soup.find("div", {"class": "px-captcha-container"}):
                logger.info("Captcha detected. Attempting to solve...")
                self.handle_captcha(driver)

            if step["type"] == "click":
                for selector_group in step["selectors"]:
                    for selector in selector_group:
                        if (
                            "aria" not in selector
                            and "text" not in selector
                            and "xpath" not in selector
                        ):
                            by = By.CSS_SELECTOR
                            self.wait_for_element(driver, selector, by=by)
            elif step["type"] == "change":
                for selector_group in step["selectors"]:
                    for selector in selector_group:
                        if (
                            "aria" not in selector
                            and "text" not in selector
                            and "xpath" not in selector
                        ):
                            by = By.CSS_SELECTOR
                            element = self.wait_for_element(driver, selector, by=by)
                            if element:
                                element.clear()
                                element.send_keys(self.data)
            elif step["type"] in ["keyDown", "keyUp"]:
                self.handle_key_event(driver, step["key"], step["type"])
            time.sleep(3)

        driver.quit()

        return self.download_dir