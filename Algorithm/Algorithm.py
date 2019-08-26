import talib as ta
import pandas as pd
import pylab as pl
import numpy as np

from pyecharts import Bar, Line, Overlap
from pyecharts import Page
from pyecharts import Grid, Kline # partially used


def MASS(Symbol):
    n = 20
    path = './data/' + Symbol+ '.csv'
    data_df2 = pd.read_csv(path)
    data_cl = data_df2['close']
    s1 = [1]
    for i in range (2,n + 1):
        s1 = s1 + [i]
        df2 = pd.DataFrame(columns=s1)
        
    for i in range(1,n + 1):
        df2[i]=ta.MA(np.array(data_cl), timeperiod= i, matype=0) 
        
 
    df2['date'] = data_df2['date']

    df2.drop(range(0,n),inplace=True)

    s2 = df2.index

    df2 = df2.reset_index()

    date =  df2['date']
       
    mass = np.zeros(len(df2))
    for i in range(0,len(df2)-1):
        for j in range(1,n):
            if df2[j][i] > df2[j + 1][i]:
                mass[i] = mass[i] + 100/n

    output = pd.DataFrame(mass,columns=['MASS'])
    output['date'] = date
    output['ind'] = output.index
    output.to_csv('./data2/'+ Symbol + 'MASS.csv',index=False,sep=',')
    
    

def MASS2(Symbol):
    n = 20
    path = './data/' + Symbol+ '.csv'
    data_df2 = pd.read_csv(path).tail(n + 1)
    data_df2 = data_df2.reset_index()
    data_cl = data_df2['close']
    s1 = [1]
    for i in range (2,n + 1):
        s1 = s1 + [i]
        df2 = pd.DataFrame(columns=s1)
        
    for i in range(1,n + 1):
        df2[i]=ta.MA(np.array(data_cl), timeperiod= i, matype=0) 
        
    df2['date'] = data_df2['date']
    df2.drop(range(0,n),inplace=True)
    df2 = df2.reset_index()

    date =  df2['date']
       
    mass = np.zeros(len(df2))
    for i in range(0,len(df2)-1):
        for j in range(1,n):
            if df2[j][i] > df2[j + 1][i]:
                mass[i] = mass[i] + 100/n
              
    output = pd.DataFrame(mass,columns=['MASS'])
    output['date'] = date
    
    path2 = './data/'+ Symbol + 'MASS.csv'
    ori = pd.read_csv(path2)
    ori.loc[len(ori)] = output.iloc[0]
    ori.to_csv('./'+ Symbol + 'MASS.csv',index=False,sep=',')

def MACD(Symbol):
    EMA1 = 12
    EMA2 = 26
    N = 9
    
    path = './data/' + Symbol+ '.csv'
    df = pd.read_csv(path)
    data_cl = df['close']
    date =  df['date']
    output = pd.DataFrame(date,columns=['date'])
    output['date'] = date

    output['avg'] = ta.MA(np.array(data_cl), timeperiod= N, matype=0) 
    output['DIFF'], output['DEA'], output['MACD'] =  ta.MACD(data_cl, fastperiod= EMA1, \
    slowperiod= EMA2, signalperiod= N)
    
    output.drop(range(0,33),inplace=True)
    output['ind'] = output.index
    output.to_csv('./data2/'+ Symbol + 'MACD.csv',index=False,sep=',')
    
    
def KDJ( Symbol):
    
    n = 20
    path = './data/' + Symbol+ '.csv'
    df = pd.read_csv(path)
    date =  df['date']
    
    lowList= df['low'].rolling(n).min()
    lowList.fillna(value = df['low'].expanding().min(), inplace=True)
    
    highList = df['high'].rolling(n).max()
    highList.fillna(value = df['high'].expanding().max(), inplace=True)
    
    rsv = (df['close'] - lowList) / (highList - lowList) * 100
    
    output = pd.DataFrame(date,columns=['date'])
    
    k = [50] * len(df)
    d = [50] * len(df)
    
    for i in range(1 , len(df)):
        k[i] = rsv.iloc[i]/3 + 2*k[i-1]/3
        d[i] = 2*d[i-1]/3 + 1*k[i]/3

    output['kdj_k'] = k
#    output['kdj_d'] = df['kdj_k'].ewm(com = 2)
    output['kdj_d'] = d
    output['kdj_j'] = 3.0 * output['kdj_k'] - 2.0 * output['kdj_d']
    output['ind'] = output.index
    output.to_csv('./data2/'+ Symbol + 'KDJ.csv',index=False,sep=',')
    
    
