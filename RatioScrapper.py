#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:01:44 2020

@author: sharvarinagesh
"""




import scrapper as sc
import pandas as pd

class RatoiSheetScrapper :
    # URL = 'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05' #Quarterly result of page industries\
    COLUMNS_NEEDED = ['Year','Pbdit Margin (%)','Net Profit Margin (%)','Return On Networth/Equity (%)','Return On Capital Employed (%)','Total Debt/Equity (X)','Current Ratio (X)','Dividend Payout Ratio (Np) (%)','Earnings Retention Ratio (%)']
    def __init__(self,url):
        self.UrlList = url
        
    def callScrapper(self, url):
        fsc = sc.FinancialScrapper(url)
        return fsc.readPage()   

    def readSheet(self):
        finData = pd.DataFrame()
        try :
            finData = self.callScrapper(self.UrlList['consolidated'])
        except :
            print("Exception occurred while reading:", self.UrlList['consolidated'] )
            print("Attempting to read Standalone statement")
            try:
                finData = self.callScrapper(self.UrlList['standalone'])
            except:
                print("WARNING!: Data could not be extracted for :", self.UrlList)
                raise Exception("ERROR: Ratio sheet data collection failed. Tried both Consolidated and Standalone")
        pd.set_option('display.max_columns', None)
        ratio = finData[self.COLUMNS_NEEDED]
        ratio.set_index("Year",inplace = True)
        return ratio



# url= {
#         "standalone": "https://www.moneycontrol.com/financials/relaxofootwears/ratiosVI/RF07#RF07",
#         "consolidated": "https://www.moneycontrol.com/financials/relaxofootwears/ratiosVI/RF07#RF07"
#     }
# pls = RatoiSheetScrapper(url)
# pl = pls.readSheet()
# print(pl)