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


def getTeamsTasks(SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY):
    global driver
    options = Options()
    # options.add_argument("--headless")
    n = 1
    webdriver_service = Service(ChromeDriverManager().install())
    for _ in range(5):
        try:
            driver = webdriver.Chrome(service=webdriver_service, options=options)
            wait = setWebDriverWait(10)
            driver.get(URL)
            # SSO認証
            sleep(n)
            wait.until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(
                SSO_USERNAME
            )
            wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            sleep(n)
            wait.until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(
                SSO_PASSWORD
            )
            wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            sleep(n)
            print("SSO認証が完了しました。")
            wait = setWebDriverWait(10)
            sleep(1.5)
            if len(driver.find_elements(By.ID, "idTxtBx_SAOTCC_OTC")) > 0:
                # totpの認証を行う
                totp_key = totp.get_totp_token(OTP_SEC_KEY)
                authenticator = wait.until(
                    EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
                )
                authenticator.send_keys(totp_key)
                wait.until(
                    EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
                ).click()
                print("二要素認証が完了しました。")
            else:
                print("二要素認証はスキップされました。")
            wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
            print("ログイン完了")
            break
        except StaleElementReferenceException as sere:
            print(sere)
            n = n + 0.5
            close()
            pass
        except TimeoutException as te:
            print(te)
            n = n + 0.5
            close()
            pass
        except Exception as e:
            print(e)
            n = n + 0.5
            close()
            pass

    try:
        wait = setWebDriverWait(20)
        sleep(n)
        assignment_menu = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div[3]/div/div/div[1]/div[4]/div/button",
                )
            )
        )
        # 課題ページに遷移
        assignment_menu.click()
        print("課題ページに遷移しました。")
        n = 5
        # TODO: iframeの移動
        sleep(n)
        iframe = driver.find_element(By.XPATH, "/html/body/iframe")
        driver.switch_to.frame(iframe)
        print("iframeに移動しました。")
        # sleep(n)
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div",
                )
            )
        )
        sleep(2)
        task_list = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div/div[1]/main/div[2]/div/div[2]/div"
        )
        task_list = [task.text for task in task_list]
        return task_list
    except StaleElementReferenceException as sere:
        print(sere)


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
