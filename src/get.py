# coding: UTF-8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import totp

n = 1.5


def getTaskList(URL, SSO_USERNAME, SSO_PASSWORD, OTP_SEC_KEY):
    for _ in range(2):
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

            select_element_locale = driver.find_element(By.ID, "selectLocale")
            Select(select_element_locale).select_by_value("ja")
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
            # # TOTP
            # totp_key = totp.get_totp_token(OTP_SEC_KEY)
            # authenticator = wait.until(
            #     EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC"))
            # )
            # authenticator.send_keys(totp_key)
            # wait.until(
            #     EC.presence_of_element_located((By.ID, "idSubmit_SAOTCC_Continue"))
            # ).click()
            # print("二要素認証が完了しました。")
            wait.until(EC.element_to_be_clickable((By.ID, "idBtn_Back"))).click()
            wait.until(
                EC.element_to_be_clickable((By.NAME, "_eventId_proceed"))
            ).click()
            print("ログインが完了しました。")
            break
        except TimeoutException as te:
            print(te)
            close()
            pass
        except StaleElementReferenceException as se:
            print(se)
            close()
            pass

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
    driver.quit()
    print("ブラウザを閉じました。")
