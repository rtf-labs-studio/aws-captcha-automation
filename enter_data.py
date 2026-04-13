from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def process_account_creation(driver):
    """
    Функция принимает Selenium драйвер, создаёт аккаунт и переключается на нужную вкладку

    Args:
        driver: Selenium WebDriver instance
    """
    try:
        # 1. Ожидаем элемент и кликаем на него
        create_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='create-account-button']"))
        )
        create_button.click()

        # Небольшая задержка для открытия новой вкладки
        time.sleep(5)

        # 2. Получаем количество открытых вкладок и переключаемся на предпоследнюю
        window_handles = driver.window_handles
        tabs_count = len(window_handles)
        print(f"Открыто вкладок: {tabs_count}")

        # Переключаемся на последнюю вкладку - 1 (предпоследнюю)
        if tabs_count >= 2:
            driver.switch_to.window(window_handles[-1])
            print("Переключились на предпоследнюю вкладку")
        else:
            print("Предпоследней вкладки нет, остаёмся на текущей")

        # 3. Работа с полем email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='emailAddress']"))
        )
        email_input.clear()
        email_input.send_keys("test55555@gmail.com")

        # 4. Работа с полем accountName
        account_input = driver.find_element(By.XPATH, "//input[@name='accountName']")
        account_input.clear()
        account_input.send_keys("profile55555")

        # 5. Нажатие на кнопку submit
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        print("Аккаунт успешно создан!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")