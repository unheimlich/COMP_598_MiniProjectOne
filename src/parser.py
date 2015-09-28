#!/usr/bin/env python

#
# FILE AND AUTHOR INFO HERE 
#

# import libraries 
import urllib, htmllib, re, sys
from bs4 import BeautifulSoup

#location of scraped files
path = "/Users/kylebrumsted/Documents/School/Fall2015/COMP598/Project1/scraped/"

#name of scraped files
counter = 0
fname = path+str(counter)+".html"

#open the file and put it into a BS object
htmlfile = open(fname, "r")
soup = BeautifulSoup(htmlfile, "html.parser")
htmlfile.close()

shares = soup.find("div", class_='share-count')
if shares != None:
	print shares.children