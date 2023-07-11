import sys
import os
from pathlib import Path
import random
from pandas.core.frame import DataFrame
import chardet
import pandas as pd
from faker import Faker


fake = Faker()


def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as rawdata:
        result = chardet.detect(rawdata.read(10000))
    return result["encoding"]


def overwrite_file(
    file_path: str, data_frame: DataFrame, new_file_name: str = None
) -> str:
    os.remove(file_path)
    if new_file_name:
        directory = os.path.dirname(file_path)
        new_file_path = os.path.join(directory, new_file_name)
    else:
        new_file_path = file_path
    data_frame.to_csv(new_file_path, sep="\t", index=False)

    return new_file_path


def filter(file_path: str, encoding: str, column: str, expected: str) -> DataFrame:
    data_frame = pd.read_csv(file_path, encoding=encoding, sep="\t")
    return data_frame[data_frame[column] == expected]


def generate_user_agent():
    # List of possible platforms
    platforms = [
        "Windows NT 10.0",
        "Macintosh",
        "X11; Linux x86_64",
        "Windows NT 6.1",
        "Windows NT 6.2",
        "Windows NT 6.3",
        "Windows NT 7.0",
        "Windows NT 8.0",
        "Windows NT 9.0",
        "X11; Ubuntu; Linux i686",
        "X11; U; Linux i686",
        "Macintosh; I; Intel Mac OS X 10_6_8",
        "Macintosh; U; Intel Mac OS X 10_6_8",
        "Macintosh; U; Intel Mac OS X 10_7_0",
        "Macintosh; U; Intel Mac OS X 10_7_1",
        "Macintosh; U; Intel Mac OS X 10_7_2",
        "Macintosh; U; Intel Mac OS X 10_7_3",
        "Macintosh; U; Intel Mac OS X 10_7_4",
        "Macintosh; U; Intel Mac OS X 10_7_5",
        "Macintosh; U; Intel Mac OS X 10_7_6",
    ]

    # List of possible OS versions
    os_versions = [
        "10_15_7",
        "10_14_6",
        "10_13_6",
        "10_12_6",
        "10_11_6",
        "10_10_6",
        "10_9_6",
        "10_8_6",
        "10_7_6",
        "10_6_6",
        "10_5_6",
        "10_4_6",
        "10_3_6",
        "10_2_6",
        "10_1_6",
        "10_0_6",
        "9_9_6",
        "9_8_6",
        "9_7_6",
        "9_6_6",
    ]

    # List of possible browser versions
    browser_versions = [
        "537.36",
        "537.35",
        "537.34",
        "537.33",
        "537.32",
        "537.31",
        "537.30",
        "537.29",
        "537.28",
        "537.27",
        "537.26",
        "537.25",
        "537.24",
        "537.23",
        "537.22",
        "537.21",
        "537.20",
        "537.19",
        "537.18",
        "537.17",
    ]

    # List of possible Chrome versions
    chrome_versions = [
        "113.0.0.0",
        "112.0.0.0",
        "111.0.0.0",
        "110.0.0.0",
        "109.0.0.0",
        "108.0.0.0",
        "107.0.0.0",
        "106.0.0.0",
        "105.0.0.0",
        "104.0.0.0",
        "103.0.0.0",
        "102.0.0.0",
        "101.0.0.0",
        "100.0.0.0",
        "99.0.0.0",
        "98.0.0.0",
        "97.0.0.0",
        "96.0.0.0",
        "95.0.0.0",
        "94.0.0.0",
    ]

    platform = random.choice(platforms)
    os_version = random.choice(os_versions)
    browser_version = random.choice(browser_versions)
    name = fake.name()
    chrome_version = random.choice(chrome_versions)

    user_agent = f"Mozilla/5.0 ({platform}; Intel Mac OS X {os_version}) AppleWebKit/{browser_version} (KHTML, {name}) Chrome/{chrome_version} Safari/{browser_version}"
    return user_agent
