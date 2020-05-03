#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:10:24 2020

@author: sharvarinagesh
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from Util import to_float

class FinancialScrapper :
    
    def __init__(self, url):
        self.url = url

    def getFinancialTable(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')  #pass the page content through BeautifulSoup
        table = soup.find("table", class_="mctable1")   # All the financial data is in the table "mctable1"
        return table

    def readPage(self):
        self.table = self.getFinancialTable()
        return self.readTable()
    
    def readYears(self, header_tds):
        i=0
        years =[]
        #Reading the years from the first row of the data
        for td in header_tds:
            if i==0:
                i = i+1
                continue
            if(td.has_attr('class')):  # rows with class has no data in it. so skip
                break;
            
            year = td.text
            years.append(year)
            i = i+1

        return years
        
    def readTable(self):
        trs = self.table.find_all("tr")  #  Get all <tr> tags in the table
        header_tds = trs[0].find_all("td")  #This tells what kind of financial statement is it and the years(eg: Mar19, Mar18 etc)
        financial_data_header =  header_tds[0].text #financial statement header. Eg profit& Loss, balance sheet etc. 
        years =self.readYears(header_tds)  #Forming an array of years, which will be column names
        
        financial_data = {'Year' : years}
        # getting the years for which the financial data is present. And making separate dictionaries for each year.
        
        # First two rows are header and empty. So removing them
        del(trs[0])
        del(trs[0])
        # Reading each row of data
        for tr in trs:
            if(tr.has_attr('class') & ("darkbg" in tr['class'] )):
                continue    
    
            tds = tr.find_all("td")
            column = tds[0].text.title()
            column = re.sub('\s+\/\s+','/', column)
            del(tds[0])
            
            for td in tds:
                if(td.has_attr('class')):
                    break;

                if(not column in financial_data.keys()):
                    financial_data[column]=[]
                
                financial_data[column].append(to_float(td.text))
                
        # Ref: https://stackoverflow.com/questions/18837262/convert-python-dict-into-a-dataframe/32344037#32344037
        
        # financial_df = pd.DataFrame.from_dict(financial_data,orient='index',columns=years)
        financial_df = pd.DataFrame(financial_data)
        # print(financial_df)
        return financial_df


# URL = 'http://www.moneycontrol.com/financials/bosch/profit-lossVI/B05' #Quarterly result of page industries\
# URL='https://www.moneycontrol.com/financials/relaxofootwears/ratiosVI/RF07#RF07'
# fc = FinancialScrapper(URL)
# fin_data = fc.readPage()
# # print(fin_data.info())
# print(fin_data.head(20))


