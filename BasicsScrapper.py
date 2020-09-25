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
    
    def readValuation(self,ratioList):
        valueList = {}
        for ratio in ratioList:
            key = ratio.find("div", class_="value_txtfl").text
            if ( key  in self.COLUMNS_NEEDED):
                value = to_float(ratio.find("div", class_="value_txtfr").text)
                valueList[key] = value
        return valueList
    
    def isNotEmpty(self, cssTagVal):
        if( cssTagVal):
            return False
        if('-' in cssTagVal):
            return False
    
        return True
        
    def readPage(self):
        
        soup = self.getPage()
        basicData ={'name':'','Avg Score':0,'Highest Score':0,'Company Overview':' ','price':0,'52low':0, '52high':0, 'sector':'','Market Cap (Rs Cr.)':0,'P/E':0,'Book Value (Rs)':0,'Dividend (%)':0,'Industry P/E':0,'EPS (TTM)':0,'P/C':0,'Price/Book':0,'Dividend Yield.(%)':0,'Face Value (RS)':0,'url':''}
        #Name extraction is kept out of try block because, I want the processing of the data to stop in case name extraction is not done
        # If extraction of any other column is failed, it's ok, as other basic data columns are not used to rate/score the company.
        name = soup.find("h1", class_="pcstname").text
        basicData["name"] = name
        basicData["url"] = self.url
        try:
            price = to_float(soup.find("span", class_="txt15B nse_span_price_wrap hidden-xs").text)
            basicData["price"] = price
            div52HiLo = soup.find("div", class_="clearfix lowhigh_band week52_lowhigh_wrap")
            low52 = to_float(div52HiLo.find("div", class_="low_high1").text)
            high52 = to_float(div52HiLo.find("div", class_="low_high3").text)
            basicData["52low"] = low52
            basicData["52high"] = high52
       
            sector = soup.find("p", class_="bsns_pcst disin").find("span", class_="hidden-lg").text
            basicData["sector"] = sector
            companyOverview = soup.find("div", class_="morepls_cnt").text if( self.isNotEmpty(soup.find("div", class_="morepls_cnt"))) else ' '
            basicData["Company Overview"] = companyOverview
            basicRatios = soup.find("div", id="consolidated_valuation")
            ratioList = basicRatios.find_all("li", class_="clearfix")
            valueList = self.readValuation(ratioList)
            if(valueList["P/E"]== 0 and valueList["Book Value (Rs)"]==0):  #Consolidated section does not have any value. We need to read standalone tab
                print("ERROR: consolidated Value list is empty, reading standalone value list")
                basicRatios = soup.find("div", id="standalone_valuation")
                ratioList = basicRatios.find_all("li", class_="clearfix")
                valueList = self.readValuation(ratioList)
            basicData.update(valueList)    
            return basicData
            
            
        except (Exception) as error : #If Basic data collection fails, continue with whatever is collected
            print("ERROR: Failed to read Basic data for url : ", self.url ,error)
            
        return basicData
        
 
# bscS = BasicsScrapper("https://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/pageindustries/PI35")
# print(bscS.readPage())
