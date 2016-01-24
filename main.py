import urllib

website = urllib.urlopen("http://google.com")
print website.info()
