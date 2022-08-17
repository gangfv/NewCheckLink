import time

from requests.exceptions import SSLError


def error(worksheet, donor, acceptor, linkbuilder, values):
    try:
        len_error = len(worksheet.col_values(1))
        worksheet.update_cell(len_error + 1, 1, donor)
        worksheet.update_cell(len_error + 1, 2, acceptor)
        worksheet.update_cell(len_error + 1, 3, linkbuilder)
        worksheet.update_cell(len_error + 1, 4, str(values))
    except SSLError:
        print("SSLError")
        time.sleep(60)
        len_error = len(worksheet.col_values(1))
        worksheet.update_cell(len_error + 1, 1, donor)
        worksheet.update_cell(len_error + 1, 2, acceptor)
        worksheet.update_cell(len_error + 1, 3, linkbuilder)
        worksheet.update_cell(len_error + 1, 4, str(values))
    except:
        time.sleep(60)
        len_error = len(worksheet.col_values(1))
        worksheet.update_cell(len_error + 1, 1, donor)
        worksheet.update_cell(len_error + 1, 2, acceptor)
        worksheet.update_cell(len_error + 1, 3, linkbuilder)
        worksheet.update_cell(len_error + 1, 4, str(values))
