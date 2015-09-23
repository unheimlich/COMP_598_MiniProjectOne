#!/usr/bin/env python

#
# FILE AND AUTHOR INFO HERE 
#

# import libraries 
import urllib, htmllib, re, sys
from bs4 import BeautifulSoup
from sets import Set



# grab URL string from command line arguments
url = "http://www.dailymail.co.uk/home/index.html"

#declare global variables and structures
unscrapedLinks = set([url])
scrapedLinks = set([])
counter = 0
limit = 200
path = "../data/PartTwo/scraped"
urlPrefix = "http://www.dailymail.co.uk"

#as long as we have links we haven't explored, keep iterating
while unscrapedLinks:
	# quit loop after scraping to a limit
	if len(scrapedLinks) > limit: break

	# remove top item from set
	url = unscrapedLinks.pop()

	# try to open connection to website
	try:
		website = urllib.urlopen(url)
	except IOError:
		print("[Scraper]:: Encountered malformed URL: "+url+". Will continue scraping...")
		scrapedLinks.add(url)
		continue
	# read html into the data variable
	data = website.read()
	# close the connection
	website.close()

	# we only save the page if it is an article. 
	if 'article' in url:
		# name for scraped files
		fname = path+str(counter)+".html"
		counter += 1

		# open new file, make first line the URL then write the entire HTML file
		htmlfile = open(fname, "w")
		htmlfile.write("<!--"+url+"-->\n")
		htmlfile.write(data)
		htmlfile.close()
		print("Saved article #"+str(counter)+": "+url)

	# to scraped list
	scrapedLinks.add(url)

	# even if we didn't save, we still want all the links on the page
	soup = BeautifulSoup(data, "html.parser")
	#find all anchors and add them to the unscraped set
	for link in soup.find_all('a'):
		# get the ref
		ref = link.get('href')

		# filter the anchor list with some basic patterns
		if ref == None: continue
		if '.html' not in ref: continue
		if 'dailymail' in ref: continue
		if '#' in ref: continue
		if 'www' in ref: continue
		if 'http' in ref: continue

		# add the dailymail prefix to the anchor
		childURL = urlPrefix+ref
		#if we already scraped that link, don't add.
		if childURL in scrapedLinks: continue
		unscrapedLinks.add(childURL)

print("Number of unscraped links upon exit: "+str(len(unscrapedLinks)))
		

 	


