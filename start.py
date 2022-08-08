import numpy as numpy
from multiprocessing import Pool
from core.google_links import ws_links, worksheet_errors, worksheet_cloudflare, worksheet_no_links, worksheet_capcha
from utils.check_links import check_link

if __name__ == '__main__':

    mode = int(input("Выберите режим (test_link=0 или start=1): "))


    def worksheet_all(worksheet):
        worksheet.clear()
        worksheet.update_cell(1, 1, 'Donor')
        worksheet.update_cell(1, 2, 'Acceptor')
        worksheet.update_cell(1, 3, 'Linkbuilder')
        worksheet.update_cell(1, 4, 'Error')


    worksheet_all(worksheet_errors)
    worksheet_all(worksheet_no_links)
    worksheet_all(worksheet_cloudflare)
    worksheet_all(worksheet_capcha)

    np_ws_links = numpy.array(ws_links)

    if mode == 1:
        process_count = int(input("Enter the number of processes: "))
        p = Pool(processes=process_count)
        p.map(check_link, zip(np_ws_links[1:, 0], np_ws_links[1:, 1]))
    else:
        donor = [
            "https://angvremya.ru/sport/49530-snova-vdvoem-wintrike-team-rasstajutsja-s-tremja-chlenami-sostava-po-dota-2.html"]
        acceptor = ["https://odds.ru/football/forecasts/stavka-i-prognoz-na-match-yaponiya-chili/"]
        p = Pool(processes=1)
        p.map(check_link, zip(donor, acceptor))
