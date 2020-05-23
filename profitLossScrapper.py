#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:10:24 2020

@author: sharvarinagesh
"""
import scrapper as sc
import pandas as pd

class ProfitLossScrapper :
    # URL = 'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05' #Quarterly result of page industries\
    COLUMNS_NEEDED = ['Year','Total Operating Revenues','Total Revenue','Finance Costs','Depreciation And Amortisation Expenses','Total Expenses','Profit/Loss Before Tax','Current Tax','Profit/Loss For The Period','Basic Eps (Rs.)','Equity Share Dividend']
    def __init__(self,url):
        self.UrlList = url
        
        
    def callScrapper(self, url):
        fsc = sc.FinancialScrapper(url)
        return fsc.readPage()   


    def readPL(self):
        try :
            finData = self.callScrapper(self.UrlList['consolidated'])
        except :
            print("Exception occurred while reading:", self.UrlList['consolidated'] )
            print("Attempting to read Standalone statement")
            try:
                finData = self.callScrapper(self.UrlList['standalone'])
            except:
                 print("WARNING!: Data could not be extracted for :", self.UrlList)
                 raise Exception("ERROR: Profit & Loss data collection failed. Tried both Consolidated and Standalone")

        pd.set_option('display.max_columns', None)
        pl = None
        
        pl = finData[self.COLUMNS_NEEDED]
        pl.set_index("Year",inplace = True)
       
        return pl
    
# url='http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05'
# url= {'standalone':'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05', 'consolidated':'https://www.moneycontrol.com/financials/bosch/consolidated-profit-lossVI/B05#B05'}
# url= {'standalone':'http://www.moneycontrol.com/financials/nestleindia/profit-lossVI/NI#NI','consolidated':'https://www.moneycontrol.com/financials/nestleindia/consolidated-profit-lossVI/NI#NI'}
# # # url= {'standalone':'https://www.moneycontrol.com/financials/nestleindia/consolidated-profit-lossVI/NI#NI','consolidated':'https://www.moneycontrol.com/financials/nestleindia/consolidated-profit-lossVI/NI#NI'}
# pls = ProfitLossScrapper(url)
# pl = pls.readPL()
# print(pl)