#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:01:44 2020

@author: sharvarinagesh
"""




import scrapper as sc
import pandas as pd
from Util import ffmt


class RatoiSheetScrapper :
    # URL = 'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05' #Quarterly result of page industries\
    COLUMNS_NEEDED = ['Year','Pbdit Margin (%)','Net Profit Margin (%)','Return On Networth/Equity (%)','Return On Capital Employed (%)','Total Debt/Equity (X)','Current Ratio (X)','Dividend Payout Ratio (Np) (%)','Earnings Retention Ratio (%)']
    def __init__(self,url):
        self.na = url
        
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
    
    def pbditMargin(self,plrow):
        
        pbdit = plrow['Profit/Loss Before Tax'] + plrow['Finance Costs']+plrow['Depreciation And Amortisation Expenses']
        if(plrow['Total Operating Revenues'] == 0):
            return 0
        else :
            return ffmt((pbdit/ plrow['Total Operating Revenues']) * 100)
        
      
    def netProfitMargin(self,plrow):
        if (plrow['Total Revenue'] == 0) :
            return 0 
        else:
            return ffmt((plrow['Profit/Loss For The Period']/plrow['Total Revenue']) *100 )
        
            

    # Reference : https://strategiccfo.com/roe-return-on-equity/
    def roe(self,plrow, balancerow):
        if (balancerow['Total Shareholders Funds'] == 0) :
            return 0 
        else:
            return ffmt((plrow['Profit/Loss For The Period']/balancerow['Total Shareholders Funds']) * 100)
        
    
    # Reference: https://strategiccfo.com/roce/
    def roce(self, plrow, balancerow):
        ebit = plrow['Profit/Loss Before Tax']+ plrow['Finance Costs']
        capitalEmployed = balancerow['Total Assets'] - balancerow['Total Current Liabilities']
        return 0 if(capitalEmployed == 0) else ffmt(ebit/capitalEmployed * 100)
        
    
    #Reference: https://www.investopedia.com/terms/d/debtequityratio.asp
    # https://www.investopedia.com/ask/answers/070615/how-do-you-calculate-shareholder-equity.asp
    def debtToEquity(self, balancerow):
        totalLiabilities = balancerow['Total Non-Current Liabilities'] + balancerow['Total Current Liabilities']
        shareholdersEquity = balancerow['Total Shareholders Funds']
        return 0 if(shareholdersEquity ==0) else ffmt(totalLiabilities / shareholdersEquity)


    #Reference: https://www.investopedia.com/terms/c/currentratio.asp
    def currentRatio(self, balancerow):
        return 0 if(balancerow['Total Current Liabilities'] ==0) else ffmt((balancerow['Total Current Assets']/ balancerow['Total Current Liabilities']))
        
 
    #Reference: https://www.investopedia.com/terms/d/dividendpayoutratio.asp
    def dividendPayoutRatio(self,plrow):
        return 0 if(plrow['Profit/Loss For The Period'] ==0) else ffmt(plrow['Equity Share Dividend']/plrow['Profit/Loss For The Period'] * 100)
        
        
    #Reference: https://www.investopedia.com/terms/r/retentionratio.asp
    def earningsRetentionRatio(self,plrow):
        return 0 if(plrow['Profit/Loss For The Period'] ==0) else ffmt((plrow['Profit/Loss For The Period'] -plrow['Equity Share Dividend'])/plrow['Profit/Loss For The Period'] * 100)
    
    def calculateRatio(self,balancedata, pldata):
        ratio = {'Pbdit Margin (%)':[],'Net Profit Margin (%)':[],'Return On Networth/Equity (%)':[],'Return On Capital Employed (%)':[],'Total Debt/Equity (X)':[],'Current Ratio (X)':[],'Dividend Payout Ratio (Np) (%)':[],'Earnings Retention Ratio (%)':[]}
        Year =[]
        if(len(balancedata) != len(pldata)):
            print("ERROR : balancesheet data and P&L data does not match!" )
            raise Exception("ERROR: Ratio data calculation failed. Balance sheet data and P&L data are not of same length")
        for row in balancedata.index :
            Year.append(row)
            plrow = pldata.loc[row].astype(float)
            balancerow = balancedata.loc[row].astype(float)
            ratio['Pbdit Margin (%)'].append( self.pbditMargin(plrow))
            ratio['Net Profit Margin (%)'].append(self.netProfitMargin(plrow))
            ratio['Return On Networth/Equity (%)'].append(self.roe(plrow,balancerow))
            ratio['Return On Capital Employed (%)'].append(self.roce(plrow, balancerow))
            ratio['Total Debt/Equity (X)'].append(self.debtToEquity(balancerow))
            ratio['Current Ratio (X)'].append(self.currentRatio(balancerow))
            ratio['Dividend Payout Ratio (Np) (%)'].append(self.dividendPayoutRatio(plrow))
            ratio['Earnings Retention Ratio (%)'].append(self.earningsRetentionRatio(plrow))
        
        ratioDf = pd.DataFrame(ratio, index=Year, dtype=float)
        # ratioDf.set_index("Year",inplace = True)
        return ratioDf
        
# url= {
#         "standalone": "https://www.moneycontrol.com/financials/relaxofootwears/ratiosVI/RF07#RF07",
#         "consolidated": "https://www.moneycontrol.com/financials/relaxofootwears/ratiosVI/RF07#RF07"
#     }
# pls = RatoiSheetScrapper(url)
# try:
#     pl = pls.readSheet()
#     print(pl)
# except:
#     print("Need to calculate ratios")