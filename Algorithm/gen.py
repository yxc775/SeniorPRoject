# -*- coding: utf-8 -*-
"""

@author: Lishan Jin
"""
import Reporter
from pyecharts import Page

import DBfunction
import txtmes

def readList(Num):
    #Waiting for DB method 

    li = []
    f2=open(r'./list'+ Num + '.txt','r+')
    art = f2.readlines()
    
    for i in range(0,len(art)):
        Symbol  = art[i].replace('\r','').replace('\n','')
        li.append(Symbol)
    
    return li

def genReport1(date):
    
    DB =  DBfunction.getDB()
    
    ListU =  DBfunction.getUserlist(DB)
    
    
    for i in range(0,len(ListU)):
        User  = ListU[i]
        ListS =  DBfunction.getUserStock(DB, User)
        ListM =  DBfunction.getUserMethod(DB, User)
        
        page = Page()
        
        l1 = Reporter.plotKline('sh')
        l3 = Reporter.plotKline('hs300')
        page.add_chart(l1 , name = 'the 200 day Kline of SH ')
        page.add_chart(l3 , name = 'the 200 day Kline of HS300')
        
        for i in range (0,len(ListS)):
            Symbol  = ListS[i]
            txtmes.setUp(date, Symbol)
            l1 = Reporter.plotKline(Symbol)
            page.add_chart(l1 , name = 'the 200 day Kline of ' + Symbol)
            
            for j in range (0,len(ListM)):
                stg =  ListM[j]
                exec('l = Reporter.plot1{}(Symbol)'.format(stg))
                exec('page.add_chart(l)')
                
                
              
        page.render('./report/'+ User + '.html')
        page.render('./hist/' + User +' '+ date + '.html')  
        
        
def genReport2(date):
    
    DB =  DBfunction.getDB()
    
    ListU =  DBfunction.getUserlist(DB)
    
    for i in range(0,len(ListU)):
        User  = ListU[i]
        ListS =  DBfunction.getUserStock(DB, User)
        ListM =  DBfunction.getUserMethod(DB, User)
        
        page = Page()
        
        l1 = Reporter.plotKline('sh')
        l3 = Reporter.plotKline('hs300')
        page.add_chart(l1 , name = 'the 200 day Kline of SH ')
        page.add_chart(l3 , name = 'the 200 day Kline of HS300')
        
        for i in range (0,len(ListS)):
            Symbol  = ListS[i]
            l1 = Reporter.plotKline(Symbol)
            page.add_chart(l1 , name = 'the 200 day Kline of ' + Symbol)
            
            for j in range (0,len(ListM)):
                stg =  ListM[j]
                exec('l = Reporter.plot2{}(Symbol)'.format(stg))
                exec('page.add_chart(l)')
                
        page.render('./report/'+ User + '.html')
        page.render('./hist/' + User +' '+ date + '.html')

        

    
