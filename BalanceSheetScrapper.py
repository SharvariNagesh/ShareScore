#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:36:24 2020

@author: sharvarinagesh
"""

import scrapper as sc
import pandas as pd
from FinancialSheetScrapper import FinancialSheetScrapper

class BalanceSheetScrapper(FinancialSheetScrapper):
    COLUMNS_NEEDED = ['Year','Equity Share Capital','Reserves And Surplus','Total Shareholders Funds','Total Non-Current Liabilities','Total Current Liabilities','Total Capital And Liabilities', 'Total Current Assets','Total Assets']
    def __init__(self,url, readStandalone):
        FinancialSheetScrapper.__init__(self)
        self.UrlList = url
        self.ReadStandalone = readStandalone
        
    def readBalanceSheet(self):
        finData = super().readFinancialSheet( self.UrlList, self.ReadStandalone)
        balanceSheet = finData[self.COLUMNS_NEEDED]
        balanceSheet.set_index("Year",inplace = True)
        return balanceSheet



# print("Hello")
# url= {'standalone':'https://www.moneycontrol.com/financials/nestleindia/balance-sheetVI/NI#NI', 'consolidated':'https://www.moneycontrol.com/financials/nestleindia/consolidated-balance-sheetVI/NI#NI'}
# # url= {'standalone':'https://www.moneycontrol.com/financials/monsantoindia/balance-sheetVI/MI39#MI39', 'consolidated':'https://www.moneycontrol.com/financials/monsantoindia/consolidated-balance-sheetVI/MI39#MI39'}

# pls = BalanceSheetScrapper(url, True)
# pl = pls.readBalanceSheet()
# print(pl)