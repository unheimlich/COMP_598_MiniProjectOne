#!/usr/bin/env python

import urllib, htmllib, re, sys
from bs4 import BeautifulSoup

url = sys.argv[1]

website = urllib.urlopen("http://"+url)
data = website.read()
website.close()

soup = BeautifulSoup(data, "html.parser")

for link in soup.find_all('a'):
    print(link.get('href'))
