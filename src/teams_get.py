# coding: UTF-8
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://teams.microsoft.com/v2/"


def getTeamsTasks():
    task_list = []
    global driver
    options = Options()
    # options.add_argument("--headless")
    # ログイン
    try:
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=options)
        wait = WebDriverWait(driver, 15)
        driver.get(URL)
        sleep(5)
    except TimeoutException as te:
        print(te)


getTeamsTasks()
