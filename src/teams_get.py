# coding: UTF-8
from time import sleep
import os
import totp
import json
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
URL = "https://teams.microsoft.com/"
cookies_file = "cookies_teams.json"

XPATH_SSO_USERNAME = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]"
XPATH_SSO_PASSWORD = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input"
XPATH_SSO_NAME_ENTER = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div/input"
XPATH_SSO_PASS_ENTER = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[5]/div/div/div/div/input"

XPATH_ASSIGNMENT_PAGE = (
    "/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/div[4]/div/button"
)
XPATH_TEAMS_IFRAME = "/html/body/iframe"
XPATH_TEAMS_ASSIGNMENT = "/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div"


def getTeamsTasks(SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY):
    global driver
    driver = None
    options = Options()
    # options.add_argument("--headless")
    webdriver_service = Service(ChromeDriverManager().install())
    check = False
    while True:
        if driver is None:
            driver = webdriver.Chrome(service=webdriver_service, options=options)
            wait = setWebDriverWait(10)
            driver.get(URL)
        try:
            wait.until(EC.presence_of_all_elements_located)
            # SSO_USERNAMEのENTER
            if len(driver.find_elements(By.XPATH, XPATH_SSO_NAME_ENTER)) > 0 and check:
                check = False
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_SSO_NAME_ENTER))
                ).click()
                sleep(0.5)
            # SSO_PASSWORDのENTER
            elif (
                len(driver.find_elements(By.XPATH, XPATH_SSO_PASS_ENTER)) > 0 and check
            ):
                check = False
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_SSO_PASS_ENTER))
                ).click()
            # SSO_USERNAMEの入力
            elif len(driver.find_elements(By.XPATH, XPATH_SSO_USERNAME)) > 0:
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_SSO_USERNAME))
                ).send_keys(SSO_USERNAME)
                check = True
            # SSO_PASSWORDの入力
            elif len(driver.find_elements(By.XPATH, XPATH_SSO_PASSWORD)) > 0:
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_SSO_PASSWORD))
                ).send_keys(SSO_PASSWORD)
                check = True
            # TOTP
            elif len(driver.find_elements(By.ID, "idTxtBx_SAOTCC_OTC")) > 0:
                # totpの認証を行う
                totp_key = totp.get_totp_token(OTP_SEC_KEY)
                wait.until(
                    EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
                ).send_keys(totp_key)
                wait.until(
                    EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
                ).click()
            # 認証全体の完了
            elif len(driver.find_elements(By.ID, "idBtn_Back")) > 0:
                wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
                print("ログイン完了")
                break
            else:
                continue
        except StaleElementReferenceException as sere:
            print(sere)
            continue
        except TimeoutException as te:
            print(te)
            close()
            continue
    sleep(1000)
    wait = setWebDriverWait(20)
    for _ in range(5):
        try:
            wait.until(EC.presence_of_all_elements_located)
            # 課題ページのクリック
            wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_ASSIGNMENT_PAGE))
            ).click()
            wait.until(EC.presence_of_all_elements_located)
            # iframeの移動
            iframe = driver.find_element(By.XPATH, XPATH_TEAMS_IFRAME)
            driver.switch_to.frame(iframe)
            # 課題の取得
            wait.until(
                EC.presence_of_element_located((By.XPATH, XPATH_TEAMS_ASSIGNMENT))
            )
            task_list = driver.find_elements(By.XPATH, XPATH_TEAMS_ASSIGNMENT)
            task_list = [task.text for task in task_list]
            return task_list
        except StaleElementReferenceException as sere:
            print(sere)
            continue
        except TimeoutException as te:
            print(te)
            continue


def addCookies(driver, cookies, print_flag=False):
    if print_flag:
        for cookie in cookies:
            driver.add_cookie(cookie)
            print(cookie)
        return
    else:
        for cookie in cookies:
            driver.add_cookie(cookie)
        return


def readCookies(file_name: str):
    try:
        with open(file_name, "r") as input:
            cookies = json.load(input)
    except Exception as e:
        print(e)
        cookies = []
    print("cookie read from json")
    return cookies


def saveCookies(file_name: str, cookies):
    try:
        with open(file_name, "w", newline="") as output:
            json.dump(cookies, output)
    except Exception as e:
        print(e)
    print("cookie saved to json")


def close():
    driver.quit()
    print("ブラウザを閉じました。")


def setWebDriverWait(time=10):
    wait = WebDriverWait(driver, time)
    return wait
