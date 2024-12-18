# coding: UTF-8
import os
from time import sleep
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import totp

load_dotenv()
url = os.getenv("GAKUJO_URL")
options = Options()
options.add_argument("--headless")

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)
driver.get(url)
wait = WebDriverWait(driver, 30)

n = 1.2

def getTaskList():
    task_list = []
    # ログイン
    # 日本語選択
    select_element_locale = driver.find_element(By.ID, "selectLocale")
    Select(select_element_locale).select_by_value("ja")
    wait.until(EC.element_to_be_clickable((By.ID, "btnSsoStart"))).click()
    print("ログインページにアクセスしました。")

    # SSO認証
    sleep(n)
    wait.until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys(
        os.getenv("SSO_USERNAME")
    )
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    sleep(n)
    wait.until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys(
        os.getenv("SSO_PASSWORD")
    )
    wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
    print("SSO認証が完了しました。")

    # TOTP
    totp_key = totp.get_totp_token(os.getenv("OTP_SEC_KEY"))
    sleep(n)
    authenticator = wait.until(
        EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
    )
    authenticator.send_keys(totp_key)
    wait.until(
        EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
    ).click()
    sleep(n)
    print("二要素認証が完了しました。")

    wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
    wait.until(EC.element_to_be_clickable((By.NAME, "_eventId_proceed"))).click()
    print("ログインが完了しました。")

    # 学情システム内
    wait.until(
        EC.element_to_be_clickable((By.ID, "templateMediumSizeContentsHref"))
    ).click()
    task_list = wait.until(
        EC.presence_of_element_located((By.ID, "dataTable01"))
    ).find_elements(By.TAG_NAME, "tr")
    print("課題ページにアクセスしました。")
    return task_list


def close():
    driver.quit()
    print("ブラウザを閉じました。")
