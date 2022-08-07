import numpy as numpy
from multiprocessing import Pool
from core.google_links import ws_links, worksheet_errors
from utils.check_links import check_link

if __name__ == '__main__':

    mode = int(input("Выберите режим (test_link=0 или start=1): "))
    worksheet_errors.clear()
    worksheet_errors.update_cell(1, 1, 'Donor')
    worksheet_errors.update_cell(1, 2, 'Acceptor')
    worksheet_errors.update_cell(1, 3, 'Linkbuilder')
    worksheet_errors.update_cell(1, 4, 'Error')
    np_ws_links = numpy.array(ws_links)
    if mode == 1:
        process_count = int(input("Enter the number of processes: "))
        p = Pool(processes=process_count)
        p.map(check_link, zip(np_ws_links[1:, 0], np_ws_links[1:, 1]))
    else:
        donor = ["https://www.0619.com.ua/news/2426432/matc-aponia-cili"]
        acceptor = ["https://odds.ru/football/forecasts/stavka-i-prognoz-na-match-yaponiya-chili/"]
        p = Pool(processes=1)
        p.map(check_link, zip(donor, acceptor))
