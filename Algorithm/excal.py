# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 16:36:05 2019

@author: Lishan Jin
"""

import pandas as pd  
import tushare as ts  
 
def excal():
    cal_dates = ts.trade_cal()
 
    for i in cal_dates.index:
        isOpen = cal_dates.loc[i]['isOpen']
        if not isOpen:
            cal_dates.drop([i],axis = 0, inplace = True)
    
    cal_dates = cal_dates.reset_index()
    cal_dates = cal_dates.drop('index', axis = 1)
    cal_dates.to_csv('./data/excal.csv',index=False,sep=',')
    
    
excal()
    
