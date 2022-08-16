import gspread

from core.attribute.credentials import credentials

gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1dEYWYC5ZDOFGwxUSs3WnBsk32vOouT43TuAp7iFO7ic/')

worksheet_links = sh.worksheet('Links')
ws_links = worksheet_links.get_all_values()

worksheet_no_proxy_preprocessing = sh.worksheet('Preprocessing')
ws_links_preprocessing = worksheet_no_proxy_preprocessing.get_all_values()

worksheet_no_links = sh.worksheet('No Link')
ws_no_links = worksheet_no_links.get_all_values()

worksheet_anti_bot = sh.worksheet('Anti-Bot')
