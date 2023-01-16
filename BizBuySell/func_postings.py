# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 22:04:09 2023

@author: Filip
"""


#import libraries necessary for web-scraping
import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag
from pprint import pprint
import requests
import re
import pandas as pd

from urllib.request import Request, urlopen


# scrape data from link - html parsing

def scraper_html(url_link):
  req = Request(
      url=url_link, 
      headers={'User-Agent': 'Mozilla/5.0'}
  )
  webpage = urlopen(req).read()
  soup = BeautifulSoup(webpage, "html.parser")
  return soup

# clean data - remove new rows
def clean_text(lista):
  result = []
  for i in lista:
    text = re.sub(r'\r\n', '', i)
    text = re.sub(r'\n','', text)
    text = text.split('                        ')
    result.append(text)
  information_2 = [item for sublist in result for item in sublist]
  df_dict = dict(kv.split(':') for kv in information_2)
  df_dict = {k.strip(): v for (k, v) in df_dict.items()}
  df_1 = pd.DataFrame(df_dict, index=[0])
  return df_1


# export data from html
def export_from_html(test):
  information = []
  description = ''
  k = []
  v = []
  for header in test.find_all(True,{'class':['span6 specs','businessDescription','listingProfile_details']}):
      nextNode = header
      if nextNode.find(class_ = "title"):
        text = nextNode.text.strip()
        information.append(text)
      elif nextNode.find("dt"):
        k = [i.text for i in test.select('dt')] 
        v = [i.text for i in test.select('dd')]
      else:
        description = nextNode.text.strip()
      res = clean_text(information)
      res['Listing Description'] = description
      for i in range(0,len(k)-1):
        res[k[i]]= v[i]
  return res


# to be revised
def listing_type(url):
  if "Business-Asset" in url:
    return "Asset Sales"
  elif "Business-Real-Estate-For-Sale" in url:
    return "Real Estate"
  elif "Start-Up-Business" in url:
    return "Start-Up Businesses"
  elif "Business-Opportunity" in url:
    return "Established Businesses"
  else:
    return "Other"