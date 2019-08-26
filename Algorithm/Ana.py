# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 22:17:28 2019

@author: Lishan Jin
"""

import DBfunction

def Doanas ():
    DB = DBfunction.getDB()
    ListS = DBfunction.getStocklist(DB)
    ListM = readList2()
    
    for i in range(0,len(ListS)):
        Symbol  = ListS[i]
        print(Symbol)
            
        for j in range(0,len(ListM)):
            stg = ListM[j]
            exec('{}(Symbol)'.format(stg))
        
def readList2():
    #Waiting for DB method 
    #Ana method for each stock
    li = []
    f2=open(r'./list2.txt','r+')
    art = f2.readlines()
    
    for i in range(0,len(art)):
        Symbol  = art[i].replace('\r','').replace('\n','')
        li.append(Symbol)
    
    return li
