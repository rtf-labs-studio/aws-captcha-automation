import os
import time
import requests
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from twocaptcha import TwoCaptcha


class CaptchaHandler:
    def __init__(self, driver, api_key, temp_image_path="captcha_temp.png"):
        self.driver = driver
        self.solver = TwoCaptcha(api_key)
        self.temp_image_path = temp_image_path
        self.wait = WebDriverWait(self.driver, 15)

    def _get_captcha_image(self, img_url):
        """Скачивание изображения капчи через requests."""
        try:
            headers = {"User-Agent": self.driver.execute_script("return navigator.userAgent;")}
            response = requests.get(img_url, headers=headers, timeout=10)
            if response.status_code == 200:
                with open(self.temp_image_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to download captcha image: {e}")
            return False

    def solve_security_check(self, single_run=True):
        """
        The main loop for monitoring and solving captchas.
        :param single_run: If True, performs one run and exits.
        """
        logger.info("Starting Security Check Monitor...")

        while True:
            try:
                # Поиск заголовка проверки
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Security Verification')]")
                visible_elements = [el for el in elements if el.is_displayed()]

                if not visible_elements:
                    logger.info("No captcha detected on the screen.")
                    if single_run: break
                    time.sleep(10)
                    continue

                logger.warning("Security review detected! Attempting to solve...")
                target = visible_elements[0]

                # Поиск контейнера и переключение во фрейм
                container = target.find_element(By.XPATH, "./ancestor::div[contains(@class, 'awsui_container')][1]")
                iframe = container.find_element(By.XPATH, ".//iframe")
                self.driver.switch_to.frame(iframe)

                try:
                    # Ожидание появления изображения
                    captcha_img = self.wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='captcha']")))
                    img_url = self.wait.until(lambda d: captcha_img.get_attribute("src"))

                    if not img_url or "http" not in img_url:
                        logger.error("Invalid captcha URL.")
                        continue

                    # Скачивание и решение
                    if self._get_captcha_image(img_url):
                        logger.info("Solving captcha via 2Captcha...")
                        result = self.solver.normal(self.temp_image_path)
                        captcha_text = result['code']
                        logger.success(f"Captcha solved: {captcha_text}")

                        # Ввод данных
                        input_field = self.driver.find_element(By.NAME, "captchaGuess")
                        input_field.clear()
                        input_field.send_keys(captcha_text)

                        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                        submit_btn.click()

                        logger.info("Form submitted. Waiting for redirection...")
                        time.sleep(2)  # Даем время на обработку

                except TimeoutException:
                    logger.error("Timed out waiting for captcha elements inside iframe.")
                except Exception as e:
                    logger.error(f"Error during solving process: {e}")
                finally:
                    # Всегда возвращаемся из iframe
                    self.driver.switch_to.default_content()
                    if os.path.exists(self.temp_image_path):
                        os.remove(self.temp_image_path)

            except (NoSuchElementException, StaleElementReferenceException):
                logger.debug("Elements changed during detection, retrying...")

            if single_run:
                break
            time.sleep(5)