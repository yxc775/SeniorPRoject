# -*- coding: utf-8 -*-
"""

@author: Lishan Jin
"""
"""
    Data preparation tool
    
    Using Txt file as symbol list 
    collect daily high low price and close price and previous close price 
    for previous 200 trading days from today 
    
    output data to symbol index.csv file to each symbol
"""
import pandas as pd
import datetime
import tushare as ts
import numpy as np
import DBfunction

def finddate(num, enddate):
    
    path = './data/excal.csv'
    cal_dates = pd.read_csv(path)
    
    inde = cal_dates.loc[cal_dates.calendarDate == enddate].index
    startdate = cal_dates.iloc[inde - 199].calendarDate.values[0]
    
    return startdate, enddate

def prepData(edd):
    num = 200
#    x = datetime.datetime.now()
#    edd = str(x)[0:10] 
    DB = DBfunction.getDB()
    
    std, edd = finddate(num,edd)
    List = DBfunction.getStocklist(DB)
    
    cont = np.zeros(len(List))
    Na2 = pd.DataFrame(cont,columns=['Name'])
    
    for i in range(0,len(List)):
            
        Symbol  = List[i]
        
        Na2.Name.iloc[i] = Symbol
        
        dt = ts.get_hist_data(Symbol,start = std , end = edd)
        dt2 = dt[['open','high','close','low']]
        
        length = dt2.shape[0]
        if length < num:
            dt = ts.get_hist_data( Symbol , end = edd)
            if dt.shape[0] < num:
                 dt2 = dt[['open','high','close','low']]
            else:
                dt2 = dt.head(num)[['open','high','close','low']]
        
        dt3= dt2.sort_index(axis=0 ,ascending=True)
        dt3['date'] = dt3.index
        dt3 = dt3.reset_index(drop = True)
        dt3['ind'] = dt3.index
        dt3.to_csv('./data/'+ Symbol +'.csv',index=False,sep=',')
        
    Na2['ind'] = Na2.index
    Na2.to_csv('./data/StockName.csv',index=False,sep=',')

    
def AddData():
    num = 200
    x = datetime.datetime.now()
    edd = str(x)[0:10] 
    
    DB = DBfunction.getDB()
    List = DBfunction.getStocklist(DB)
    
    for i in range(0,len(List)):
            
        Symbol  = List[i]
        
        dt = ts.get_hist_data(Symbol,start = edd , end = edd)
        dt2 = dt[['open','high','close','low']]
        dt2['date'] = dt2.index
        dt2 = dt2.reset_index(drop = True)
        
        path = './data/' + Symbol+ '.csv'
        data_df2 = pd.read_csv(path)
        data_df2 = data_df2.drop('index')
        
        data_df2.append(dt2 , sort = False)
        data_df2 = data_df2.tail(num)
        
        data_df2 = data_df2.reset_index(drop = True)
        data_df2.to_csv('./data/'+ Symbol +'.csv',index=True ,sep=',')
     

    