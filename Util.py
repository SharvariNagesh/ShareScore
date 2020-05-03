#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:26:01 2020

@author: sharvarinagesh
"""

import re

def to_float(stringFloat):
    if re.findall("\d", stringFloat):
        value = float(re.sub(',','',stringFloat))
    else: 
        value = float(0)
    return value

# Reference: https://feliperego.github.io/blog/2016/08/10/CAGR-Function-In-Python
# This function calculats the compound interest
def cagr(originalInvestment, returnValue, termInYears):
    CAGR = ((returnValue/originalInvestment)**(1/termInYears)-1) * 100
    return "{:5.2f}".format(CAGR)
    

# print(cagr(346.14,432.73,2))