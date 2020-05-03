#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 20:34:42 2020

@author: sharvarinagesh

Basic Scrapper when passed the companies base URL scraps basic information like, name of the company, current price, 52 week low/high, sector, Overview of the company. market cap, p/e etc
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from Util import to_float

class BasicsScrapper :
    COLUMNS_NEEDED =['Market Cap (Rs Cr.)', 'P/E','Book Value (Rs)','Dividend (%)','Industry P/E','EPS (TTM)', 'P/C', 'Price/Book', 'Dividend Yield.(%)','Face Value (RS)']
    
    def __init__(self, url):
        self.url = url

    def getPage(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')  #pass the page content through BeautifulSoup
        # table = soup.find("table", class_="mctable1")   # All the financial data is in the table "mctable1"
        return soup

    def readPage(self):
        soup = self.getPage()
        basicData ={}
        name = soup.find("h1", class_="pcstname").text
        basicData["name"] = name
        basicData["url"] = self.url
        price = to_float(soup.find("span", class_="txt15B nse_span_price_wrap hidden-xs").text)
        basicData["price"] = price
        div52HiLo = soup.find("div", class_="clearfix lowhigh_band week52_lowhigh_wrap")
        low52 = to_float(div52HiLo.find("div", class_="low_high1").text)
        high52 = to_float(div52HiLo.find("div", class_="low_high3").text)
        basicData["52low"] = low52
        basicData["52high"] = high52
   
        sector = soup.find("p", class_="bsns_pcst disin").find("span", class_="hidden-lg").text
        basicData["sector"] = sector
        companyOverview = soup.find("div", class_="morepls_cnt").text
        basicData["Company Overview"] = companyOverview
        basicRatios = soup.find("div", id="consolidated_valuation")
        rationList = basicRatios.find_all("li", class_="clearfix")
        for ratio in rationList:
            key = ratio.find("div", class_="value_txtfl").text
            if ( key  in self.COLUMNS_NEEDED):
                value = to_float(ratio.find("div", class_="value_txtfr").text)
                basicData[key] = value
        return basicData
    
 
# bscS = BasicsScrapper("https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/bosch/B05")
# print(bscS.readPage())
