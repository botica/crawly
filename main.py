import urllib
from lxml import etree

website = urllib.urlopen("http://news.google.com")
page = website.read()
html = etree.HTML(page)
pretty = etree.tostring(html, pretty_print=True, method="html")
# print pretty
