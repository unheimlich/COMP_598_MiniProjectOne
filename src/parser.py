#!/usr/bin/env python

#
# @author Kyle Brumsted
# @author Suzin You
#
# This program reads each stored HTML file from the scraper and parses it to extract the features for our dataset.

# import libraries 
import urllib, htmllib, re, sys, codecs
from bs4 import BeautifulSoup
from sets import Set
from datetime import datetime, timedelta

# Total number of files properly formatted that had successful feature extraction.
total_success = 0


#location of scraped files
path = "/Volumes/SeagateBackup/"
folder = ''

#set of parsed links so we don't have duplicates in our dataset
parsedLinks = set([])

#the csv file to be written to
csv = open(path+"dataNew.csv", "w")

#folder with scraped html
folder = "scraped3/"


#loop through scraped files
for counter in range(0,11560):
	fname = path+folder+str(counter)+".html"
	if (counter % 100) == 0: print("opening file "+path+folder+str(counter)+" ...")

	# The set of features to be extracted from each file. Description of each found in AttributeInfo.txt
	url = ''
	timedelta = ''
	n_tokens_title = 0
	n_tokens_content = 0
	n_unique_tokens = 0
	num_hrefs = 0
	num_self_hrefs = 0
	num_imgs = 0
	num_videos = 0
	average_token_length = 0
	num_keywords = 0
	data_channel_is_news = 0
	data_channel_is_ushome = 0
	data_channel_is_sport = 0
	data_channel_is_tvshowbiz = 0
	data_channel_is_auhome = 0
	data_channel_is_femail = 0
	data_channel_is_health = 0
	data_channel_is_sciencetech = 0
	data_channel_is_money = 0
	data_channel_is_video = 0
	data_channel_is_travel = 0
	weekday_is_monday = 0
	weekday_is_tuesday = 0
	weekday_is_wednesday = 0
	weekday_is_thursday = 0
	weekday_is_friday = 0
	weekday_is_saturday = 0
	weekday_is_sunday = 0
	is_weekend = 0
	num_shares = 0

	#open the file and put it into a BS object
	try:
		s = codecs.open(fname, 'r', encoding = 'utf-8').read()
		htmlfile = codecs.encode(s, 'ascii', 'ignore')
	except UnicodeDecodeError:
		print("[parser]:: UnicodeDecodeError. skipping file.")
		continue

	soup = BeautifulSoup(htmlfile, "html.parser")

	# Extract share count from div, if this count is dynamically generated for the given file, we skip it and move on to the next one.
	shares = soup.find("div", class_='share-count')
	if shares != None:
		num_shares = shares.contents[1].text
		if 'k' in num_shares:
			x = 1000
			newshares = 0
			num = re.findall(r'\d+',num_shares)
			for digit in num:
				newshares = newshares + (int(digit)*x)
				x = x/10
			num_shares = str(newshares)
	else:
		print(" no shares value")
		continue

	# Find the 'link' element and extract the url and channel info from it.
	# If url already parse, we skip this file.
	linkEl = soup.find("link")
	if linkEl != None:
		links = str(linkEl).split("\"")
		url = links[1]
		if url in parsedLinks:
			print("url "+url+" already in parsed links")
			continue
		else:
			parsedLinks.add(url)
		toks = url.split("/")
		#Extract the channel
		channel = toks[3]
		if channel == 'news':
			data_channel_is_news = 1
		elif channel == 'ushome':
			data_channel_is_ushome = 1
		elif channel == 'sport':
			data_channel_is_sport = 1
		elif channel == 'tvshowbiz':
			data_channel_is_tvshowbiz = 1
		elif channel == 'auhome':
			data_channel_is_auhome = 1
		elif channel == 'femail':
			data_channel_is_femail = 1
		elif channel == 'health':
			data_channel_is_health = 1
		elif channel == 'sciencetech':
			data_channel_is_sciencetech = 1
		elif channel == 'money':
			data_channel_is_money = 1
		elif channel == 'video':
			data_channel_is_video = 1
		else:
			data_channel_is_travel = 1
	else: 
		print("		failed to get url and channel info")
		continue



	# Gather all text in content body
	allText = ""
	paras = soup.find_all("p", class_='mol-para-with-font')
	if paras != None:
		for p in paras:
			if p.contents != []:
				try:
					allText = allText+" "+p.contents[0].text
				except AttributeError:
					print("		[parser]:: error in parsing; probably empty tag with a space. will continue.")
					continue
	# Necessary because DailyMail has two different html structures for content body.
	if len(allText) == 0:
		paras = soup.find_all("font")
		if paras != None:
			for p in paras:
				if p.contents != []:
					try:
						allText = allText+" "+str(p.contents[0])
					except AttributeError:
						print("		[parser]:: error in parsing; probably empty tag with a space. will continue.")
						continue
	# If HTML format follows neither of the normal conventions, we skip this file.
	if len(allText) == 0: 
		print("		can't get text body")
		continue

	# Calculate the features relating to the content body (total word count, unique word count, average word length)
	totlen = 0.0
	toks = allText.split(" ")
	for tok in toks:
		tok = tok.replace('\n',"").replace("'","").replace(".","").replace(",","").replace("-","").lower() # surely there is a builtin python method for removing punctuation
		totlen = totlen + len(tok)*1.0
	n_tokens_content = len(toks)
	
	average_token_length = totlen/(len(toks)*1.0)

	uniqueWords = set(toks)
	n_unique_tokens = len(uniqueWords)

	# Extract the title and count the tokens
	title = soup.find("title")
	if title != None:
		title = str(title.text)
		title = title.replace(" | Daily Mail Online","")
		toks = title.split(" ")
		n_tokens_title = len(toks)
	else: 
		print("		no title element")
		continue

	# Extract and count the keywords
	metaEl = soup.find("meta")
	if metaEl != None:
		keywds = str(metaEl).split("\"")
		wds = keywds[1].split(",")
		num_keywords = len(wds)
	else:
		print("		no keywords element")
		continue


	# Find the date published.
	date = soup.find("span","article-timestamp article-timestamp-published")
	if date == None:
		print("		no date element")
		continue
	try:
		published = datetime.strptime(date.text, '\n  Published:\n  %H:%M GMT, %d %B %Y\n')
	except ValueError:
		print("		[parser]:: ValueError, will continue")
		continue
	td = datetime.now()-published
	timedelta = td.days
	if timedelta < 0: timedelta = 0

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

	# Extract number of images
	for img in soup.find_all("div", class_="mol-img"):
	    num_imgs += 1

	# Extract number of videos
	for vid in soup.find_all("div", class_="moduleFull mol-video"):
	    num_videos += 1

	# Count the total number of links and the number of links that point back to DailyMail
	for link in soup.find_all('a'):
		ref = link.get('href')
		if ref != None:
			num_hrefs += 1
			if 'dailymail' in ref:
				num_self_hrefs += 1

	# If all features are successfully gathered, we write them to the CSV file.
	line = url+","+str(timedelta)+","+str(n_tokens_title)+","+str(n_tokens_content)+","+str(n_unique_tokens)+","+str(num_hrefs)+","+str(num_self_hrefs)+","+str(num_imgs)+","+str(num_videos)+","+str(average_token_length)+","+str(num_keywords)+","+str(data_channel_is_news)+","+str(data_channel_is_ushome)+","+str(data_channel_is_sport)+","+str(data_channel_is_tvshowbiz)+","+str(data_channel_is_auhome)+","+str(data_channel_is_femail)+","+str(data_channel_is_health)+","+str(data_channel_is_sciencetech)+","+str(data_channel_is_money)+","+str(data_channel_is_video)+","+str(data_channel_is_travel)+","+str(weekday_is_monday)+","+str(weekday_is_tuesday)+","+str(weekday_is_wednesday)+","+str(weekday_is_thursday)+","+str(weekday_is_friday)+","+str(weekday_is_saturday)+","+str(weekday_is_sunday)+","+str(is_weekend)+","+str(int(num_shares))+'\n'
	csv.write(line)
	total_success += 1

print ("total success: "+str(total_success))
csv.close()


