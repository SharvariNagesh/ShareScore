#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:09:47 2020

@author: sharvarinagesh
"""
import sys
import BasicsScrapper
import pathlib
import csv
import Navigator
import profitLossScrapper
import BalanceSheetScrapper
import RatioScrapper
import pandas as pd
import Scorer
import Util
import DBWriter


def updateBasicData(basicSheet, finData):
    
    avgScore = finData["Score"].mean()
    highestScore = finData['Score'].max()
    epsCagr = Util.cagr(finData.iloc[-1]['Basic Eps (Rs.)'], finData.iloc[0]['Basic Eps (Rs.)'], len(finData) - 1)
    netProfitCagr = Util.cagr(finData.iloc[-1]['Profit/Loss For The Period'], finData.iloc[0]['Profit/Loss For The Period'], len(finData) - 1)
    basicSheet["Avg Score"]= avgScore
    basicSheet["Highest Score"]= highestScore    
    basicSheet["EPS CAGR"]= epsCagr
    basicSheet["NetProfit CAGR"] = netProfitCagr
    return basicSheet    
    
def readFinancialData(nav,basicSheet):
    
    balancedata = BalanceSheetScrapper.BalanceSheetScrapper(nav['BalanceSheet']).readBalanceSheet()
    print("Balance Sheet processed")
    
    pldata = profitLossScrapper.ProfitLossScrapper(nav['ProfitLoss']).readPL()
    print("Profit & Loss Sheet processed")
    
    ratiodata = RatioScrapper.RatoiSheetScrapper(nav['RatioSheet']).readSheet()
    print("Ratio Sheet processed")
    frames = [balancedata, pldata, ratiodata]
    finData = pd.concat(frames,sort=False,axis=1,)
    finData.insert(loc=0,column='Company Name', value=(basicSheet['name'] * len(finData)))
    finData.reset_index( inplace = True)
    finData.set_index(["Company Name","Year"],inplace = True)
    finDataWithScore = Scorer.Scorer(basicSheet, finData).calculate() 
    return finDataWithScore
  

def writeToFile(basicSheet, finData):
    print("Writing Fin Data")
    if( pathlib.Path("financial_data.csv").exists()):
        finData.to_csv (r'financial_data.csv' , mode='a', header=False)
    else:
        finData.to_csv (r'financial_data.csv' , mode='a',header=True)        
    
# writing a dictionary to a file
# Ref : https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in dict_data:
#             writer.writerow(data)
# except IOError:
#     print("I/O error")
    
def writeData(basicSheet, finData):
   
    writeToFile(basicSheet, finData)
    
    dbWriter = DBWriter.DBWriter()
    dbWriter.basicDataToDB(basicSheet)
    dbWriter.finDataToDB(finData)
    
print("Enter URL to process :")

while True:
    data = input("Please enter the company URL:\n")
    if 'exit' == data.lower():
        print("Breaking")
        break
    print("Processing:", data)
    nav = Navigator.Navigator(data).getFinancialUrls()
    print(nav)
    basicSheet = BasicsScrapper.BasicsScrapper(nav['Basic']).readPage()
    print("Basic Sheet processed")
    finData = readFinancialData(nav,basicSheet)
    basicSheet = updateBasicData(basicSheet, finData)
    
    print(basicSheet)
    print(finData)
    writeData(basicSheet, finData)