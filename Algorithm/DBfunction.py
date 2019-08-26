import os

import stockDB


def getDB():
    filep = os.path.realpath('..') + "/Database/demo.db"
    print(filep)
    db = stockDB.stockDB(filep)
    
    return db

def getUserlist(DB):
    dic = DB.get_user_name()
    li= []
    for i in range(0,len(dic)):
        name = dic[i][1] + '_' + dic[i][2]+'_'+str(dic[i][0])
        li.append(name)
        
    return li


def getStocklist(DB):
    
    dic = DB.get_stock_name()
    li= []
    for i in range(0,len(dic)):
        name = dic[i][0]
        li.append(name)
        
    return li

def getUserMethod(DB , username ):
    
    fn = username.split("_")[0]
    lm = username.split("_")[1]
    nm = username.split("_")[2]
    
    dic = DB.get_user_prefer_method(int(nm), fn,None, lm)
    
    li = []
    for i in range(0,len(dic)):
        name = dic[i][1]
        li.append(name)
        
    return li
    
def getUserStock(DB , username ):
    
    fn = username.split("_")[0]
    lm = username.split("_")[1]
    nm = username.split("_")[2]
    
    dic = DB.get_user_stock(int(nm), fn, None, lm)
    
    li = []
    for i in range(0,len(dic)):
        name = dic[i][1]
        li.append(name)
        
    return li


def readList():
    #Waiting for DB method 

    li = []
    f2=open(r'./list.txt','r+')
    art = f2.readlines()
    
    for i in range(0,len(art)):
        Symbol  = art[i].replace('\r','').replace('\n','')
        li.append(Symbol)
    
    return li

#DB = getDB()

##li = readList()
##
##
##for i in range(0,len(li)):
##    try:    
##        DB.insert_stock(stock_id = i, stock_name = li[i] , stock_description = 'SSE')
##    except:
##        print(i)
##DB.insert_user(1, 'Yunxi', 'Kou', 0 ,'', '', '', 1) 


#    
    
    
