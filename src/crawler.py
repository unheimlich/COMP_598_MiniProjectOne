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

# put the html into a beautifulSoup object
soup = BeautifulSoup(data, "html.parser")

# Now using the beautifulSoup object we can parse and manipulate the document tree easily
#	- find number of photos, videos, words, links, etc
#	- search for shares or whatever the objective fn will be

# example: finding and printing all of the anchor elemnts and their references in the document tree
for link in soup.find_all('a'):
    print(link.get('href'))
