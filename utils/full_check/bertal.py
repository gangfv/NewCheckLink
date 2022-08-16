import random
import time
from multiprocessing import Pool

import numpy
import requests
from bs4 import BeautifulSoup

from core.error import error
from core.google_links import ws_links_preprocessing, worksheet_no_links
from utils.full_check.status_code import value_link


def links_inf(value):
    donor = value[0]
    acceptor = value[1]
    linkbuilder = value[2]

    try:
        r = requests.get(f"https://bertal.ru/index.php?a10396944/{donor}#h")
        soup = BeautifulSoup(r.text, "lxml")
        web = str(soup.find("textarea")).replace('&lt;', '<').replace('&gt;', '>')
        soup = BeautifulSoup(web, "lxml")

        links_acceptor = [link.get('href') for link in soup.find_all('a', href=True)]
        index_link = links_acceptor.index(acceptor)
        attrs_acceptor = [link.get('rel') for link in soup.find_all('a', href=True)]
        for attr in attrs_acceptor:
            if attr in [['nofollow'], ['noindex'], ['sponsored']]:
                print(donor, acceptor, str(attr)[2:-2])
                error(worksheet_no_links, donor, acceptor, linkbuilder, str(attr)[2:-2])
                break
    except ValueError:
        r = requests.get(f"https://bertal.ru/index.php?a10396944/{donor}#h")
        soup = BeautifulSoup(r.text, "lxml")
        web = soup.find("textarea")

        if None == web:
            protocol = donor[:donor.find(":")]
            r = requests.get(f"https://bertal.ru/index.php?a10393863/{donor.replace(protocol, 'http')}#h")
            soup = BeautifulSoup(r.text, "lxml")
            web = soup.find("textarea")

            try:
                status = soup.find("div", id="otv").find_all("b")[-1].text
                value_link(status, donor, acceptor, linkbuilder, web)
            except AttributeError:
                er = soup.find("div", id="er").text[:6]
                if er == "ОШИБКА":
                    print(f"{donor} - Undefined server error")
                    error(worksheet_no_links, donor, acceptor, linkbuilder, 'Undefined server error')

        try:
            status = soup.find("div", id="otv").find_all("b")[-1].text
            value_link(status, donor, acceptor, linkbuilder, web)
        except AttributeError:
            er = soup.find("div", id="er").text[:6]
            if er == "ОШИБКА":
                pass


if __name__ == '__main__':
    np_ws_links_preprocessing = numpy.array(ws_links_preprocessing)
    p = Pool(processes=1)
    p.map(links_inf,
          zip(np_ws_links_preprocessing[1:, 0], np_ws_links_preprocessing[1:, 1], np_ws_links_preprocessing[1:, 2]))
