import numpy

from core.google_links import ws_links

np_ws_links = numpy.array(ws_links)
print(np_ws_links.idnex(""))
print(', '.join(map(str, np_ws_links.ravel())))