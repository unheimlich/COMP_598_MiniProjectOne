#!/usr/bin/env python

#
# FILE AND AUTHOR INFO HERE 
#

# import libraries 
#import urllib, htmllib, re, sys
import urllib, html.parser, re, sys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

#location of scraped files
path = "C://Users//Suzin//Desktop//COMP598 Machine Learning//Project 1//COMP_598_MiniProjectOne//data//PartTwo//Scraped//"

#name of scraped files
counter = 0
fname = path+str(counter)+".html"

#open the file and put it into a BS object
htmlfile = open(fname, "r")
soup = BeautifulSoup(htmlfile, "html.parser")
htmlfile.close()

#timedelta = soup.find("span", class_='article-timestamp article-timestamp-published')
#if timedelta != None:
#    print (timedelta.children)    
    #with datetime from datatime as dt:


# initialise variables
timedel = ''
weekday_is_monday = 0
weekday_is_tuesday = 0
weekday_is_wednesday = 0
weekday_is_thursday = 0
weekday_is_friday = 0
weekday_is_saturday = 0
weekday_is_sunday = 0
is_weekend = 0
n_hrefs = 0
n_self_hrefs = 0
n_imgs = 0
n_videos = 0


# timedelta
date = soup.find("span","article-timestamp article-timestamp-published")
published = datetime.strptime(date.text, '\n  Published:\n  %H:%M GMT, %d %B %Y\n')
#print (published)
td = datetime.now()-published
timedel = td.days

#weekday_is_
if published.weekday()==0:
	weekday_is_monday = 1
elif published.weekday()==1:
	weekday_is_tuesday = 1
elif published.weekday()==2:
	weekday_is_wednesday = 1
elif published.weekday()==3:
	weekday_is_thursday = 1
elif published.weekday()==4:
	weekday_is_friday = 1
elif published.weekday()==5:
	weekday_is_saturday = 1
	is_weekend = 1
else:
	weekday_is_sunday = 1
	is_weekend = 1

# n_hrefs & n_self_hrefs
panel = soup.find("ul","rotator-panels link-bogr1 linkro-ccox")
#print (panel)
try:
	for x in panel.find_all("href"):
		#print ("hrefs: \n",x.text)
		n_self_hrefs += 1
except AttributeError as noPanels:
	print ("something is wrong.")

# n_imgs
for img in soup.find_all("div", class_="mol-img"):
    n_imgs += 1

# n_videos
for vid in soup.find_all("div", class_="moduleFull mol-video"):
    n_videos += 1



print (timedel,",",weekday_is_monday,",",weekday_is_tuesday,",",weekday_is_wednesday,",",weekday_is_thursday,",",weekday_is_friday,",",weekday_is_saturday,",",weekday_is_sunday,",",is_weekend,",",n_hrefs,",",n_self_hrefs,",",n_imgs,",",n_videos)