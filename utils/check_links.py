import random

from fake_useragent import UserAgent
from urllib.parse import urlparse

from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from core.google_links import worksheet_errors


def check_link(value):
    donor = value[0]
    print(donor)
    acceptor = value[1]

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
    try:
        driver.get(donor)

        elems = driver.find_elements(By.XPATH, "//a[@href]")

        links = [urlparse(elem.get_attribute('href')).netloc for elem in elems]
        attrs = [elem.get_attribute('rel') for elem in elems]

        dom_acceptor = urlparse(acceptor).netloc
        links_attr = [' '.join(x) for x in zip(links, attrs)][links.index(dom_acceptor)]

        content = str(driver.page_source)

        if 'Access denied' in content:
            print(f"{donor} {acceptor} Cloudflare")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, "Cloudflare")

        elif 'Checking if the site connection is secure' in content:
            print(f"{donor} {acceptor} Capcha")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, "Capcha")

        elif '<html><head></head><body></body></html>' in content:
            print(f"{donor} {acceptor} Blank site")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, "Blank site")

        elif 'Bad Gateway' in content:
            print(f"{donor} {acceptor} Bad Gateway")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, "Bad Gateway")

        elif not links_attr:
            print(f"{donor} {acceptor} None link")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, f"None link")

        elif len(links_attr.split()) <= 1:
            print(f"{donor} {acceptor} - OK")

        else:
            attr = ' '.join(links_attr.split()[1:])
            print(f"{donor} {acceptor} {attr}")
            len_error = len(worksheet_errors.col_values(1))

            worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
            worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
            worksheet_errors.update_cell(len_error + 1, 4, f"{attr}")

        driver.close()
        driver.quit()
    except WebDriverException:
        print(f"{donor} {acceptor} - Bad Gateway")
        len_error = len(worksheet_errors.col_values(1))

        worksheet_errors.update_cell(len_error + 1, 1, f"{donor}")
        worksheet_errors.update_cell(len_error + 1, 2, f"{acceptor}")
        worksheet_errors.update_cell(len_error + 1, 4, "Bad Gateway")
        driver.close()
        driver.quit()
