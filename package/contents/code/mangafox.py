#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Module to get updates data from MangaFox.me

@package mangafox
'''

import urllib2
from bs4 import BeautifulSoup
from htmllib import HTMLParser

import time
import os


MANGAFOXURL = "http://mangafox.me/releases/"

def formate_string(string):
	string = string.replace("\r", "")
	html_escape_table = {
	    "&": "&amp;",
	    '"': "&quot;",
	    "'": "&apos;",
	    ">": "&gt;",
	    "<": "&lt;",
	    }
	p = HTMLParser(None)
	p.save_bgn()
	p.feed(string)
	return p.save_end()
	#return "".join(html_escape_table.get(c,c) for c in string)
	
	return string

def getHtmlUpdates(url):
	""" Get HTML with updates """
	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPHandler(debuglevel=0))
	opener.addheaders = [ ('User-agent', "Mozilla/5.0 (X11; Linux x86_64; rv:14.0)"
					" Gecko/20100101 Firefox/14.0.1") ]
	responce = opener.open(url)
	return "".join(responce.readlines())

def listUpdates(html):
	""" Create list HTML with updates"""
	soup = BeautifulSoup(html)
	updates = soup.find("ul", attrs={"id": "updates"})
	result = updates.findAll('li')
	return result

def parseItem(item):
	""" Parsing data for one updated manga"""
	manga = {}
	manga['title'] = unicode(item.find('a').contents[0])
	manga['descr_url'] = unicode(item.find('a').get('href'))
	manga['date'] = unicode(item.find('em').contents[0])
	if item.find('span', attrs={'class' : 'hotch'}) is not None:
		manga['hot_new'] = unicode('hot')
	elif item.find('span', attrs={'class' : 'newch'}) is not None:
		manga['hot_new'] = unicode('new')
	else:
		manga['hot_new'] = None
	chapters_list = item.findAll('a', attrs = {'class' : 'chapter'})
	manga['chapters'] = []
	for chapter in chapters_list:
		link = unicode(chapter.get('href'))
		number = unicode(chapter.contents[0])
		manga['chapters'].append((number, link))
	return manga

def parseUpdates():
	""" Create list with all updates"""
	html = getHtmlUpdates(MANGAFOXURL)
	mangalist = listUpdates(html)
	mangaUpdates = []
	for item in mangalist:
		mangaUpdates.append(parseItem(item))
	return mangaUpdates

def getDescription(url):
	""" Find description for manga """
	html = getHtmlUpdates(url)
	soup = BeautifulSoup(html)
	if not (soup.find('p', attrs = {'class': 'summary'}) == None):
		temp = soup.find('p', attrs = {'class': 'summary'}).contents
		description = u''
		for p in temp:
			if not (p == '<br />'):
				description += unicode(p)
		print temp
	else:
		description = "Description is missing at this moment"
	#description = formate_string(description)
	image_url = soup.find('div', attrs = {'class': 'cover'}).find('img').get('src')
	return description, image_url

if __name__ == "__main__":
	mangalist = parseUpdates()
	print mangalist
	print "Title: %s\n" % mangalist[1]['title'] 
	print "Updated: %s\n" % mangalist[1]['date']
	print getDescription(mangalist[1]['descr_url'])
	for i in mangalist[1]['chapters']:
		chapter, url = i
		print "Updated chapter: %s\n" % chapter
	print str(mangalist[1]['chapters'])
