#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:21:06 2020

@author: sharvarinagesh

This file defines scoring criteria for various parameters

Ref: https://docs.python.org/3/library/enum.html
"""


from enum import IntEnum, Enum 

# creating enumerations using class 
class ROEnum(IntEnum): 
    class0 = 12
    class1 = 15
    class2 = 20
    class3 = 25
    
    def check(self, value):
        return (value >= self.value)
        
    
class OperatingMargin(IntEnum): 
    class0 = 12
    class1 = 20
    class2 = 30
    class3 = 45
    
    def check(self, value):
        return (value >= self.value)

class NetProfitMargin(IntEnum): 
    class0 = 7
    class1 = 12
    class2 = 18
    class3 = 25
    
    def check(self, value):
        return (value >= self.value)
    
# class CurrentRatio(IntEnum):
#     class0 = 0
#     class1 = 2
#     class2 = 5
#     class3 = 10
    
#     def check(self, value):
#         return (value > (self.value))
    
class DebtToNetProfit(IntEnum):
    class0 = 15
    class1 = 10
    class2 = 5
    class3 = 1
    
    def check(self, value):
        return(value <= self.value)


    
def getScore(enumObj, actualValue):
    score = 0
    for classNo in enumObj :
        if(  classNo.check(actualValue)):
            score = score + 50
        else:
            return score
    return score
        # print(classNo," = ", classNo.value)

# score = getScore(ROEnum, 20)
# print("ROEnum Score = ", score)

# score = getScore(DebtToEquity, 0.3)
# print("DebtToEquity Score = ", score)