def DMI(Symbol):
    
    N = 12
    MM = 16
    
    path = './data/' + Symbol+ '.csv'
    df2 = pd.read_csv(path)
    
    date =  df2['date']
    close = df2['close']
    high = df2['high']
    low = df2['low']
    
    df = pd.DataFrame()
    df['h-l'] = high-low
    df['h-c'] = abs(high-close.shift(1))
    df['l-c'] = abs(close.shift(1)-low)
    df['tr'] = df.max(axis=1)
    df['PDM'] = high-high.shift(1)
    df['MDM'] = low.shift(1)-low
    df['DPD'] = 0
    df['DMD'] = 0
    df['NTR'] = 0
    df['NPDM'] = 0
    df['NMDM'] = 0
    df['ADX'] = 0
    df['ADXR'] = 0
    df['PDI'] = 0
    df['MDI'] = 0
    df['DX'] = 0
    
    for i in range(len(df.index)):
        PDM = df['PDM'].iloc[i]
        MDM = df['MDM'].iloc[i]
        if PDM<0 or PDM<MDM:
            df['DPD'].iloc[i] = 0
        else:
            df['DPD'].iloc[i] = PDM
        if MDM<0 or MDM<PDM: 
            df['DMD'].iloc[i] = 0
        else:
            df['DMD'].iloc[i] = MDM
            
    for i in range(N,len(df.index)):
        df['NTR'].iloc[i] = sum(df['tr'].iloc[i-N+1:i])
        df['NPDM'].iloc[i] = sum(df['DPD'].iloc[i-N+1:i])
        df['NMDM'].iloc[i] = sum(df['DMD'].iloc[i-N+1:i])
        
    df['PDI'] = df['NPDM']/df['NTR']*100
    df['MDI'] = df['NMDM']/df['NTR']*100
    df['DX'] = abs(df['MDI']-df['PDI'])/(df['MDI']+df['PDI'])*100
    
    for i in range(MM,len(df.index)):
        summDX = 0
        summADX = 0
        for j in range(i-MM,i):
            summDX += df['DX'].iloc[j]
            summADX += df['ADX'].iloc[j]
        df['ADX'].iloc[i] = summDX/MM
        summADX += df['ADX'].iloc[j]
        df['ADXR'].iloc[i] = summADX/MM
    
    df['date'] = date
    df['ind'] = df.index
    df.to_csv('./data2/'+ Symbol + 'DMI.csv',index=False,sep=',')
    
    
    
def plotMASS(Symbol):
    
    path = './data/'+ Symbol + 'MASS.csv'
    df = pd.read_csv(path)
    l1 = Line('MASS',background_color="#FFF", width=1500, height=680,is_datazoom_show=True, datazoom_type="both")
    l1.add('MASS',df['date'],df['MASS'])
    
    return l1

def plotKline(Symbol):
    
    path2 = './data/' + Symbol+ '.csv'
    df2 = pd.read_csv(path2)
    df2.drop(range(0,n),inplace=True)
    l2 = Line(background_color="#FFF", width=1500, height=680,is_datazoom_show=True, datazoom_type="both",)
    l2.add('Close price',df2['date'],df2['close'])
    
    return l2

def plotKDJ(Symbol):
    
    path = './data/'+ Symbol + 'KDJ.csv'
    df = pd.read_csv(path)
    l1 = Line('KDJ',background_color="#FFF", width=1500, height=680,is_datazoom_show=True, datazoom_type="both")
    l1.add('kdj_k',df['date'],df['kdj_k'])
    l1.add('kdj_d',df['date'],df['kdj_d'])
    l1.add('kdj_j',df['date'],df['kdj_j'])
    
    return l1

def plotMACD(Symbol):
    
    path = './data/'+ Symbol + 'MACD.csv'
    df = pd.read_csv(path)
    
    l1 = Line(background_color="#FFF", width=1500, height=680,is_datazoom_show=True, datazoom_type="both")
    l1.add('DIFF',df['date'],df['DIFF'])
    l1.add('DEA',df['date'],df['DEA'])
    
    b1 = Bar(is_datazoom_show=True, datazoom_type="both")
    b1.add('MACD',df['date'],df['MACD'])
    
    ov = Overlap()
    ov.add(l1)
    ov.add(b1)
    
    return ov
    
    
    
    
    
    


