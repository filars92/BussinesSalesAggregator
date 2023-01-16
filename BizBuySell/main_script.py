# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 21:20:40 2023

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


import func_listings as fl
import func_postings as fp


# add all industries 
industries = {
    "Agriculture":"agriculture",
    "Financial Services":"financial-services",
    "Retail":"retail",
    "Automotive & Boat":"automotive-and-boat",
    "Health Care & Fitness":"health-care-and-fitness",
    "Service Businesses":"service-businesses",
    "Beauty & Personal Care":"beauty-and-personal-care",
    "Manufacturing":"manufacturing",
    "Transportation & Storage":"transportation-and-storage",
    "Building & Construction":"building-and-construction",
    "Non-Classifiable Establishments":"non-classifiable-establishments",
    "Travel":"travel",
    "Communication & Media":"communication-and-media",
    "Online & Technology":"online-and-technology",
    "Wholesale & Distributors":"wholesale-and-distributors",
    "Education & Children":"education-and-children",
    "Pet Services":"pet-services",
    "Entertainment & Recreation":"entertainment-and-recreation",
    "Restaurants & Food":"restaurants-and-food"
}

# --------------------------------------------------- #
###        SCRAPE, TRANSFORM &  EXPORT DATA 
# --------------------------------------------------- #


main_url = 'https://www.bizbuysell.com/'
suffix = '-businesses-for-sale/'
industry_links = []
dfs = []


for value in industries:
  whole_url = main_url + industries[value] + suffix
  industry_links.append(whole_url)
  soup = fl.scraper_main(whole_url)
  listings = fl.find_listings(soup)
  
  for i in listings[:1]:
     t = fp.scraper_html(i)
     c = fp.export_from_html(t)
      # c = clean_text(k)
     c["Listing Type"] = fp.listing_type(i)
     c["Industry"] = value #this is hard-coded for now, so it needs to be changed once we include all industries
     c["Listing URL"] = i
     c["Listing Source"] = 'Biz Buy Sell' #hard-coded
    
     dfs.append(c)

df_2 = pd.concat(dfs)


df_2.to_excel("bizbuysell_test1.xlsx")