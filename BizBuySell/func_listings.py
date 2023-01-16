# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:45:58 2023

@author: Filip
"""

#import security protocol
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#import libraries necessary for web-scraping
import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag
from pprint import pprint
import requests
import re
import pandas as pd

from urllib.request import Request, urlopen


# scrape data from main link (used for scraping of url links of listings) - lxml parsing

def scraper_main(url_link):
  req = Request(
      url=url_link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  webpage = urlopen(req).read()
  soup = BeautifulSoup(webpage, "lxml")
  return soup


# find all listings 

def find_listings(soup):
  headers = []
# I - find all text
  for header in soup.find_all('app-listing-diamond'):
      nextNode = header
      while True:
          nextNode = nextNode.nextSibling
          if nextNode is None:
              break
          if isinstance(nextNode, NavigableString):
              continue
          headers.append(str(nextNode))
# II - get url text and remove duplicates  
  business_urls = []      
  for i in headers:
    mk1 = str(i).find('href="') + 6
    mk2 = str(i).find('?d=undefined', mk1)
    subString = str(i)[mk1:mk2]
    business_urls.append(subString)
  business_urls = set(business_urls)
# III - get the url (clean) - remove unnecessary urls
  business_urls_clean = []
  for i in business_urls:
    if 'business-broker' not in i and "Business" in i:
      business_urls_clean.append(i)
# IV - return whole urls for the listings
  business_urls_total = []
  url_1 =  'https://www.bizbuysell.com'
  for i in business_urls_clean:
    business_urls_total.append(url_1+i)

  return business_urls_total