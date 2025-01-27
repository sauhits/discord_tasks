# coding: UTF-8
from time import sleep
import totp, os
import json
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    NoSuchElementException,
)
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
XPATH_AUTHCODE = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div[3]/div/input"
XPATH_AUTHCODE_ENTER = "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[6]/div/div/div/div/input"
XPATH_LAST_ENTER = "/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input"


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
            # SSO_USERNAMEの入力
            if len(driver.find_elements(By.XPATH, XPATH_SSO_USERNAME)) > 0 and check == False:
                print("SSO_USERNAMEの入力")
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_SSO_USERNAME))
                ).send_keys(SSO_USERNAME)
                check = True
            # SSO_PASSWORDの入力
            elif len(driver.find_elements(By.XPATH, XPATH_SSO_PASSWORD)) > 0 and check==False:
                print("SSO_PASSWORDの入力")
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_SSO_PASSWORD))
                ).send_keys(SSO_PASSWORD)
                check = True
            # SSO_USERNAMEのENTER
            elif (
                len(driver.find_elements(By.XPATH, XPATH_SSO_NAME_ENTER)) > 0 and check
            ):
                print("SSO_USERNAMEのENTER")
                check = False
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_SSO_NAME_ENTER))
                ).click()
                sleep(0.5)
            # SSO_PASSWORDのENTER
            elif (
                len(driver.find_elements(By.XPATH, XPATH_SSO_PASS_ENTER)) > 0 and check
            ):
                print("SSO_PASSWORDのENTER")
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_SSO_PASS_ENTER))
                ).click()
            # TOTP
            elif len(driver.find_elements(By.XPATH, XPATH_AUTHCODE)) > 0:
                print("TOTPの入力")
                # totpの認証を行う
                totp_key = totp.get_totp_token(OTP_SEC_KEY)
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_AUTHCODE))
                ).send_keys(totp_key)
                wait.until(
                    EC.presence_of_element_located((By.XPATH, XPATH_AUTHCODE_ENTER))
                ).click()
                sleep(1)
                if len(driver.find_elements(By.XPATH, XPATH_AUTHCODE)) > 0:
                    close()
                    continue
            # 認証全体の完了
            elif len(driver.find_elements(By.XPATH, XPATH_LAST_ENTER)) > 0 and check:
                wait.until(
                    EC.element_to_be_clickable((By.XPATH, XPATH_LAST_ENTER))
                ).click()
                print("ログイン完了")
                break
            else:
                continue
        except StaleElementReferenceException as sere:
            print(sere.msg)
            continue
        except ElementNotInteractableException as enie:
            print(enie.msg)
            continue
        except TimeoutException as te:
            print(te.msg)
            close()
            continue
    wait = setWebDriverWait(10)
    for _ in range(5):
        print("トライ", _, "回目")
        try:
            wait.until(EC.presence_of_all_elements_located)
            print("ロード完了")
            # 課題ページのクリック
            wait.until(
                EC.element_to_be_clickable((By.XPATH, XPATH_ASSIGNMENT_PAGE))
            ).click()
            print("課題ページに遷移しました。")
            # iframeの移動
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[7]/div/div/div/div/div/iframe")))
            iframe = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[7]/div/div/div/div/div/iframe")
            driver.switch_to.frame(iframe)
            print("iframeに移動しました。")
            # 課題の取得
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div",
                    )
                )
            )
            task_list = driver.find_elements(
                By.XPATH, "/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div"
            )
            print("課題の取得完了")
            task_list = [task.text for task in task_list]
            if task_list is None:
                continue
            return task_list
        except StaleElementReferenceException as sere:
            print(sere.msg)
            continue
        except ElementNotInteractableException as enie:
            print(enie.msg)
            continue
        except NoSuchElementException as nsee:
            print(nsee.msg)
            continue
        except TimeoutException as te:
            print(te.msg)
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


def close():
    driver.quit()
    print("ブラウザを閉じました。")


def setWebDriverWait(time=10):
    wait = WebDriverWait(driver, time)
    return wait


getTeamsTasks(
    os.getenv("SSO_USERNAME"), os.getenv("SSO_PASSWORD"), os.getenv("OTP_SEC_KEY")
)
