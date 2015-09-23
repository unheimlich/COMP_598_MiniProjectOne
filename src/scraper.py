#!/usr/bin/env python

#
# FILE AND AUTHOR INFO HERE 
#

# import libraries 
import urllib, htmllib, re, sys
from bs4 import BeautifulSoup

# grab URL string from command line arguments
url = sys.argv[1]

# open connection to website
website = urllib.urlopen("http://"+url)
# read html into the data variable
data = website.read()
# close the connection
website.close()

#destination for scraped files
path = "/Users/kylebrumsted/Documents/School/Fall2015/COMP598/Project1/scraped/"

#name for scraped files
counter = 0
fname = path+str(counter)+".html"

#Open new file, make first line the URL then write the entire HTML file
htmlfile = open(fname, "w")
htmlfile.write("<!--"+url+"-->")
htmlfile.write(data)
htmlfile.close()

'''
TODO: Gather anchor list, scrape each ref, increment the counter on each one. Also need to create a list of scraped links.

soup = BeautifulSoup(data, "html.parser")
for link in soup.find_all('a'):

	ref = link.get('href')

	if ref == None:
		continue
	
	#All the links that end in .html are from dailymail; all others go to external sites.
	if '.html' not in ref:
		continue
	
 	print(ref)
 	#These refs all need http://www.dailymail.co.uk prefix. Make sure to account for this in scraping and in
 '''


