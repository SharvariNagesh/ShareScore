#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:13:11 2020

@author: sharvarinagesh
"""
import psycopg2
import numpy
from psycopg2.extensions import register_adapter, AsIs

class DBWriter:
    connection = None

    def __init__(self):
        self.dbConnect()

    def __del__(self):
        if(self.connection is not None):
            # self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
        register_adapter(numpy.float64, self.addapt_numpy_float64)
        register_adapter(numpy.int64, self.addapt_numpy_int64)
        
        
    # psycopg2 had some issue with writing np.int64 into the DB. so the below 2 functions and registering adapter in the 
    # constructor is a fix for that problem
    # Ref: https://stackoverflow.com/questions/50626058/psycopg2-cant-adapt-type-numpy-int64
    def addapt_numpy_float64(self, numpy_float64):
        return AsIs(numpy_float64)


    def addapt_numpy_int64(self, numpy_int64):
        return AsIs(numpy_int64)
    
    
    def dbConnect(self):
        try:
            self.connection = psycopg2.connect(database ="sharescore", user = "share_user", password = "share123", host = "127.0.0.1", port = "5432") 
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to connect to DB : ", error)
        
    def insert(self,postgresQyery, recordToInsert):   
        try:
            if(not self.connection):
                
                "ERROR: DB CONNECTION IS NOT LIVE!"
                return None
            
            self.cursor.execute(postgresQyery, recordToInsert)

            self.connection.commit()
            count = self.cursor.rowcount
            print (count, "Record inserted successfully into the table")

        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to insert record into the table", error)
                print("Query : ", postgresQyery)

        
    def basicDataToDB(self, bD):
        postgresQyery = """ INSERT INTO sharebasic (name, avg_score, high_score, eps_cagr, netprofit_cagr, company_overview, price, low52, high52, sector, market_cap, pe, book_value, dividend, industry_pe, eps, pc, price_to_book, dividend_yield, face_value, url) VALUES (%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s)"""
        recordToInsert = (bD['name'],bD['Avg Score'],bD['Highest Score'],bD['EPS CAGR'],bD["NetProfit CAGR"],bD['Company Overview'],bD['price'],bD['52low'], bD['52high'], bD['sector'],bD['Market Cap (Rs Cr.)'],bD['P/E'],bD['Book Value (Rs)'],bD['Dividend (%)'],bD['Industry P/E'],bD['EPS (TTM)'],bD['P/C'],bD['Price/Book'],bD['Dividend Yield.(%)'],bD['Face Value (RS)'],bD['url'])
        self.insert(postgresQyery, recordToInsert)
        
    def finDataToDB(self, financiaData):
        for i in range(len(financiaData)):
            fD = financiaData.iloc[[i]]
            fD.reset_index(inplace = True)
            postgresQyery = """ INSERT INTO financialdata (company_name, year, share_capital, reserves, total_shareholders_fund, total_noncurrent_liability, total_current_liabilities, total_capital_and_liabilities, total_revenue, total_expenses, profit_loss_before_tax, current_tax, profit_loss_for_the_period, basic_eps, equity_share_dividend, pbdit_margin, net_profit_margin, roe, rotc, debt_to_equity, current_ratio, dividend_payout_ratio, earnings_retention_ratio, score, score_summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            recordToInsert = (fD["Company Name"].values[0], fD["Year"].values[0], fD["Equity Share Capital"].values[0], fD["Reserves And Surplus"].values[0], fD["Total Shareholders Funds"].values[0],  \
                              fD["Total Non-Current Liabilities"].values[0], fD["Total Current Liabilities"].values[0], fD["Total Capital And Liabilities"].values[0], fD["Total Revenue"].values[0],  \
                              fD["Total Expenses"].values[0], fD["Profit/Loss Before Tax"].values[0], fD["Current Tax"].values[0], fD["Profit/Loss For The Period"].values[0], fD["Basic Eps (Rs.)"].values[0], \
                              fD["Equity Share Dividend"].values[0], fD["Pbdit Margin (%)"].values[0], fD["Net Profit Margin (%)"].values[0], fD["Return On Networth/Equity (%)"].values[0],  \
                              fD["Return On Capital Employed (%)"].values[0], fD["Total Debt/Equity (X)"].values[0], fD["Current Ratio (X)"].values[0], fD["Dividend Payout Ratio (Np) (%)"].values[0], \
                              fD["Earnings Retention Ratio (%)"].values[0], fD["Score"].values[0], fD["Score Summary"].values[0])
            self.insert(postgresQyery, recordToInsert)

# basicData = {'name': 'Bosch Ltd.', 'url': 'https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/bosch/B05', 'price': 9916.4, '52low': 7874.0, '52high': 18133.2, 'sector': 'Auto Ancillaries', 'Company Overview': 'Bosch Ltd is Indias largest auto component manufacturer.The company`s activities can be classified under the following divisions Automotive Technology i.e. Diesel and Gasoline Fuel Injection Systems, Blaupunkt Car Multimedia Systems, Auto Electricals and Accessories, Starters and Motors, Energy and Body Systems;Industrial Technology i.e.Packaging Machines, & Special Purpose Machines and Consumer Goods and Building Technology i.e.Power Tools, Security Systems,etc.The company also in the business activities of Automotive Product.', 'Market Cap (Rs Cr.)': 29214.78, 'P/E': 29.83, 'Book Value (Rs)': 3091.44, 'Dividend (%)': 1050.0, 'Industry P/E': 15.69, 'EPS (TTM)': 332.42, 'P/C': 21.09, 'Price/Book': 3.2, 'Dividend Yield.(%)': 1.06, 'Face Value (RS)': 10.0, 'Avg Score': 1000, 'Highest Score': 1050, 'EPS CAGR': 10.2, 'NetProfit CAGR' : 11.2}
# dbWriter = DBWriter().basicDataToDB(basicData)