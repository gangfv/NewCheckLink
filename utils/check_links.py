import random
import time
from fake_useragent import UserAgent
from urllib.parse import urlparse

from requests.exceptions import SSLError
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from core.google_links import worksheet_errors


def check_link(value):
    donor = value[0]
    acceptor = value[1]
    delay = 10
    ua = UserAgent()
    user_agent = ua.chrome

    width = random.choice(range(1600, 1900, 100))
    height = random.choice(range(800, 1100, 100))

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--ignore-certificate-errors-spki-list")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    def error(values):
        try:
            len_error = len(worksheet_errors.col_values(1))
            worksheet_errors.update_cell(len_error + 1, 1, donor)
            worksheet_errors.update_cell(len_error + 1, 2, acceptor)
            worksheet_errors.update_cell(len_error + 1, 4, values)
        except SSLError:
            time.sleep(60)
            len_error = len(worksheet_errors.col_values(1))
            worksheet_errors.update_cell(len_error + 1, 1, donor)
            worksheet_errors.update_cell(len_error + 1, 2, acceptor)
            worksheet_errors.update_cell(len_error + 1, 4, values)

    try:
        driver.get(donor)

        elems = driver.find_elements(By.XPATH, "//a[@href]")

        links = [urlparse(elem.get_attribute('href')).netloc for elem in elems]
        attrs = [elem.get_attribute('rel') for elem in elems]

        dom_acceptor = urlparse(acceptor).netloc

        try:
            index_link = links.index(dom_acceptor)
            links_attr = [' '.join(x) for x in zip(links, attrs)][index_link]

            content = str(driver.page_source)

            if 'Аccess denied' in content:
                print(f"{donor} {acceptor} Cloudflare")
                error("Cloudflare")

            elif 'Сhecking if the site connection is secure' in content:
                print(f"{donor} {acceptor} Capcha")
                error("Capcha")

            elif '<html><head></head><body></body></html>' in content:
                print(f"{donor} {acceptor} Blank site")
                error("Blank site")

            elif 'Bad Gateway' in content:
                print(f"{donor} {acceptor} Bad Gateway")
                error("Bad Gateway")

            elif not links_attr:
                print(f"{donor} {acceptor} None link")
                error("None link")

            elif len(links_attr.split()) <= 1:
                print(f"{donor} {acceptor} - OK")

            else:
                attr = ' '.join(links_attr.split()[1:])
                print(f"{donor} {acceptor} {attr}")
                error(attr)

            driver.close()
            driver.quit()
        except ValueError:
            print(f"{donor} {acceptor} None link")
            error("None link")

            driver.close()
            driver.quit()

    except WebDriverException:
        print(f"{donor} {acceptor} - Bad Gateway")
        error("Bad Gateway")
        driver.close()
        driver.quit()
