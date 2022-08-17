from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from core.settings import get_chromedriver
from core.error import error

from selenium.common import (
    WebDriverException,
    TimeoutException,
    SessionNotCreatedException,
    NoSuchElementException
)

from core.google_links import (
    worksheet_no_links,
    worksheet_no_proxy_preprocessing
)


def preprocessing_check_link(value):
    donor = value[0]
    acceptor = value[1]
    linkbuilder = value[2]
    try:
        driver = get_chromedriver(use_proxy=False)

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
                title = str(driver.title)

                if 'Страница не доступна' in title:
                    print(f"{donor} {acceptor} None link")
                    error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "None link")

                elif 'Page not available' in title:
                    print(f"{donor} {acceptor} None link")
                    error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "None link")

                elif '<html><head></head><body></body></html>' in content:
                    print(f"{donor} {acceptor} Blank site")
                    error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "Blank site")

                elif "www.cloudflare" in links:
                    print(f"{donor} {acceptor} None link")
                    error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "Cloudflare")

                elif not links_attr:
                    print(f"{donor} {acceptor} None link")
                    error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "None link")

                elif len(links_attr.split()) <= 1:
                    print(f"{donor} {acceptor} - OK")

                else:
                    attrs = ' '.join(links_attr.split()[1:]).split(' ')
                    for attr in attrs:
                        if attr in ['nofollow', 'noindex', 'sponsored']:
                            print(f"{donor} {acceptor} {attr}")
                            error(worksheet_no_links, donor, acceptor, linkbuilder, f"{attr}")

                driver.close()
                driver.quit()

            except ValueError:

                if acceptor.startswith('http'):
                    link = acceptor.split('//')[1]
                    if link.startswith('www'):
                        link = link[4:]
                    elif link.endswith('/'):
                        link = link[:-1]
                elif acceptor.startswith('www'):
                    link = acceptor[4:]
                    if link.endswith('/'):
                        link = link[:-1]
                elif acceptor.endswith('/'):
                    link = acceptor[:-1]
                else:
                    link = acceptor

                tpl_link_list = ['_', '_/', 'www._', 'www._/', 'http://www._',
                                 'http://www._/', 'https://www._', 'https://www._/',
                                 'http://_', 'http://_/', 'https://_', 'https://_/']
                tpl_link_list = [i.replace("_", link) for i in tpl_link_list]

                for link in tpl_link_list:
                    try:
                        driver.find_element("xpath", f"//a[@href='{link}']")
                        print(f"{donor} {acceptor} - OK")
                        break
                    except NoSuchElementException:
                        if "www.cloudflare.com" in links:
                            print(f"{donor} {acceptor} Cloudflare")
                            error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "Cloudflare")
                            break
                        print(f"{donor} {acceptor} None link")
                        error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "None link")
                        break

                driver.close()
                driver.quit()

        except TimeoutException:
            print(f"{donor} {acceptor} - Timeout")
            error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "Timeout")
            driver.close()
            driver.quit()
        except SessionNotCreatedException:
            print(f"{donor} {acceptor} - Failed to create a new session")
            error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "Failed to create a new session")
            driver.close()
            driver.quit()
        except WebDriverException:
            print(f"{donor} {acceptor} None link")
            error(worksheet_no_proxy_preprocessing, donor, acceptor, linkbuilder, "None link")
            driver.close()
            driver.quit()
    except:
        pass
