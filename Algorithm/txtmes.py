# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 20:55:15 2019

@author: Lishan Jin
"""
import pandas as pd
from numpy import diff

def setUp(date,Symbol):
    output = pd.DataFrame(columns=['method','outcome'])
    name = date + '-' + Symbol + 'evl'
    output.to_csv('./'+ name +'.csv',index=False,sep=',')
    
    
def evMACD1 (date , Symbol):
        
    path = './data1/'+ Symbol + 'MACD.csv'
    df = pd.read_csv(path)
    name = date + '-' + Symbol + 'evl'
    output = pd.read_csv('./'+ name +'.csv')

    i = df.loc[df['date'] == date].index
    DIF = df.iloc[i]['DIFF'].values[0] 
    MACD =  df.iloc[i]['MACD'].values[0] 
    avg = df.iloc[i]['avg'].values[0] 
                 
    if avg != 0 :
        if DIF > 0 :
            if MACD > 0 :
               df2 = pd.DataFrame({'method':['MACD'], 'outcome':[1]}) 
                    
        elif DIF < 0:            
            if MACD < 0 :
                df2 = pd.DataFrame({'method':['MACD'], 'outcome':[-1]})  
                    
        else:
             df2 = pd.DataFrame({'method':['MACD'], 'outcome':[0]})  
    else:
         df2 = pd.DataFrame({'method':['MACD'], 'outcome':[0]})  
    
    output = output.append(df2, ignore_index = True)
    output.to_csv('./'+ name +'.csv',index=False,sep=',')
    
def evMASS1(date , Symbol):
    
    path = './data1/'+ Symbol + 'MASS.csv'
    df = pd.read_csv(path)
    i = df.loc[df['date'] == date].index
    
    y = [df.iloc[i-3]['MASS'].values[0],df.iloc[i-2]['MASS'].values[0],df.iloc[i-1]['MASS'].values[0],df.iloc[i]['MASS'].values[0]]
    dx = 1
    dy2 = diff(y)/dx
    dy = dy2[-1]
    ddy2 = diff(dy2)/dx
    ddy = ddy2[-1]
    
    name = date + '-' + Symbol + 'evl'
    output = pd.read_csv('./'+ name +'.csv')
    
    if dy > 0:
        if ddy > 0 or ddy == 0:
            df2 = pd.DataFrame({'method':['MASS'], 'outcome':[2]}) 
        else:
            df2 = pd.DataFrame({'method':['MASS'], 'outcome':[1]}) 
    elif dy < 0:
        if ddy > 0 or ddy == 0:
            df2 = pd.DataFrame({'method':['MASS'], 'outcome':[-1]}) 
        else:
            df2 = pd.DataFrame({'method':['MASS'], 'outcome':[-2]}) 
    else:
        df2 = pd.DataFrame({'method':['MASS'], 'outcome':[0]}) 
            
    output = output.append(df2, ignore_index = True)
    output.to_csv('./'+ name +'.csv',index=False,sep=',')
    
def evKDJ1(date , Symbol):
    
    path = './data1/'+ Symbol + 'KDJ.csv'
    df = pd.read_csv(path)
    
    i = df.loc[df['date'] == date].index
    k = df.iloc[i]['kdj_k'].values[0] 
    j =  df.iloc[i]['kdj_j'].values[0] 
    d = df.iloc[i]['kdj_d'].values[0] 
    
    name = date + '-' + Symbol + 'evl'
    output = pd.read_csv('./'+ name +'.csv')
    
    if j > 100 :
        df2 = pd.DataFrame({'method':['KDJ'], 'outcome':[-2]}) 
    elif j < 10:
        df2 = pd.DataFrame({'method':['KDJ'], 'outcome':[2]})
    else:
        if d > k :
            df2 = pd.DataFrame({'method':['KDJ'], 'outcome':[-1]}) 
        elif d < k:
            df2 = pd.DataFrame({'method':['KDJ'], 'outcome':[1]})
        else:
            df2 = pd.DataFrame({'method':['KDJ'], 'outcome':[0]})
            
    output = output.append(df2, ignore_index = True)
    output.to_csv('./'+ name +'.csv',index=False,sep=',')
    
def evDMI1(date , Symbol):
    
    path = './data1/'+ Symbol + 'DMI.csv'
    df = pd.read_csv(path)
    name = date + '-' + Symbol + 'evl'
    output = pd.read_csv('./'+ name +'.csv')
    
    i = df.loc[df['date'] == date].index
    PDI = df.iloc[i]['PDI'].values[0] 
    MDI =  df.iloc[i]['MDI'].values[0] 
    ADX = df.iloc[i]['ADX'].values[0] 
    ADXR = df.iloc[i]['ADXR'].values[0]
    
    a = 0
    if PDI > MDI:
        a = a + 1
        if ADX > ADXR:
            a = a + 1
    elif PDI < MDI:
        a = a - 1
        if ADX < ADXR:
            a = a - 1
    else:
        a = 0
    
    df2 = pd.DataFrame({'method':['DMI'], 'outcome':[a]})
    output = output.append(df2, ignore_index = True)
    output.to_csv('./'+ name +'.csv',index=False,sep=',')
    
    
def interpre(Symbol , method,date):
    
    name = date + '-' + Symbol + 'evl.csv'
    df = pd.read_csv(name) 
    i = df.loc[df['method'] == method].index
    outcome = df.iloc[i]['outcome'].values[0]
    
    if outcome == 2:
        txt = '\nFrom method ' + method + ', ' + Symbol + ' has a very positve situation'
    elif outcome == 1:
        txt = '\nFrom method ' + method + ', ' + Symbol + ' has a positve situation'
    elif outcome == 0:
        txt = '\nFrom method ' + method + ', ' + Symbol + ' has a neutral situation'
    elif outcome == -1:
        txt = '\nFrom method ' + method + ', ' + Symbol + ' has a negative situation'
    elif outcome == -2:
        txt = '\nFrom method ' + method + ', ' + Symbol + ' has a very negative situation'
    
    return txt
