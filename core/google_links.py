import gspread

from core.attribute.credentials import credentials

gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1dEYWYC5ZDOFGwxUSs3WnBsk32vOouT43TuAp7iFO7ic/')

worksheet_errors = sh.worksheet('Errors')
worksheet_no_links = sh.worksheet('No Link')
worksheet_cloudflare = sh.worksheet('CloudFlare')
worksheet_capcha = sh.worksheet('Capcha')

worksheet_links = sh.worksheet('Links')
ws_links = worksheet_links.get_all_values()
