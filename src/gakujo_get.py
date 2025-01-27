# coding: UTF-8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import totp, os
from time import sleep
from dotenv import load_dotenv

def getTaskList(URL, SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY):
    for _ in range(3):
        task_list = []
        global gakujo_driver
        # options.add_argument("--headless")
        # ログイン
        try:
            webdriver_service = Service(ChromeDriverManager().install())
            options = Options()
            gakujo_driver = webdriver.Chrome(service=webdriver_service, options=options)
            wait = setWebDriverWait(10)
            gakujo_driver.get(URL)

            # select_element_locale = gakujo_driver.find_element(By.ID, "selectLocale")
            # Select(select_element_locale).select_by_value("ja")
            wait.until(EC.element_to_be_clickable((By.ID, "btnSsoStart"))).click()
            print("ログインページにアクセスしました。")
            # SSO認証
            wait.until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(
                SSO_USERNAME
            )
            wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            wait.until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(
                SSO_PASSWORD
            )
            wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            print("SSO認証が完了しました。")
            # TOTP

            while True:
                if len(gakujo_driver.find_elements(By.ID, "idTxtBx_SAOTCC_OTC")) > 0:
                    break
                elif len(gakujo_driver.find_elements(By.ID, "idBtn_Back")) > 0:
                    break
                else:
                    sleep(0.5)
                    wait.until(EC.presence_of_all_elements_located)
            if len(gakujo_driver.find_elements(By.ID, "idTxtBx_SAOTCC_OTC")) > 0:
                # totpの認証を行う
                totp_key = totp.get_totp_token(OTP_SEC_KEY)
                wait.until(
                    EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
                ).send_keys(totp_key)
                wait.until(
                    EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
                ).click()
                print("二要素認証が完了しました。")
            else:
                print("二要素認証はスキップされました。")
            wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
            wait.until(
                EC.element_to_be_clickable((By.NAME, "_eventId_proceed"))
            ).click()
            print("ログインが完了しました。")
            break
        except TimeoutException as te:
            print(te.msg)
            close()
            continue
        except StaleElementReferenceException as se:
            print(se.msg)
            close()
            continue
        except ElementNotInteractableException as en:
            print(en.msg)
            close()
            continue

    # 学情システム内
    wait.until(
        EC.element_to_be_clickable((By.ID, "templateMediumSizeContentsHref"))
    ).click()

    # オプション選択
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SC_14002B00_01_SearchConditionForm']/div[1]/ul/li/div/div[2]/div/ul/li[1]/label"))).click()
    # print("課題区分を選択しました。")

    # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SC_14002B00_01_SearchConditionForm']/div[1]/ul/li/div/div[2]/div/a"))).click()
    # print("詳細選択を開きました。")
    # sleep(n)
    # year_select=driver.find_element(By.XPATH, "//*[@id='changeStartYearCmb']")
    # Select(year_select).select_by_value("2024")
    # print("2024年度を選択しました。")
    #
    # semester_select=driver.find_element(By.ID, "changeStartSemesterCmb")
    # Select(semester_select).select_by_value("2")
    # print("後期を選択しました。")

    # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SC_14002B00_01_SearchConditionForm']/div[2]/button"))).click()
    # 課題取得
    task_list = wait.until(
        EC.presence_of_element_located((By.ID, "dataTable01"))
    ).find_elements(By.TAG_NAME, "tr")
    print("課題ページにアクセスしました。")

    return task_list


def close():
    gakujo_driver.quit()
    print("ブラウザを閉じました。")


def setWebDriverWait(time=10):
    wait = WebDriverWait(gakujo_driver, time)
    return wait


# load_dotenv()
# getTaskList(
#     os.environ.get("GAKUJO_URL"),
#     os.environ.get("SSO_USERNAME"),
#     os.environ.get("SSO_PASSWORD"),
#     os.environ.get("OTP_SEC_KEY"),
# )
