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
url = "https://gakujo.shizuoka.ac.jp/lcu-web/"
options = Options()
# options.add_argument("--headless")

webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)
driver.get(url)
wait = WebDriverWait(driver, 20)

# ログイン
# 日本語選択
select_element_locale = driver.find_element(By.ID, "selectLocale")
select = Select(select_element_locale)
select.select_by_value("ja")

# ログイン
login_button = driver.find_element(By.ID, "btnSsoStart")
login_button.click()

# SSO認証
SSO_username = wait.until(EC.presence_of_element_located((By.ID, "i0116")))

SSO_username.send_keys(os.getenv("SSO_USERNAME"))
to_password_page = driver.find_element(By.ID, "idSIButton9")
to_password_page.click()


SSO_password = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
SSO_password.send_keys(os.getenv("SSO_PASSWORD"))

sleep(1)
login_button = driver.find_element(By.ID, "idSIButton9")
login_button.click()

# 二要素認証
sign_in_another_way_link = wait.until(
    EC.element_to_be_clickable((By.ID, "signInAnotherWay"))
)
sign_in_another_way_link.click()
verification_code_element = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//div[@data-bind='text: display' and text()='Use a verification code']",
        )
    )
)
verification_code_element.click()

# TOTP
authenticator=wait.until(EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC")))
totp_key=totp.get_totp_token(os.getenv("OTP_SEC_KEY"))
authenticator.send_keys(totp_key)
check_key=wait.until(EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue")))
check_key.click()

sleep(1)
continue_button = wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back")))
continue_button.click()

proceed_button = wait.until(EC.element_to_be_clickable((By.NAME, "_eventId_proceed")))
proceed_button.click()

sleep(10000)
# Quit the driver
driver.quit()