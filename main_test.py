
from selenium.webdriver.chrome.options import Options
from aws_main import  CaptchaHandler
from enter_data import process_account_creation

import undetected_chromedriver as uc



def main():
    # Настройки Chrome с прокси
    options = Options()

    # Если запускаете на Linux от пользователя, иногда помогает:
    options.add_argument("--no-sandbox")
    options.add_argument('--connection-timeout=60')
    options.add_argument("--lang=en-US,en")  # 👈 Добавьте эту строку
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless=new")  # новый headless
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={custom_user_agent}')
    driver = uc.Chrome(version_main=145, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(30)
    driver.get("https://aws.amazon.com")
    process_account_creation(driver)
    captcha_manager = CaptchaHandler(driver, api_key="2captchaAPIKEY")
    captcha_manager.solve_security_check(single_run=False)
    input("Enter to continue...")




if __name__ == "__main__":
    main()