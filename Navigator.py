#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:57:05 2020

@author: sharvarinagesh
"""


from selenium import webdriver
import json
import pprint

class Navigator :
    
    def __init__(self, url):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors') 
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome("/Users/sharvarinagesh/Technical/Python/webscrap/chromedriver", options=options)

        
    def getConsolidatedUrl(self, standaloneUrl):
        self.driver.get(standaloneUrl)
        consolidatedUrl = self.driver.find_element_by_link_text("Consolidated").get_attribute("href")
        return consolidatedUrl
    
    def getFinancialUrls(self):
        self.driver.get(self.url)
        balanceSheetUrl = self.driver.find_element_by_css_selector("[title='Balance Sheet']").get_attribute("href")
        profitLossUrl = self.driver.find_element_by_css_selector("[title='Profit & Loss']").get_attribute("href")
        ratioUrl = self.driver.find_element_by_css_selector("[title='Ratios']").get_attribute("href")
        # ratioUrl = self.driver.find_element_by_link_text("Ratios").get_attribute("href")# Somehow this is not working
        # print(ratioUrl)
        # ratiosUrl = driver.find_element_by_xpath('//*[@title="Ratios"]').get_attribute("href")
        consolidatedBalanceSheet = self.getConsolidatedUrl(balanceSheetUrl)
        # print('Consolidated balance sheet:', consolidatedBalanceSheet)
        consolidatedProfitLossSheet = self.getConsolidatedUrl(profitLossUrl)
        # print('Consolidated profit loss sheet:', consolidatedProfitLossSheet)
        consolidatedRatioSheet = self.getConsolidatedUrl(ratioUrl)
        urlList ={"Basic":self.url, 
                  "BalanceSheet":{"standalone":balanceSheetUrl, "consolidated":consolidatedBalanceSheet}, 
                  "ProfitLoss":{"standalone":profitLossUrl, "consolidated":consolidatedProfitLossSheet},
                  "RatioSheet":{"standalone" : ratioUrl, "consolidated":consolidatedRatioSheet }}
        # pprint.pprint(urlList)
        return urlList
        #Amara raja battery doesn't have much financial data in consolidated form. So just to get data for all the years, i did this below code
        # url = {
        #     "Basic": "https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/amararajabatteries/ARB",
        #     "BalanceSheet": {
        #         "standalone": "http://www.moneycontrol.com/financials/amararajabatteries/balance-sheetVI/ARB#ARB",
        #         "consolidated": "http://www.moneycontrol.com/financials/amararajabatteries/balance-sheetVI/ARB#ARB"
        #     },
        #     "ProfitLoss": {
        #         "standalone": "http://www.moneycontrol.com/financials/amararajabatteries/profit-lossVI/ARB#ARB",
        #         "consolidated": "http://www.moneycontrol.com/financials/amararajabatteries/profit-lossVI/ARB#ARB"
        #     },
        #     "RatioSheet": {
        #         "standalone": "http://www.moneycontrol.com/financials/amararajabatteries/ratiosVI/ARB#ARB",
        #         "consolidated": "http://www.moneycontrol.com/financials/amararajabatteries/ratiosVI/ARB#ARB"
        #     }
        # }
        # return url
    

# url="https://www.moneycontrol.com/india/stockpricequote/auto-ancillaries/amararajabatteries/ARB"
# urls = Navigator(url).getFinancialUrls()

# # print(json.dumps(urls,indent=3))
# pprint.pprint(urls, width=1)
# print(json.dumps(urls, indent=4))