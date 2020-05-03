#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:36:24 2020

@author: sharvarinagesh
"""

import scrapper as sc
import pandas as pd

class BalanceSheetScrapper :
    # URL = 'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05' #Quarterly result of page industries\
    COLUMNS_NEEDED = ['Year','Equity Share Capital','Reserves And Surplus','Total Shareholders Funds','Total Non-Current Liabilities','Total Current Liabilities','Total Capital And Liabilities']
    def __init__(self,url):
        self.UrlList = url
        
    def callScrapper(self, url):
        fsc = sc.FinancialScrapper(url)
        return fsc.readPage()   

    def readBalanceSheet(self):
        try :
            finData = self.callScrapper(self.UrlList['consolidated'])
        except :
            print("Exception occurred while reading:", self.UrlList['consolidated'] )
            print("Attempting to read Standalone statement")
            try:
                finData = self.callScrapper(self.UrlList['standalone'])
            except:
                print("WARNING!: Data could not be extracted for :", self.UrlList)
                finData = {}
                return finData
        pd.set_option('display.max_columns', None)
        # print(finData.columns)
        balanceSheet = finData[self.COLUMNS_NEEDED]
        # ShareCapitalChange = (pl.iloc[-1]['Equity Share Capital']) - (pl.loc[0]['Equity Share Capital'])
        # pl['Share Capital Change'] = ShareCapitalChange
        balanceSheet.set_index("Year",inplace = True)
        return balanceSheet



# print("Hello")
# url= {'standalone':'https://www.moneycontrol.com/financials/nestleindia/balance-sheetVI/NI#NI', 'consolidated':'https://www.moneycontrol.com/financials/nestleindia/consolidated-balance-sheetVI/NI#NI'}
# pls = BalanceSheetScrapper(url)
# pl = pls.readBalanceSheet()
# print(pl)