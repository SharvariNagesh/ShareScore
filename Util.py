#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:26:01 2020

@author: sharvarinagesh
"""

import re

def to_float(stringFloat):
    if re.findall("\d", stringFloat):
        value = "{:.2f}".format(float(re.sub(',','',stringFloat)))
    else: 
        value = float(0)
    return value

# Reference: https://feliperego.github.io/blog/2016/08/10/CAGR-Function-In-Python
# This function calculats the compound interest
def cagr(originalInvestment, returnValue, termInYears):
    if(originalInvestment==0 or termInYears==0):
        print("ERROR: 0 dividend encountered in cagr. originalInvestment: {} & termInYears: {}".format(originalInvestment, termInYears))
        return 0
    CAGR = ((returnValue/originalInvestment)**(1/termInYears)-1) * 100
    return "{:5.2f}".format(CAGR)
    
#Formatting float numbers. And fixing 2 decimal places.
def ffmt(longFloat):
    return "{:.2f}".format(longFloat)


# print(cagr(346.14,432.73,2))
# print(cagr(10,432.73,0))
# print(to_float('11.8888888888'))
# print(ffmt(33.5611439187844))