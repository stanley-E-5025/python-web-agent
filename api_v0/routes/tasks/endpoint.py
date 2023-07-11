from fastapi import APIRouter, HTTPException
from database.operations import create_task, read_task, update_task, delete_task, read_all_tasks
from database.models import Task
from helpers.scrap_client import ScraperClient
import json
from uuid import UUID

router = APIRouter(tags=["task"], prefix="/task")

@router.post("/", response_model=Task)
def create_new_task(task: Task):
    return create_task(task)

@router.get("/{id}", response_model=Task)
def get_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=list[Task])
def get_all_tasks():
    return read_all_tasks()

def update_existing_task(id:UUID, task: Task):
    updated_task = update_task(id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{id}", response_model=Task)
def delete_existing_task(id:UUID):
    deleted_task = delete_task(id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task

@router.post("/execute/{id}")
async def execute_task(id:UUID):
    task = read_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    step =  {
    "title": "Recording 5/9/2023 at 10:14:35 AM",
    "steps": [
        {
            "type": "setViewport",
            "width": 1440,
            "height": 821,
            "deviceScaleFactor": 1,
            "isMobile": False,
            "hasTouch": False,
            "isLandscape": False,
        },
        {
            "type": "navigate",
            "url": "https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
                    "title": "Workbook: Open Data Regulatory Services - Violations",
                }
            ],
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.QFLowerBound > div"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyQuantitativeDateQuickFilter_0"]/div/div[2]/div[1]/div'
                ],
                ["pierce/div.QFLowerBound > div"],
            ],
            "offsetY": 6,
            "offsetX": 18,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["body > span span > span"],
                ["xpath//html/body/span/div[3]/span/span"],
                ["pierce/body > span span > span"],
                ["text/5/9/2023"],
            ],
            "offsetY": 2.5,
            "offsetX": 22.34375,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.QFLowerBound > div"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyQuantitativeDateQuickFilter_0"]/div/div[2]/div[1]/div'
                ],
                ["pierce/div.QFLowerBound > div"],
            ],
            "offsetY": 1,
            "offsetX": 26,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["tr:nth-of-type(1) > td:nth-of-type(2)"],
                ["xpath//html/body/span/div[2]/table/tbody/tr[1]/td[2]"],
                ["pierce/tr:nth-of-type(1) > td:nth-of-type(2)"],
            ],
            "offsetY": 7.5,
            "offsetX": 13,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.tab-textRegion-boundary div:nth-of-type(2)"],
                ['xpath///*[@id="tabZoneId20"]/div/div/div/div[1]/div/span/div[2]'],
                ["pierce/div.tab-textRegion-boundary div:nth-of-type(2)"],
            ],
            "offsetY": 15,
            "offsetX": 93,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#tabZoneId6 div.tabComboBoxNameContainer"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_0"]/div/div[3]/span/div[1]'
                ],
                ["pierce/#tabZoneId6 div.tabComboBoxNameContainer"],
            ],
            "offsetY": 10,
            "offsetX": 74,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "#FI_federated\\.00w687c1maup7s1dd4wh40d7d2b6\\,none\\:Address\\:nk7677579796986060413_6318501153575507500_\\(All\\) input"
                ],
                [
                    'xpath///*[@id="FI_federated.00w687c1maup7s1dd4wh40d7d2b6,none:Address:nk7677579796986060413_6318501153575507500_(All)"]/div[2]/input'
                ],
                [
                    "pierce/#FI_federated\\.00w687c1maup7s1dd4wh40d7d2b6\\,none\\:Address\\:nk7677579796986060413_6318501153575507500_\\(All\\) input"
                ],
            ],
            "offsetY": 2,
            "offsetX": 8,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["button.apply > span.label"],
                [
                    'xpath///*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_0_menu"]/div[3]/button[2]/span[2]'
                ],
                ["pierce/button.apply > span.label"],
                ["text/Apply"],
            ],
            "offsetY": 4,
            "offsetX": 49,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["div.tab-toolbar"],
                ['xpath///*[@id="toolbar-container"]/div[1]'],
                ["pierce/div.tab-toolbar"],
            ],
            "offsetY": 15,
            "offsetX": 653,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["#download-ToolbarButton > span.tabToolbarButtonText"],
                ['xpath///*[@id="download-ToolbarButton"]/span[2]'],
                ["pierce/#download-ToolbarButton > span.tabToolbarButtonText"],
            ],
            "offsetY": 3.25,
            "offsetX": 27.9375,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["aria/Crosstab"],
                ["button:nth-of-type(3)"],
                [
                    'xpath///*[@id="DownloadDialog-Dialog-Body-Id"]/div/fieldset/button[3]'
                ],
                ["pierce/button:nth-of-type(3)"],
            ],
            "offsetY": 5.5,
            "offsetX": 122,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "div.f1lp596a > div > div > div:nth-of-type(2) > div > div > div > div"
                ],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div'
                ],
                [
                    "pierce/div.f1lp596a > div > div > div:nth-of-type(2) > div > div > div > div"
                ],
            ],
            "offsetY": 21,
            "offsetX": 4.5,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["label:nth-of-type(2)"],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[2]/div[2]/div/label[2]'
                ],
                ["pierce/label:nth-of-type(2)"],
            ],
            "offsetY": 5.5,
            "offsetX": 7.5703125,
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                ["aria/Download Crosstab", "aria/Download"],
                [
                    "#export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id button"
                ],
                [
                    'xpath///*[@id="export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id"]/div/div[3]/button'
                ],
                [
                    "pierce/#export-crosstab-options-dialog-Dialog-BodyWrapper-Dialog-Body-Id button"
                ],
            ],
            "offsetY": 8.5,
            "offsetX": 61.40625,
        },
    ],
}
    url = task.url
    type = task.type

    scraper = ScraperClient(url, step, type, task.id)
    results = await scraper.extract_blob()
    return results