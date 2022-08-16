from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from fake_useragent import UserAgent
import random


def get_chromedriver(use_proxy=False):
    ua = UserAgent()
    user_agent = ua.chrome

    width = random.choice(range(1600, 1900, 100))
    height = random.choice(range(800, 1100, 100))

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-extensions")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors-spki-list")

    if use_proxy:
        options.add_argument("--proxy-server=proxy.soax.com:10000")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver
