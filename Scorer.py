#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:58:16 2020

@author: sharvarinagesh
"""



import scrapper as sc
import pandas as pd
import enums
from enums import ROEnum, OperatingMargin,DebtToNetProfit,NetProfitMargin,CurrentRatio

class Scorer :
  
    def __init__(self, basic, financialData):
        self.basic = basic
        self.financialData = financialData
        self.shareCountScore = None
        self.scoreBG = None
    
    #If number of shares has reduced or company has bought back shares, give a score of 100
    # If there is no change in share, no points
    # If the company has issued more shares, then reduce 100 
    def shareCountReductionCheck(self):
        if(self.shareCountScore is not None):
            return self.shareCountScore 
        equityCapitalChange = (self.financialData.iloc[-1]['Equity Share Capital']) - (self.financialData.iloc[0]['Equity Share Capital'])
        if(equityCapitalChange>0):
            self.shareCountScore = 100
        elif(equityCapitalChange == 0):
            self.shareCountScore = 0
        else:
            self.shareCountScore = -100
        return self.shareCountScore 
    
    #Check if NetProfit is increasing YOY. For every year the net profit has increased, we add 50 points
    def calculateFromBusinessGrowth(self):
        if(self.scoreBG is not None):
            return self.scoreBG 
        lenOfDf = len(self.financialData) - 1
        self.scoreBG = 0
        while(lenOfDf > 0):
            netProfitPrev = self.financialData.iloc[lenOfDf]['Profit/Loss For The Period']
            netProfit=self.financialData.iloc[lenOfDf -1]['Profit/Loss For The Period']
            lenOfDf = lenOfDf - 1
            if(netProfit > netProfitPrev):
                self.scoreBG = self.scoreBG + 50
        return self.scoreBG
    
    #Calculates the score of the company
    def calculate(self):
        
        self.score = 0
        # print(self.financialData.to_dict(orient='records'))
        # for row_dict in self.financialData.to_dict(orient='records'):
        #     print(row_dict)
        self.scoreList=[]
        for i in range(len(self.financialData)):
            row = self.financialData.iloc[[i]]
            
            scoreROE = enums.getScore(ROEnum, row['Return On Networth/Equity (%)'].values[0]) #ROE
            # comment = ""
            scoreROTC = enums.getScore(ROEnum, row['Return On Capital Employed (%)'].values[0]) #ROTC
            scoreOM =  enums.getScore(OperatingMargin, row['Pbdit Margin (%)'].values[0]) #Operating profit margin
            scoreNM =  enums.getScore(NetProfitMargin, row['Net Profit Margin (%)'].values[0]) #Net profit margin
            scoreCR =  enums.getScore(CurrentRatio, row['Current Ratio (X)'].values[0]) #Current ratio check
            debtToNetProfit = row['Total Non-Current Liabilities'].values[0] / row['Profit/Loss For The Period'].values[0]
            scoreDTNP = 0
            if(debtToNetProfit < 0 ): #Company is making loss
                scoreDTNP = -100
            else:
                scoreDTNP =  enums.getScore(DebtToNetProfit, debtToNetProfit) #Debt to Net profit ratio
            scoreSC = self.shareCountReductionCheck() 
            scoreBG = self.calculateFromBusinessGrowth()
            score = scoreROE + scoreROTC + scoreOM + scoreNM + scoreCR + scoreDTNP + scoreSC + scoreBG
            scoreSummary = "ROE Score : " + str(scoreROE) + \
                    "\n ROTC Score: " + str(scoreROTC) + \
                    "\n Operation Margin score: " + str(scoreOM) +\
                    "\n Net Profit Margin Score: " + str(scoreNM) + \
                    "\n Current Ratio score: " + str(scoreCR) +\
                    "\n Debt to NetProfit : " + str(debtToNetProfit) + " and Score: " + str(scoreDTNP) +\
                    "\n Share Count Reduction Check score : " + str(scoreSC) +\
                    "\n Business Growth score: " + str(scoreBG) + \
                    "\n TOTAL SCORE: " + str(score)
            self.scoreList.append({ "Score" : score, "Score Summary" : scoreSummary})
        scoreListDf = pd.DataFrame(self.scoreList, index = self.financialData.index.values.tolist())
        finDataWithScore = pd.concat([self.financialData, scoreListDf], axis=1, sort=False)
        # print(finDataWithScore)
        return finDataWithScore
        
        
# print("Hello")
# basic = {'x' : 23, 'y':45}
# fin = {'Pbdit Margin (%)':[14.71,15.79,14.99,14.20,13.57], 
#         'Net Profit Margin (%)':[7.65,8.29,7.35,7.02,6.95],
#         'Return On Networth/Equity (%)': [15.87,21.15,19.78,25.05,28.01], 
#         'Return On Capital Employed (%)': [23.93,30.20,27.17,18.92,18.85],
#         'Total Debt/Equity (X)':[0.08,0.16,0.22,0.42,0.57],
#         'Current Ratio (X)': [1.58,1.35,1.24,1.16,1.20],
#         'Total Non-Current Liabilities':[43.45,73.76,104.10,155.51,178.79],
#         'Profit/Loss For The Period' :[175.44,161.07,119.95,120.28,103.05],
#         'Equity Share Capital':[12.40,12.03,12.01,12.00,6.00]
#         }
# index = ['Mar19','Mar18','Mar17','Mar16','Mar15']
# finData = pd.DataFrame(fin, index = index)
# scorer = Scorer(basic, finData).calculate()
# print(scorer)