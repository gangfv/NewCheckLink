import re
from urllib.parse import urlparse

from core.error import error
from core.google_links import worksheet_no_links, worksheet_anti_bot


def value_link(soup, url, acceptor, linkbuilder, web):
    status = soup.find("div", id="otv").find_all("b")[-1].text
    if re.search("200", status):

        dom_acceptor = urlparse(acceptor).netloc
        search_link = re.search(dom_acceptor, web.decode())

        if search_link:
            print(f"{url} {acceptor} - ОК")
        else:
            print(f"{url} {acceptor} - None Link")
            error(worksheet_no_links, url, acceptor, linkbuilder, "None link")

    elif re.search("400", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("403", status):
        print(f"{url} - {status}")
        error(worksheet_anti_bot, url, acceptor, linkbuilder, status)

    elif re.search("404", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("408", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("500", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("502", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("503", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("504", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    elif re.search("505", status):
        print(f"{url} - {status}")
        error(worksheet_no_links, url, acceptor, linkbuilder, status)

    return status
