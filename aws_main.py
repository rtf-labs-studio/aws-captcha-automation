from selenium.webdriver.support.wait import WebDriverWait
import os
import time
import requests
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from loguru import logger

def monitor_and_solve_security(driver, API_KEY, sear_captha = True):

    logger.info("Launching Security Check...")
    solver = TwoCaptcha(API_KEY)
    time.sleep(10)
    while True:
        try:
            # 1. Поиск всех элементов с текстом
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Security Verification')]")

            # 2. Фильтруем только те, что видны на экране
            visible_elements = [el for el in elements if el.is_displayed()]

            if visible_elements:
                logger.warning("External active security review.")
                target = visible_elements[0]

                # 3. Находим контейнер и iframe
                container = target.find_element(By.XPATH, "./ancestor::div[contains(@class, 'awsui_container')][1]")
                iframe = container.find_element(By.XPATH, ".//iframe")

                # 4. Заходим в контекст iframe
                driver.switch_to.frame(iframe)

                try:
                    # 5. Ждем, пока у картинки появится атрибут src, который начинается на 'http' или 'data'
                    # (иногда капчи передаются в base64 через data:image/png...)
                    wait = WebDriverWait(driver, 10)
                    captcha_img = wait.until(lambda d: d.find_element(By.XPATH, "//img[@alt='captcha']"))

                    # Ждем, пока src перестанет быть None или пустой строкой
                    img_url = wait.until(lambda d: captcha_img.get_attribute("src") or False)

                    if not img_url or img_url == 'None':
                        logger.info("Captcha URLs are still empty, skipping iteration...")
                        continue

                    img_path = "captcha_temp.png"

                    # Скачиваем с обработкой сессии (чтобы не было 403 ошибки)
                    headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}
                    response = requests.get(img_url, headers=headers, timeout=10)

                    with open(img_path, 'wb') as f:
                        f.write(response.content)

                    # 6. Решаем через библиотеку 2captcha
                    logger.info("Solving the captcha......")
                    try:
                        result = solver.normal(img_path)
                        captcha_text = result['code']  # Получаем текст капчи
                        logger.success(f"The captcha was solved successfully: {captcha_text}")

                        # 7. Ввод ответа и нажатие кнопки
                        input_field = driver.find_element(By.XPATH, "//input[@name='captchaGuess']")
                        input_field.clear()
                        input_field.send_keys(captcha_text)

                        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
                        submit_btn.click()

                        logger.info("The form has been submitted. Exiting the loop.")

                        if os.path.exists(img_path):
                            os.remove(img_path)

                        # Если все прошло успешно — возвращаемся и выходим из цикла
                        driver.switch_to.default_content()


                    except Exception as e:
                        logger.error(f"Error")
                        # В случае ошибки API пробуем еще раз на следующей итерации

                except NoSuchElementException:
                    logger.error("Waiting for elements inside iframe to show...")
                finally:
                    # Важно: всегда выходим из iframe, даже если упали с ошибкой
                    driver.switch_to.default_content()

        except (NoSuchElementException, StaleElementReferenceException):
            # Пропускаем, если элементы DOM изменились в процессе поиска
            pass
        logger.info(f"There is no captcha on the screen")
        time.sleep(10)
        if sear_captha:
            break
