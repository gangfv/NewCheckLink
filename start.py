import time

import numpy as numpy
from multiprocessing import Pool
from utils.full_check.bertal import links_inf
from utils.no_proxy_preprocessing import preprocessing_check_link
from core.google_links import (
    ws_links,
    worksheet_no_links,
    worksheet_no_proxy_preprocessing,
    worksheet_anti_bot,
    ws_no_links, ws_links_preprocessing
)

if __name__ == '__main__':
    def worksheet_all(worksheet):
        worksheet.update_cell(1, 4, 'Error')
        worksheet.update_cell(1, 1, 'Donor')
        worksheet.update_cell(1, 2, 'Acceptor')
        worksheet.update_cell(1, 3, 'Linkbuilder')


    try:
        worksheet_no_links.clear()
        worksheet_no_proxy_preprocessing.clear()
        worksheet_anti_bot.clear()

        time.sleep(3)

        worksheet_all(worksheet_no_links)
        worksheet_all(worksheet_no_proxy_preprocessing)
        worksheet_all(worksheet_anti_bot)

        time.sleep(3)

        np_ws_links = numpy.array(ws_links)
        p = Pool(processes=8)
        p.map(preprocessing_check_link, zip(np_ws_links[1:, 0], np_ws_links[1:, 1], np_ws_links[1:, 2]))
    except:
        pass

    try:
        np_ws_links_preprocessing = numpy.array(ws_links_preprocessing)
        for d, a, l in zip(np_ws_links_preprocessing[1:, 0], np_ws_links_preprocessing[1:, 1],
                           np_ws_links_preprocessing[1:, 2]):
            links_inf(d, a, l)

    except:
        pass
