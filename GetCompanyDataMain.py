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
import time
from Util import to_float


#Formula : Value(V) = [EPS x ( 8.5 + 2G) x 4.4 ] /Y 
#"Here EPS is earnings per share. 
#G is growth of Sales
#4.4 is bond output at 1964. We will keep it like that for now
#Y is current 10 year bond yield
#eg: say eps is 30 and sales growth is 7.5% and 10 bond yield in india is 8.85 then value of the company is:
#V = [30 x (8.5 + (2 x 7.5) x 4.4]/ 8.85 = "
def calculateIntrinsicValue(basicSheet):
    bondYield = 6.23
    eps= float(to_float(basicSheet['EPS (TTM)']))
    growth = float( to_float(basicSheet['Sales CAGR']))
    avgPE = float(15)
    bondOP = 4.4
    
    intrinsicValue = (eps * (avgPE + (2 * growth)) * bondOP )/bondYield
    return intrinsicValue
    
def updateBasicData(basicSheet, finData):
    
    avgScore = finData["Score"].mean()
    roce = finData["Return On Capital Employed (%)"].mean()
    roe  = finData["Return On Networth/Equity (%)"].mean()
    highestScore = finData['Score'].max()
    epsCagr = Util.cagr(finData.iloc[-1]['Basic Eps (Rs.)'], finData.iloc[0]['Basic Eps (Rs.)'], len(finData) - 1)
    netProfitCagr = Util.cagr(finData.iloc[-1]['Profit/Loss For The Period'], finData.iloc[0]['Profit/Loss For The Period'], len(finData) - 1)
    salesCagr = Util.cagr(finData.iloc[-1]['Total Revenue'], finData.iloc[0]['Total Revenue'], len(finData) - 1)
    basicSheet["Avg Score"]= avgScore
    basicSheet["Highest Score"]= highestScore    
    basicSheet["EPS CAGR"]= epsCagr
    basicSheet["NetProfit CAGR"] = netProfitCagr
    basicSheet["Sales CAGR"] = salesCagr
    basicSheet["ROE"] = round(roe, 2)
    basicSheet["ROCE"] = round(roce, 2)
    basicSheet["IntrinsicValue"] = calculateIntrinsicValue(basicSheet)
    return basicSheet    
    
def readFinancialData(nav,basicSheet, readStandalone):
    
    balancedata = BalanceSheetScrapper.BalanceSheetScrapper(nav['BalanceSheet'],readStandalone).readBalanceSheet()
    print("Balance Sheet processed")
    
    pldata = profitLossScrapper.ProfitLossScrapper(nav['ProfitLoss'], readStandalone).readPL()   
    print("Profit & Loss Sheet processed")
    
    ratiodata = None
    ratioScrapper = RatioScrapper.RatoiSheetScrapper(nav['RatioSheet'])
    # try:
    #     ratiodata = ratioScrapper.readSheet()
    #     print("Ratio Sheet processed")
    # except :
    ratiodata = ratioScrapper.calculateRatio(balancedata, pldata)
    frames = [balancedata, pldata, ratiodata]
    finData = pd.concat(frames,sort=False,axis=1,).astype(float)
    finData.insert(loc=0,column='Company Name', value=(basicSheet['name']))
    finData.reset_index( inplace = True)
    finData.set_index(["Company Name","Year"],inplace = True)
    finDataWithScore = Scorer.Scorer(basicSheet, finData).calculate() 
    return finDataWithScore
  

def writeToFile(basicSheet, finData):
    # print("Writing Fin Data")
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
    dbWriter.basicDataToDB(basicSheet)
    dbWriter.finDataToDB(finData)

def processUrl(data, readStandalone):
    nav = Navigator.Navigator(data).getFinancialUrls()
    basicSheet = BasicsScrapper.BasicsScrapper(nav['Basic']).readPage()
    # print("Basic Sheet processed")
    finData = readFinancialData(nav,basicSheet, readStandalone)
    if(not finData is None):
        basicSheet = updateBasicData(basicSheet, finData)
        writeData(basicSheet, finData)
        print("finished processing ", data)
        time.sleep(5)
    
#If command line parameters are passed, the program reads from the file.    
#Usage: python <Python file> file <company list file>
# If no command line is passed, then it reads urls from command line
pd.set_option('display.max_columns', None)
dbWriter = DBWriter.DBWriter()
if(len(sys.argv)>1 and sys.argv[1].lower() == 'file'):
    try:
        file = open(sys.argv[2], 'r') 
        lines = file.readlines() 
    except (Exception) as error :
        print("ERROR: Failed to read the data from: " ,error)
        sys.exit()
        
    for line in lines: 
        try:   
            data = line.strip()
            print("Processing:", data)
            processUrl(data, True)
        except (Exception) as error :
            print("ERROR: Failed to process the data from: ", data,error)
   
else:
    print("Enter URL to process :")
    
    while True:
        try: 
            data = input("Please enter the company URL:\n")
            if 'exit' == data.lower():
                print("Exiting from the code")
                break
            readStandalone = input("Read Only Standalone? (y/n):\n")
            if 'y' == readStandalone.lower():
                print("Reading Standalone data")
                readStandalone = True
            else:
                print("Reading Consolidated data")
                readStandalone = False
            processUrl(data, readStandalone)
        except (Exception) as error :
            print("ERROR: Failed to process the data from: ", data,error)

   