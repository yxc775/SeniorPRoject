
from pyecharts import Bar, Line, Overlap
from pyecharts import Page
from pyecharts import Grid, Kline # partially used
import pandas as pd

def plot1MASS(Symbol):
    
    path = './data1/'+ Symbol + 'MASS.csv'
    df = pd.read_csv(path)
    l1 = Line('MASS of ' + Symbol ,background_color="#FFF", width=1500, height=680)
    l1.add('MASS',df['date'],df['MASS'])
    
    return l1

def plotKline(Symbol):
    
    path2 = './data/' + Symbol+ '.csv'
    df2 = pd.read_csv(path2)
    l2 = Line('Kline of ' + Symbol ,background_color="#FFF", width=1500, height=680)
    l2.add('Close price',df2['date'],df2['close'])
    
    return l2

def plot1KDJ(Symbol):
    
    path = './data1/'+ Symbol + 'KDJ.csv'
    df = pd.read_csv(path)
    l1 = Line('KDJ of ' + Symbol ,background_color="#FFF", width=1500, height=680)
    l1.add('kdj_k',df['date'],df['kdj_k'])
    l1.add('kdj_d',df['date'],df['kdj_d'])
    l1.add('kdj_j',df['date'],df['kdj_j'])
    
    return l1

def plot1MACD(Symbol):
    
    path = './data1/'+ Symbol + 'MACD.csv'
    df = pd.read_csv(path)
    
    l1 = Line('MACD of ' + Symbol, background_color="#FFF", width=1500, height=680)
    l1.add('DIFF',df['date'],df['DIFF'])
    l1.add('DEA',df['date'],df['DEA'])
    
    b1 = Bar(width=1500, height=680)
    b1.add('MACD',df['date'],df['MACD'])
    
    ov = Overlap()
    ov.add(l1)
    ov.add(b1)
    
    return ov
    
def plot1DMI(Symbol):
    
    path = './data1/'+ Symbol + 'DMI.csv'
    df = pd.read_csv(path)
    
    l1 = Line('DMI of ' + Symbol, background_color="#FFF", width=1500, height=680)
    l1.add('PDI',df['date'],df['PDI'])
    l1.add('MDI',df['date'],df['MDI'])
    l1.add('ADX',df['date'],df['ADX'])
    l1.add('ADXR',df['date'],df['ADXR'])

    return l1


def plot2MASS(Symbol):
    
    path = './data2/'+ Symbol + 'MASS.csv'
    df = pd.read_csv(path)
    l1 = Line('MASS of ' + Symbol ,background_color="#FFF", width=1500, height=680)
    l1.add('MASS',df['date'],df['MASS'])
    
    return l1

def plot2KDJ(Symbol):
    
    path = './data2/'+ Symbol + 'KDJ.csv'
    df = pd.read_csv(path)
    l1 = Line('KDJ of ' + Symbol ,background_color="#FFF", width=1500, height=680)
    l1.add('kdj_k',df['date'],df['kdj_k'])
    l1.add('kdj_d',df['date'],df['kdj_d'])
    l1.add('kdj_j',df['date'],df['kdj_j'])
    
    return l1

def plot2MACD(Symbol):
    
    path = './data2/'+ Symbol + 'MACD.csv'
    df = pd.read_csv(path)
    
    l1 = Line('MACD of ' + Symbol, background_color="#FFF", width=1500, height=680)
    l1.add('DIFF',df['date'],df['DIFF'])
    l1.add('DEA',df['date'],df['DEA'])
    
    b1 = Bar(width=1500, height=680)
    b1.add('MACD',df['date'],df['MACD'])
    
    ov = Overlap()
    ov.add(l1)
    ov.add(b1)
    
    return ov
    
def plot2DMI(Symbol):
    
    path = './data2/'+ Symbol + 'DMI.csv'
    df = pd.read_csv(path)
    
    l1 = Line('DMI of ' + Symbol, background_color="#FFF", width=1500, height=680)
    l1.add('PDI',df['date'],df['PDI'])
    l1.add('MDI',df['date'],df['MDI'])
    l1.add('ADX',df['date'],df['ADX'])
    l1.add('ADXR',df['date'],df['ADXR'])

    return l1

def readList(Num):
    #Waiting for DB method 

    li = []
    f2=open(r'./list'+ Num + '.txt','r+')
    art = f2.readlines()
    
    for i in range(0,len(art)):
        Symbol  = art[i].replace('\r','').replace('\n','')
        li.append(Symbol)
    
    return li


#ListS = readList('4')
#ListM = readList('2')
#
#page = Page()
#
#for i in range (0,len(ListS)):
#    Symbol  = ListS[i]
#    l1 = plotKline(Symbol)
#    page.add_chart(l1 , name = 'the 200 day Kline of ' + Symbol)
#            
#    for j in range (0,len(ListM)):
#        stg =  ListM[j]
#        exec('l2 = plot{}(Symbol)'.format(stg))
#        page.add_chart(l2)
#                
#page.render('test.html')