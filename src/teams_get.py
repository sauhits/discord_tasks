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
standby_url = "https://teams.microsoft.com/l/meetup-join/19%3ameeting_Zjg3NjJiNDYtYjM0NC00OTYwLTk0MTItMDg3ZGI2Zjc0NGFj%40thread.v2/0?context=%7b%22Tid%22%3a%22e0d7dc00-4621-4fe0-90b1-df7b1b40b351%22%2c%22Oid%22%3a%2265647787-084e-4088-9b52-f9c758e5af0a%22%7d"
URL = "https://teams.microsoft.com/"
cookies_file = "cookies_teams.json"
tmp = "html.txt"
tmp1 = "tmp1.json"
teams_shot = "teams_shot.png"
SSO_USERNAME = os.environ.get("SSO_USERNAME")
SSO_PASSWORD = os.environ.get("SSO_PASSWORD")
OTP_SEC_KEY = os.environ.get("OTP_SEC_KEY")


def getTeamsTasks():
    global driver
    options = Options()
    # options.add_argument("--headless")
    n = 0.5
    try:
        webdriver_service = Service(ChromeDriverManager().install())
        for _ in range(5):
            try:
                n = n * 2
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
                # # TOTP
                # totp_key = totp.get_totp_token(OTP_SEC_KEY)
                # authenticator = wait.until(
                #     EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
                # )
                # authenticator.send_keys(totp_key)
                # wait.until(
                #     EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
                # ).click()
                sleep(n)
                print("二要素認証が完了しました。")
                wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
                print("ログイン完了")
                break
            except StaleElementReferenceException as sere:
                print(sere)
                n = n + 1
                close()
                pass
            except TimeoutException as te:
                print(te)
                n = n + 1
                close()
                pass
            except Exception as e:
                print(e)
                n = n + 1
                close()
                pass

        try:
            wait = setWebDriverWait(20)
            sleep(n)
            assignment_menu = wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "66aeee93-507d-479a-a3ef-8f494af43945")
                )
            )
            print("cookie取得開始")
            cookies = driver.get_cookies()
            saveCookies(cookies_file, cookies)
            # 課題ページに遷移
            assignment_menu.click()
            print("課題ページに遷移しました。")
            sleep(10)
            # TODO: iframeの移動
            wait.until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.ID, "cacheable-iframe:66aeee93-507d-479a-a3ef-8f494af43945")
                )
            )

            with open(tmp, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("htmlを取得しました。")
            driver.save_screenshot(teams_shot)
            driver.switch_to.default_content()

        except StaleElementReferenceException as sere:
            print(sere)

    finally:
        driver.quit()


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


getTeamsTasks()
