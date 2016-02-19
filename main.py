# minimal crawler script. gathers unique 'href' attrs from <a> tags, searchs breadth first, crawls until URL_LIMIT is reached. view urls on completion optional. prints updates to console.

import urllib
from lxml.html import parse
import sys
import time

URL_LIMIT = 500

def is_image(url):
	'''takes filename as a string. returns True if url has common image extension, False if not'''
	if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.gif') or url.endswith('.gifv') or url.endswith('.ico') or url.endswith('.svg') or url.endswith('.swf') or url.endswith('.bmp') or url.endswith('.pdf'):
		return True
	else:
		return False

def is_script(url):
	'''takes filename as string. returns True if undesired script, False if not'''
	if url.startswith('javascript:') or url.startswith('mailto:') or url.startswith('tel:') or url.startswith('ios-app:'):
		return True
	else:
		return False

class crawler:

	def __init__(self, start_url):
		'''initializes member variables'''
		self.urls = []
		self.popped = []
		self.urls.append(start_url)
		self.fetched = 0

	def total_urls(self):
		'''returns number of total unique urls gathered'''
		return len(self.urls) + len(self.popped)

	def get_page(self):
		'''attempts to retrieve resource. attempts to parse resource. returns lxml.HtmlElement object or None'''
		site = self.urls.pop()
		self.popped.append(site)
		try:
			print 'fetching ' + str(site)
			handle = urllib.urlopen(site)
			page = parse(handle).getroot()
			self.fetched += 1
			return page
		except IOError as e:
			print 'problem getting ' + str(site)
			print e
			return None
		except UnicodeEncodeError:
			print 'format error'
			return None
		except UnicodeError:
			print 'format error'
			return None

	def scrape_links(self, page):
		'''takes lxml.HtmlElement as page. adds unique links to url queue.'''
		new_links = 0
		page.make_links_absolute()
		for link in page.iterlinks():
			if link[1] == 'href':
				url = link[2]
				if url not in self.popped and url not in self.urls:       # new find
					if (not is_image(url)) and (not is_script(url)):  # only want parsable documents
						self.urls.append(url) 			  # add it to list of urls to be crawled
						new_links += 1
						if self.total_urls() == URL_LIMIT:
							return
		print str(new_links) + ' new links gathered'


if len(sys.argv) == 2:
	start_url = sys.argv[1]
else:
	print 'run as:\n$python main.py <START_URL>'
	sys.exit()
crawly = crawler(start_url)
print 'scraping for ' + str(URL_LIMIT) + ' uniques urls.'
start_time = time.time()

while (0 < crawly.total_urls() < URL_LIMIT) and (len(crawly.urls) > 0): 		  # only want URL_LIMIT urls
	page = crawly.get_page()
	if page != None:
		crawly.scrape_links(page)	
	print str(crawly.total_urls()) + ' unique links gathered'
	print str(crawly.fetched) + ' resources fetched'

if crawly.total_urls() == URL_LIMIT:
	print 'success!\nthe limit of ' + str(URL_LIMIT) + ' urls has been reached!'
	duration = time.time() - start_time
	duration = duration % 100
	print 'took ' + str(int(duration)) + ' seconds!'
else:
	print 'out of links!'

response = raw_input('view urls? y/n\n')						  # prompt user to print urls
if response.upper() == 'y'.upper() or response == 'yes'.upper():
	print_urls = crawly.urls
	for url in crawly.popped:
		print_urls.append(url)
	print_urls.sort()
	for url in print_urls:
		try:
			print url
		except UnicodeEncodeError:
			print "can't print site"
		time.sleep(.01)
