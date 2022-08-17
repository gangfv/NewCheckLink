import re
from urllib.parse import urlparse

from core.error import error
from core.google_links import worksheet_no_links, worksheet_anti_bot


def value_link(status, url, acceptor, linkbuilder, web):
    if re.search("200", status):

        dom_acceptor = urlparse(acceptor).netloc

        if dom_acceptor[:4] == "www.":
            search_link = re.search(dom_acceptor[4:], web.decode())
        else:
            search_link = re.search(dom_acceptor, web.decode())

        if search_link:
            print(f"{url} {acceptor} - ОК")
        else:
            print(f"{url} {acceptor} - No Link")
            error(worksheet_no_links, url, acceptor, linkbuilder, "No link")

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
