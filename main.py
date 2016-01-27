# gather 1000 unique urls

from lxml.html import parse

urls = []
dups = []

start = 'http://www.google.com/'
urls.append(start)

def get_page():
	site = urls.pop()
	dups.append(site)
	try:
		page = parse(site).getroot()
		return page
	except IOError as e:
		print e
		return None

def scrape_links(page):
	page.make_links_absolute()
	for link in page.iterlinks():
		if link[1] == 'href':
			if link[2] not in dups and link[2] not in urls:
				urls.append(link[2])
			elif link[2] in urls:
				dups.append(link[2])

while 0 < len(urls) < 1000:
	page = get_page()
	if page != None:
		scrape_links(page)

print len(urls)
if len(urls) > 1000:
	print 'success!'
else:
  print '=['
