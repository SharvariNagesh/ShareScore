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
        if(not cssTagVal):
            return False
        if('-' in cssTagVal):
            return False
    
        return True
    
    def findIf(self,soup, tag, clas):
        try:
            if( self.isNotEmpty(soup.find(tag, class_= clas).text)):
               return to_float(soup.find(tag, class_=clas).text) 
        except (Exception) as error : #If Basic data collection fails, continue with whatever is collected
            print("ERROR: Failed to read tag and class : ", tag,clas ,error)
        
        return 0
        
    def readPage(self):
        
        soup = self.getPage()
        basicData ={'name':'','Beta':0,'Avg Score':0,'Highest Score':0,'Company Overview':' ','price':0,'52low':0, '52high':0, 'sector':'','Market Cap (Rs Cr.)':0,'P/E':0,'Book Value (Rs)':0,'Dividend (%)':0,'Industry P/E':0,'EPS (TTM)':0,'P/C':0,'Price/Book':0,'Dividend Yield.(%)':0,'Face Value (RS)':0,'url':''}
        #Name extraction is kept out of try block because, I want the processing of the data to stop in case name extraction is not done
        # If extraction of any other column is failed, it's ok, as other basic data columns are not used to rate/score the company.
        
        basicData["url"] = self.url
        try:
            basicDetails = soup.find("div", class_="inid_name")
            basicData["name"] = basicDetails.find("h1").text
            basicData["sector"]= ' '.join(basicDetails.find("a").text.split()) # There are some extra spaces
            basicData["price"] = self.findIf(soup, "div", "inprice1 nsecp")
            
            basicData["52low"] = self.findIf(soup, "td", "nseL52 bseL52")
            basicData["52high"] = self.findIf(soup, "td", "nseH52 bseH52")
            
            basicData['Market Cap (Rs Cr.)']=self.findIf(soup, "td", "nsemktcap bsemktcap")
            basicData['P/E']=self.findIf(soup, "td", "nsepe bsepe")
            basicData['Book Value (Rs)']= self.findIf(soup,"td", "nsebv bsebv")
            basicData['Dividend (%)']=0
            basicData['Industry P/E']=self.findIf(soup, "td", "nsesc_ttm bsesc_ttm")
            basicData['EPS (TTM)']=self.findIf(soup, "td", "nseceps bseceps")
            basicData['P/C']=self.findIf(soup, "td", "nseL52 bseL52")
            basicData['Price/Book']=self.findIf(soup, "td", "nsepb bsepb")
            basicData['Dividend Yield.(%)']=self.findIf(soup,"td", "nsedy bsedy")
            basicData['Face Value (RS)']=self.findIf(soup,"td","nsefv bsefv")
            basicData['Company Overview']=""
            basicData['Beta']=self.findIf(soup,"span", "nsebeta")
           
        
            return basicData
            
            
        except (Exception) as error : #If Basic data collection fails, continue with whatever is collected
            print("ERROR: Failed to read Basic data for url : ", self.url ,error)
            
        return basicData
        
 
# bscS = BasicsScrapper("https://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/pageindustries/PI35")
# print(bscS.readPage())
