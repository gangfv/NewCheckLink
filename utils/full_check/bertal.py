import random
import time
from multiprocessing import Pool

import numpy
import requests
from bs4 import BeautifulSoup

from core.google_links import ws_no_links
from utils.full_check.status_code import value_link


def links_inf(value):
    donor = value[0]
    acceptor = value[1]
    linkbuilder = value[2]

    time.sleep(random.choice(range(4, 8, 1)))
    r = requests.get(f"https://bertal.ru/index.php?a10393863/{donor}#h")
    soup = BeautifulSoup(r.text, "lxml")
    web = soup.find("textarea")

    if None == web:
        protocol = donor[:donor.find(":")]
        r = requests.get(f"https://bertal.ru/index.php?a10393863/{donor.replace(protocol, 'http')}#h")
        soup = BeautifulSoup(r.text, "lxml")
        web = soup.find("textarea")
        value_link(soup, donor, acceptor, linkbuilder, web)

    value_link(soup, donor, acceptor, linkbuilder, web)


if __name__ == '__main__':
    np_ws_no_links = numpy.array(ws_no_links)
    p = Pool(processes=1)
    p.map(links_inf, zip(np_ws_no_links[1:, 0], np_ws_no_links[1:, 1], np_ws_no_links[1:, 2]))
