# gather 1000 unique urls and print error messages

from lxml.html import parse
import sys

class crawler:

	def __init__(self, start_url):
		self.urls = []
		self.duplicates = []
		self.urls.append(start_url)

	def get_page(self):
		site = self.urls.pop()
		self.duplicates.append(site)
		try:
			page = parse(site).getroot()
			return page
		except IOError as e:
			print e
			return None	

	def scrape_links(self, page):
		page.make_links_absolute()
		for link in page.iterlinks():
			if link[1] == 'href':
				if link[2] not in self.duplicates and link[2] not in self.urls:
					self.urls.append(link[2])
				elif link[2] in self.urls:
					self.duplicates.append(link[2])	


if len(sys.argv) == 2:
	start_url = sys.argv[1]
else:
	print 'run as $python main.py <START_URL>'
	sys.exit()

crawly = crawler(start_url)

while 0 < len(crawly.urls) < 1000:
	page = crawly.get_page()
	if page != None:
		crawly.scrape_links(page)	

print len(crawly.urls)
if len(crawly.urls) > 1000:
	print 'success!'
else:
	print 'no more links!'
