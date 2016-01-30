# stop at 1000 urls
# time it and print duration after program ends
# not download and try to parse images
# calc approx time of printing at end and print

import urllib
from lxml.html import parse
import sys
import time

URL_LIMIT = 500

class crawler:

	def __init__(self, start_url):
		self.urls = []
		self.duplicates = []
		self.popped = []
		self.urls.append(start_url)

	def get_page(self):
		site = self.urls.pop()
		self.popped.append(site)
		self.duplicates.append(site)
		print 'fetching ' + str(site)
		try:
			handle = urllib.urlopen(site)
			page = parse(handle).getroot()
			return page
		except IOError as e:
			print 'problem getting ' + str(site)
			print e
			return None

	def scrape_links(self, page):
		links = 0
		page.make_links_absolute()
		for link in page.iterlinks():
			if link[1] == 'href':
				url = link[2]
				if url not in self.duplicates and url not in self.urls: # new find
					self.urls.append(url) # add it to list of urls to be crawled
					links += 1
				elif url in self.urls and url not in self.duplicates: # waiting to be crawled, add to duplicates
					self.duplicates.append(url)
		print str(links) + ' new links gathered'


if len(sys.argv) == 2:
	start_url = sys.argv[1]
else:
	print 'run as\n$ python main.py <START_URL>'
	sys.exit()

crawly = crawler(start_url)

while (0 < (len(crawly.urls) + len(crawly.popped)) < URL_LIMIT) and (len(crawly.urls) > 0):
	page = crawly.get_page()
	if page != None:
		crawly.scrape_links(page)	
	print str(len(crawly.urls) + len(crawly.popped)) + ' unique links so far'
	print str(len(crawly.popped)) + ' resources fetched (attempted)'

if len(crawly.urls) > URL_LIMIT:
	print 'success! the url limit has been reached!'
else:
	print 'out of links!'

response = raw_input('view urls? y/n\n')
if response == 'y':
	print_urls = crawly.urls
	for url in crawly.popped:
		print_urls.append(url)
	print_urls.sort()
	for url in print_urls:
		print url
		time.sleep(.01)

