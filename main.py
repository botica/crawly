import urllib
from lxml.html import parse
import sys
import time

URL_LIMIT = 300

def is_image(url):
	'returns true if url is common image, false if not'
	if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.gif') or url.endswith('.gifv') or url.endswith('.svg') or url.endswith('.swf') or url.endswith('.bmp') or url.endswith('pdf'):
		return True
	else:
		return False

def is_script(url):
	'returns true if script, false if not'
	if url.startswith('javascript') or url.startswith('mailto') or url.startswith('tel'):
		return True
	else:
		return False

class crawler:

	def __init__(self, start_url):
		self.urls = []
		self.popped = []
		self.urls.append(start_url)
		self.fetched = 0
		self.link_total = 0

	def total_urls(self):
		'returns number of total urls'
		return len(self.urls) + len(self.popped)


	def get_page(self):
		site = self.urls.pop()
		self.popped.append(site)
		print 'fetching ' + str(site)
		try:
			handle = urllib.urlopen(site)
			page = parse(handle).getroot()
			self.fetched += 1
			return page
		except IOError as e:
			print 'problem getting ' + str(site)
			print e
			return None

	def scrape_links(self, page):
		new_links = 0
		page.make_links_absolute()
		for link in page.iterlinks():
			if link[1] == 'href':
				url = link[2]
				if url not in self.popped and url not in self.urls: # new find
					if (not is_image(url)) and (not is_script(url)): # only want parsable documents
						self.urls.append(url) # add it to list of urls to be crawled
						new_links += 1
						self.link_total += 1
						if self.total_urls() == URL_LIMIT:
							return
		print str(new_links) + ' new links gathered'


if len(sys.argv) == 2:
	start_url = sys.argv[1]
else:
	print 'run as\n$ python main.py <START_URL>'
	sys.exit()
crawly = crawler(start_url)
print 'scraping for ' + str(URL_LIMIT) + ' uniques urls.'
start_time = time.time()

while (0 < crawly.total_urls() < URL_LIMIT) and (len(crawly.urls) > 0):
	page = crawly.get_page()
	if page != None:
		crawly.scrape_links(page)	
	print str(crawly.total_urls()) + ' unique links'
	print str(crawly.fetched) + ' resources fetched'

if crawly.total_urls() == URL_LIMIT:
	print 'success!\nthe limit of ' + str(URL_LIMIT) + ' urls has been reached!'
	duration = time.time() - start_time
	duration = duration % 100
	print 'took ' + str(int(duration)) + ' seconds!'
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

