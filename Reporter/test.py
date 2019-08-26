

#import tushare as ts # not used
import numpy as np
import talib  as ta
import pandas as pd
#import pylab as pl # not used
import random as rm
import datetime as dt
#import matplotlib as mpl # not used
import warnings
from pyecharts import Page
from pyecharts import Line, Grid, Bar, Overlap, Kline # partially used



class testbase :
    
    # 数据结构搭建
    __pos = pd.DataFrame(columns = ['Symbol','Date', 'vol'])
    __record = pd.DataFrame(columns = ['Symbol','Date', 'act', 'dvol', 'price'])
    __hash = pd.DataFrame(columns = ['Symbol','NumR','NumP'])
    __date = dt.datetime.now()
    __symlist = pd.DataFrame(columns = ['Symbol'])
    __stglist = pd.DataFrame(columns = [ 'startDate','endDate'])
    __timeline = pd.DataFrame(columns = ['Date'])
    __net = pd.DataFrame()
    __lastPos = {}
    __costPri = {}
    __TranSign= {}
    
    """
    用来跑回测得部分，console 内输入：
    b1 = testbase(起始日期，结束日期) 此时初始金钱为1000000 回测运行周期为 1
    可以自订周期和初始本金
    b1 = testbase(起始日期，结束日期，总本金，周期)
    日期格式为 '2018-06-07' 字符串形式
    周期和钱 是 整数形式
    
    如果需要连续运行几遍，请先清空内存 或 直接 runfile('D:/CTA files/test2.py', wdir='D:/CTA files')
    再开始跑下一遍 不然就报错

    """
    def __init__(self, startDt , endDt , totalMoney = 1000000 , preiod = 1):
        warnings.filterwarnings("ignore")
        self.prepBackTest(startDt , endDt , totalMoney)
        self.backTestP(preiod)
    
    """
    读取数据
    以CSV格式输入
    文件名应该与输入的标的名相同
    如果成功导入，则有 df， 标的名，imported 字样
    
    """
    def initialDB (self):
        sym = self.getSymlist()
        for i in sym.index:
            path = './' + sym.Symbol[i] + '.csv'
            exec('self.df{} = pd.read_csv(path)'.format(sym.Num[i]))
            print('df' , sym.Symbol[i] , 'imported')
            
    # 清除数据 应该用不到
    def clearALL(self):
        self.__pos = pd.DataFrame(columns = ['Symbol','Date', 'vol'])
        self.__record = pd.DataFrame(columns = ['Symbol','Date', 'act', 'dvol', 'price'])
        self.__hash = pd.DataFrame(columns = ['Symbol','NumR','NumP'])
        self.__stglist = pd.DataFrame(columns = ['stg', 'startDate','endDate'])
        self.__timeline = pd.DataFrame(columns = ['Date'])
        self.__date = dt.datetime.now()
        self.__net = pd.DataFrame()
        self.__lastPos = {}
        self.__costPri = {}
        
    #目前默认的设置 每个标的本金的方法 平均分钱
    def initialMon(self , total , startdate):
        sym = self.getSymlist()
        ToT = sym.shape[0]
        percent = 1.0/ToT
        
        for i in sym.index:
            exec('self.Mon{} = pd.DataFrame(columns = ["Date","Money"])'\
                 .format(sym.Num[i]))
            exec('self.Mon{}.loc[self.Mon{}.shape[0]] = [startdate , {}]'\
                 .format(sym.Num[i] , sym.Num[i] , total * percent))
            
            print('df' , sym.Symbol[i] , 'Money set')
    
    #都是GET SET 方法 后续用不到
    def getPos(self):
        return self.__pos
    
    def getRecord(self):
        return self.__record
    
    def getHash(self):
        return self.__hash
    
    def getDate(self):
        return self.__date
    
    def setDate(self,date):
        self.__date = date
        
    def getSymlist(self):
        return self.__symlist
    
    def setSymlist (self ,List):
        df = pd.DataFrame(columns = ['Symbol','Num'])
        for i in List :
            df.loc[df.shape[0]] = [i , rm.randrange(1,200)]
        
        
    def getData(self , Symbol):
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        _locals = locals()
        exec('df = self.df{}'.format(num.values[0]) ,globals(),_locals)
        df = _locals['df']
        return df
            
    def getMoney (self , Symbol):
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        df = pd.DataFrame()
        _locals = locals()
        exec('df = self.Mon{} '.format(num.values[0]) ,globals(),_locals)
        df = _locals['df']
        return df
    
    def setMoney (self , date , Symbol , mo):
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        exec('self.Mon{}.loc[self.Mon{}.shape[0]] = [date , {}]'\
                 .format(num.values[0] , num.values[0] , mo))
        
    def setCost(self, Symbol , price):
        self.__costPri[Symbol] = price
        
    def getLastCos(self , Symbol):
        a = self.__costPri
        return a[Symbol]

    def getLastPos(self , Symbol):
        a = self.__lastPos
        return a[Symbol]
    
    def setLastPos(self , Symbol , pos):
        self.__lastPos[Symbol] = pos
        
    def getTranSign(self , Symbol):
        a = self.__TranSign
        return a[Symbol]
    
    def setTranSign(self , Symbol , sign):
        self.__TranSign[Symbol] = sign
        
    def findPos (self , Symbol , date):
        a = self.getPos()
        b = a.loc[a['Date'] == date]
        
        if b.empty:
            posi = 0
        else:
            posi = b.loc[b['Symbol']  == Symbol ].iloc[-1].values[3]    
            
        return posi    
    
    def findRecord (self , Symbol , date):
        a = self.getRecord()
        b =  a.loc[a['Date'] == date]
        
        if b.empty:
            print('There is no such record =__= ')
        else:
            reci = b.loc[b['Symbol']  == Symbol ].iloc[-1] 
            return reci
     
    def addtoRecord (self , Symbol , act , dvol , price , date):
        # 1 做多 -1 做空 2平仓 0 不变
        self.__record.loc[self.__record.shape[0]] = [Symbol, date, act, dvol, price]
    
    def addtoPos (self , Symbol , act , dvol , date , pos1):
        # 1 做多 -1 做空 2平仓 0 不变
        if act == 1:
            self.__pos.loc[self.__pos.shape[0]] = [Symbol , date, pos1 + dvol]
            
            self.setLastPos(Symbol , pos1 + dvol)
        elif act == -1:
            self.__pos.loc[self.__pos.shape[0]] = [Symbol , date, pos1 - dvol]
            
            self.setLastPos(Symbol , pos1 - dvol)
        else:
            self.__pos.loc[self.__pos.shape[0]] = [Symbol , date, pos1]
            
            self.setLastPos(Symbol , pos1)
            
    # 返回时间轴上的前一天 如果没有 返回 0
    def lastday (self , date , Symbol):
        Tline = self.__timeline
        ind = Tline.loc[Tline['Date'] == date].index - 1
        if(ind >= 0):
            date1 = Tline.iloc[ind]['Date']
            
            return date1.to_string(index = False)
        else:
            return 0
    
    # 返回时间轴上的前一天 如果没有 返回 0
    def nextday (self , date , Symbol):
        Tline = self.__timeline
        ind = Tline.loc[Tline['Date'] == date].index + 1
        if(ind >= Tline.shape[0]):
            return 0
        else:
            date1 = Tline.iloc[ind]['Date']
            return date1.to_string(index = False)
        
    # 获得 某一天 某个标的的 根据目前的现金 返回最大可买进量
    def getDvol (self , Symbol , date):
        
        stgL = self.__stglist
        TradeU = stgL.loc[Symbol].tradeUnit
        
        moneyl = self.getMoney(Symbol)
        df = self.getData(Symbol)
        temp1 = df.loc[df['date'] == date]['close']
        price =  temp1.values[0]
        mon = moneyl.iloc[-1]['Money']
       # mon =  temp2.values[0]

        dvol = mon // (price * TradeU)
        
        return dvol
    
    # 买进 
    # sign = 1 做多 -1 做空
    # dvol 买进的量
    def buy (self , Symbol , dvol , date , sign):
        
        # 考虑手续费 详见 ReadMe
        stgL = self.__stglist
        feeP = stgL.loc[Symbol].fee
        feeU = stgL.loc[Symbol].feeUnit
        TradeU = stgL.loc[Symbol].tradeUnit
        
        df = self.getData(Symbol)
        price = df.loc[df['date'] == date]['close']     
        price = price.values[0]
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        if feeU == 'U':
            dmon = dvol * price * TradeU + dvol * TradeU * feeP
        elif feeU == 'W':
            dmon = dvol * price * TradeU
            dmon = dvol * price * TradeU + feeP * dmon /10000.0
        else:
            dmon = dvol*price*TradeU
            
        pos1 = self.getLastPos(Symbol)
        self.setCost(Symbol , price)
        
        self.setMoney (date , Symbol , mon - dmon)
    
        if sign == 1 :
            if pos1 >= 0:
                self.addtoRecord(Symbol , 1 , dvol ,  price , date)
                self.addtoPos(Symbol , 1 , dvol , date , pos1)
                
            else:
                self.level(date , Symbol)
                self.addtoRecord(Symbol , 1 , dvol ,  price , date)
                self.addtoPos(Symbol , 1 , dvol , date , 0)
                
        elif sign == -1:
            if pos1 <= 0:
                self.addtoRecord(Symbol , -1 , dvol ,  price , date)
                self.addtoPos(Symbol , -1 , dvol , date , pos1)
                
            else:
                self.level(date , Symbol)
                self.addtoRecord(Symbol , -1 , dvol ,  price , date)
                self.addtoPos(Symbol , -1 , dvol , date , 0)
    
    #对某标的平仓
    def level (self , date , Symbol):
        
        stgL = self.__stglist
        feeP = stgL.loc[Symbol].fee
        feeU = stgL.loc[Symbol].feeUnit
        TradeU = stgL.loc[Symbol].tradeUnit
        
        pos1 = self.getLastPos(Symbol)
        cost = self.getLastCos(Symbol)
        
        df = self.getData(Symbol)
        price = df.loc[df['date'] == date]['close']     
        price = price.values[0]
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        if pos1 > 0 :
            if feeU == 'U':
                dmon = pos1 * price * TradeU - pos1 * TradeU * feeP
            elif feeU == 'W':
                dmon = pos1 * price * TradeU
                dmon = pos1 * price * TradeU - feeP * dmon /10000.0
            else:
                dmon = pos1 * price * TradeU
                
            self.setMoney (date , Symbol , mon + dmon)
            self.addtoPos(Symbol , 2 , pos1 , date , 0)
            self.addtoRecord (Symbol , 2 , pos1 , price , date)
            
        elif pos1 < 0 :
            dmon = pos1 * 2 * (cost - price)
            dmon = mon + dmon + abs(pos1) * price
            
            
            if feeU == 'U':
                dmon = dmon - pos1 * TradeU * feeP
            elif feeU == 'W':
                dmon = dmon - feeP * price * pos1 /10000.0
            else:
                dmon = dmon
            
            self.setMoney (date , Symbol , dmon)
            self.addtoPos(Symbol , 2 , pos1 , date , 0)
            self.addtoRecord (Symbol , 2 , pos1 , price , date)
            
        else:
            self.setMoney (date , Symbol , mon)
            self.addtoPos(Symbol , 2 , 0 , date , 0)
            self.addtoRecord (Symbol , 2 , 0 , price , date)
            
     #对某标的平仓  
     #这个标的已经退出回测序列   
    def level2 (self , date , Symbol):
        
        self. level ( date , Symbol)
        net2 = self.getNet2(Symbol)
        self.__net.set_value(date , Symbol , net2)
     
    # 某天 某标的身上什么都没有发生
    def nothingHap (self , date , Symbol):
        pos1 = self.getLastPos(Symbol)
        
        df = self.getData(Symbol)
        price = df.loc[df['date'] == date]['close']     
        price = price.values[0]
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        self.setMoney (date , Symbol , mon)
        self.addtoPos(Symbol , 0 , 0 , date , pos1)
        self.addtoRecord (Symbol , 0 , 0 , price , date)
        
    #   某天 某标的身上什么都没有发生 
    #  这个标的已经退出回测序列 或者 还没有加入序列
    def nothingHap2 (self , date , Symbol):
        pos1 = self.getLastPos(Symbol)
        
        price = self.getLastCos(Symbol)
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        self.setMoney (date , Symbol , mon)
        self.addtoPos(Symbol , 0 , 0 , date , pos1)
        self.addtoRecord (Symbol , 0 , 0 , price , date)
        
        net2 = self.getNet2(Symbol)
        self.__net.set_value(date , Symbol , net2)
    
    # 割肉 止损
    # 返回 TRUE 如果止损被执行  FALSE 如果没有
    # 预设 价格负向波动超过 成本价的 10%
    # 目前所有策略都有该止损
    def cutdown (self , date , Symbol):
        
        pos1 = self.getLastPos(Symbol)
        df = self.getData(Symbol)
        
        
        if pos1 != 0:
            pricenow = df.loc[df['date'] == date]['close'].values[0]
            price = self.getLastCos(Symbol)
        
            if pos1 > 0 :
                if pricenow < price * 0.90 :
                    self.level(date , Symbol)
                    return True
                else:
                    return False
            elif pos1 < 0:
                if pricenow > price * 1.10:
                    self.level(date , Symbol)
                    return True
                else:
                    return False
        else:
            self.nothingHap (date, Symbol)
            return False 
        
    # 处理交易信号
    # 自带止损 如止损 print cutdown， 时间，标的 并结束该天
    # 每一个时间中 每一个标的 只有一次交易
    
    def signTrade(self, Symbol, date):
        sign = self.getTranSign(Symbol)
        
        if self.cutdown(date , Symbol )== False :
            if sign == 0:
                self.nothingHap (date, Symbol)
                
            elif sign == 2:
                self.level( date,Symbol )
                
            elif sign == 1:
                dvol = self.getDvol(Symbol, date)
                self.buy(Symbol, dvol, date , 1)
                
            elif sign == -1:
                dvol = self.getDvol(Symbol, date)
                self.buy(Symbol, dvol, date , -1)
        else: 
            print ('CUTDOWN', date , Symbol)
            
    #返回某天某标的的净值 这个标的已经退出回测序列 或者 还没有加入序列
    def getNet(self , date , Symbol):
        
        pos1 = self.getLastPos(Symbol)
        cost = self.getLastCos(Symbol)
        
        df = self.getData(Symbol)
        price = df.loc[df['date'] == date]['close']     
        price = price.values[0]
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        if pos1 > 0 :
            dmon = pos1 * price
            net = mon + dmon
            
        elif pos1 < 0 :
            dmon = pos1 * 2 * (cost - price)
            net = mon + dmon + abs(pos1) * price
            
        else:
            net = mon
        
        return net 
    
    #返回某标的净值 
    def getNet2(self ,Symbol):
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        net = mon
        
        return net 
    
    #画净值图
    #单标的在一张图上
    #总线在下面
    #输出至 工作文件夹下 echart.html
    def plotNet(self):
        
        stgL = self.__stglist
        netall = self.__net
        
        page = Page()
        line = Line(background_color="#FFF", width=1500, height=680)
                    
        for Symbol in stgL.index :
            line.add(Symbol, list(netall.index), list(netall[Symbol].values), is_datazoom_show=True, datazoom_type="both",\
                 is_xaxislabel_align = True, tooltip_axispointer_type="cross", datazoom_xaxis_index=[0, 1],\
                 yaxis_min="dataMin"  ,yaxis_max="dataMax"  )
    
        kline = Line(background_color="#FFF", width=1500, height=680)
        kline.add('Total Net', list(netall.index), list(netall.netDay.values),legend_top ='bottom')
        grid = Grid(width=1500, height=680)
        grid.add(line, grid_bottom='50%')
        grid.add(kline, grid_top='50%')
        page.add(grid)
        page.render('./echart.html')
        
    # 准备回测 
    def prepBackTest(self , startDt , endDt, totalMoney):
        
        # To do list:
        # Read Symbol - strategy list
        # set Symbol list 
        #从TXT上读取设置
            
        f2=open(r'./test.txt','r+')
        art = f2.readlines()
        for i in range(0,len(art)):
            
            b = art[i].replace('\r','').replace('\n','').split('#')
            Symbol = b[0]
            Stg = b[1]
            self.__stglist.set_value(Symbol,'Stg',Stg)
            fee = float(b[2])
            self.__stglist.set_value(Symbol,'fee', fee)
            feeUn = b[3]
            self.__stglist.set_value(Symbol,'feeUnit', feeUn)
            tradeUn = int(b[4])
            self.__stglist.set_value(Symbol,'tradeUnit', tradeUn)
            
            for j in range(5 , len(b)):
                Input = 'Input' + str(j - 4)
                self.__stglist. set_value(Symbol , Input , b[j] )

        f2.close()
        
        List = self.__stglist.index
        self.setSymlist (List.values)
        
        self.initialDB ()
        
        print ( 'Lists ready OvO!')
        
        # Check startDate endDate for each symbol
        
        sym = self.getSymlist()
        
        for Symbol in sym.Symbol :
            df = self.getData(Symbol)
            a = df.loc[df.date == startDt]
            
            if a.empty :
                dat = df.iloc[0].date
                self.__stglist.set_value(Symbol, 'startDate' , dat)
            else: 
                self.__stglist.set_value(Symbol, 'startDate' , startDt)
            
            b = df.loc[df.date == endDt ]
            if b.empty :
                dat = df.iloc[-1].date
                self.__stglist.set_value(Symbol, 'endDate' , dat)
            else: 
                self.__stglist.set_value(Symbol, 'endDate' , endDt)
                
        print ('Date Checked ^_^ ')
        
            
        # Set up timeline
        stgL = self.__stglist
        
        for Symbol in stgL.index :
            df = self.getData(Symbol)
            sd = stgL.loc[Symbol].startDate
            if sd == startDt:
                inde = df.loc[df.date == startDt].index
                indd = inde.values[0]
                inde2 = df.loc[df.date == endDt].index
                indd2 = inde2.values[0]
                
                print(indd,indd2)
                
                if inde2.empty:
                    indd2 = df.shape[0] - 1
                for i in range(indd , indd2 + 1):
                    dateA = df.iloc[i].date
                    self.__timeline.loc[self.__timeline.shape[0]] = [dateA]
                
                breakP = df.iloc[-1].date
                if breakP == endDt :
                    break
                else:
                    startDt = breakP
                    
            elif df.loc[df.date == startDt].empty == False:
                
                inde = df.loc[df.date == startDt].index
                indd = inde.values
                c =  df.iloc[range(indd + 1,df.shape[0])].date
                
                if c.empty:
                    break
                inde2 = df.loc[df.date == endDt].index
                indd2 = inde2.values
                
                if inde2.empty:
                    indd2 = df.shape[0] - 1
                    
                for i in range(indd + 1, indd2 + 1):
                    dateA = df.iloc[i].date
                    self.__timeline.loc[self.__timeline.shape[0]] = [dateA]
            
                breakP = self.__timeline.iloc[-1].Date
                
                if breakP == endDt :
                    break
                else:
                    startDt = breakP 
        
        print ('Timeline set  [=__=]')
        
        timeLine = self.__timeline
        for Symbol in stgL.index :
            SD = stgL.loc[Symbol].startDate
            indSD = timeLine.loc[timeLine.Date == SD].index.values
            
            self.__stglist.set_value(Symbol, 'indSD' , indSD)
                
            ED = stgL.loc[Symbol].endDate
            indED = timeLine.loc[timeLine.Date == ED].index.values
            
            self.__stglist.set_value(Symbol, 'indED' , indED)
        
        # Set up(prep) strategy for each Symbol
        stgL = self.__stglist
        for Symbol in stgL.index :
            stg = stgL.loc[Symbol].Stg
            print ('Getting ', stg , 'for' , Symbol ,'ready')
            exec('self.Pre{}(Symbol)'.format(stg))
            
        self.__date = self.__timeline.iloc[0].values[0]
        print ('The back test will start from' , self.getDate())
        
        self.initialMon( totalMoney , startDt)
    
    #回测！！！ 没有周期的版本    
    def backTest(self):
        timeLine = self.__timeline
        stgL = self.__stglist
        
        # run Back test
        for i in timeLine.index:
            date = self.getDate()
            
            for Symbol in stgL.index :
                ED = stgL.loc[Symbol].indED
                SD = stgL.loc[Symbol].indSD
                
                if i in range(int(SD) , int(ED) + 1):
                    stg = stgL.loc[Symbol].Stg
                    exec('self.Exe{}(date,Symbol)'.format(stg))
                elif i == ED + 1:
                    self.level(self.lastday (date , Symbol) , Symbol)
                    net2 = self.getNet(self.lastday (date , Symbol) , Symbol)
                    self.__net.set_value(date , Symbol , net2)
                    
                elif i > ED or i < SD:
                    self.nothingHap2(date , Symbol)
            
            self.setDate(self.nextday(date,Symbol))
        
        self.Analyse()
            
        self.plotNet()
     
    #回测！！！ 有周期的版本    
    def backTestP(self , period):
        timeLine = self.__timeline
        stgL = self.__stglist
        counter = 1
        
        # run Back test
        for i in timeLine.index:
            date = self.getDate()
            
            if i % period == 0 :               
                for Symbol in stgL.index :
                    ED = stgL.loc[Symbol].indED
                    SD = stgL.loc[Symbol].indSD
                
                    if i in range(int(SD) , int(ED)):
                        stg = stgL.loc[Symbol].Stg
                        exec('self.Exe{}(date,Symbol)'.format(stg))
                    elif i == ED:
                        self.level(self.lastday (date , Symbol), Symbol)
                        net2 = self.getNet(self.lastday (date , Symbol) , Symbol)
                        self.__net.set_value(date , Symbol , net2)
                        
                    elif i > ED or i < SD:
                        self.nothingHap2(date , Symbol)
            else:
                for Symbol in stgL.index :
                    ED = stgL.loc[Symbol].indED
                    SD = stgL.loc[Symbol].indSD
                
                    if i in range(int(SD) , int(ED) ):
                        self.nothingHap(date , Symbol)
                        net2 = self.getNet(self.lastday (date , Symbol) , Symbol)
                        self.__net.set_value(date , Symbol , net2)
                        
                    elif i == ED:
                        self.level(self.lastday (date , Symbol), Symbol)
                        net2 = self.getNet(self.lastday (date , Symbol) , Symbol)
                        self.__net.set_value(date , Symbol , net2)
                        
                    elif i > ED or i < SD:
                        self.nothingHap2(date , Symbol) 
            
            counter = counter + 1
            
            self.setDate(self.nextday(date,Symbol))
        
        self.Analyse()
            
        self.plotNet()
      
    # 算统计数据
    # 应该在 Plot之前运行
    # code 是卢青云的。。。。
    def Analyse(self):
        stgL = self.__stglist
        netall = self.__net
        netall['netDay'] = netall.apply(lambda x: x.sum(), axis=1)
        netall.to_csv('./ NetValues.csv',index=False,sep=',')
        
        print (netall )
        # pos = self.getPos()
    
          
        #Per symbol....
        for Symbol in stgL.index :
            stg = stgL.loc[Symbol].Stg
            SD = stgL.loc[Symbol].startDate
            ED = stgL.loc[Symbol].endDate
            nets = netall[Symbol]
            
            # total return
            total_return_rate =nets.iloc[-1]/nets.iloc[0] - 1
            # sharpe ratio
            total_days = len(nets)
            annual_std = (nets/nets.shift(1)-1).std()*np.sqrt(250)
            annual_return_rate= (total_return_rate+1) ** (250/total_days)-1
            sharpe_ratio= (annual_return_rate-0.04)/annual_std
              
            # max dd
            maxdd = 0
            localmax = nets.iloc[0]
            for i in range(len(nets)-1):
                if nets.iloc[i+1] > localmax:
                    localmax = nets.iloc[i+1]
                dd = (localmax - nets.iloc[i])/localmax
                if dd > maxdd:
                    maxdd = dd
            
            LN = []
            LN.append('========================= \n')
            LN.append('Symbol Name :' +  Symbol + '\n')
            LN.append('Use Strategy' + stg+ '\n')
            LN.append('From ' + str(SD) + ' To ' + str(ED) + '\n')
            LN.append('total return rate is %.2f%%  \n' %(total_return_rate*100))
            LN.append('annual return rate is %.2f%%  \n' %(annual_return_rate*100))
            LN.append('annual volatility is %.2f%% \n' % (annual_std*100))
            LN.append('sharpe ratio is %.2f  \n' % (sharpe_ratio))
            LN.append('max drawndown is %.2f  \n' % (maxdd))
            LN.append('========================= \n')
            
            Toli = ' '.join(LN)
            
            #输出单标的结果
            print (Toli)
            f2 = open(r'./Result' + Symbol + '.txt','a+')
            f2.write(Toli)
            f2.close()
            
            pos = self.getPos()
            poss = pos.loc[pos.Symbol == Symbol]
            poss.to_csv('./PositionRecord' + Symbol + '.csv',index=False,sep=',')
            
            rec = self.getRecord()
            recs = rec.loc[pos.Symbol == Symbol]
            recs.to_csv('./TransactionRecord' + Symbol + '.csv',index=False,sep=',')
            
        # Analys for Total net
        
        stg = stgL.loc[Symbol].Stg
        SD = stgL.loc[Symbol].startDate
        ED = stgL.loc[Symbol].endDate
        nets = netall['netDay']
        # total return
        total_return_rate =nets.iloc[-1]/nets.iloc[0] - 1
        # sharpe ratio
        total_days = len(nets)
        annual_std = (nets/nets.shift(1)-1).std()*np.sqrt(250)
        annual_return_rate= (total_return_rate+1) ** (250/total_days)-1
        sharpe_ratio= (annual_return_rate-0.04)/annual_std
  
    # max dd
        maxdd = 0
        Totmax = netall['netDay'] .iloc[0]
        for i in range(len(nets)-1):
            if nets.iloc[i+1] > Totmax :
                Totmax = nets.iloc[i+1]
            dd = (Totmax - nets.iloc[i])/Totmax
            if dd > maxdd:
                maxdd = dd
    
        LN = []
        LN.append('========================= \n')
        LN.append('Result summay for total \n')
        LN.append('From ' + SD + ' To ' + ED+ '\n')
        LN.append('total return rate is %.2f%%  \n' %(total_return_rate*100))
        LN.append('annual return rate is %.2f%%  \n' %(annual_return_rate*100))
        LN.append('annual volatility is %.2f%% \n' % (annual_std*100))
        LN.append('sharpe ratio is %.2f  \n' % (sharpe_ratio))
        LN.append('max drawndown is %.2f  \n' % (maxdd))
        LN.append('=========================\n')
            
        Toli = ' '.join(LN)
        
        #输出总结果
        print (Toli)
        f2 = open(r'./ResultTOT.txt','a+')
        f2.write(Toli)
        f2.close()
        
        stgL.to_csv('./Config.csv',index=False,sep=',')
    
    # 布林线策略装订参数 装填数据 布林线策略代码 BOL 大写
    # Input1 = N 均线周期
    # Input2 = b 偏移系数 通道宽度
    # 用前确保 已从 TXT 中读取 Input1，2 （prepBackTest）
    # 数据计算在这里完成
    def PreBOL (self , Symbol):
        
        df = self.getData(Symbol)
        stgL = self.__stglist
        N = stgL.loc[Symbol].Input1
        b = stgL.loc[Symbol].Input2
        
        N = int(N)
        b = float(b)
        
        self.setLastPos(Symbol , 0)
        self.setCost(Symbol, 0)
        self.setTranSign(Symbol, 0)
        
        data_cl = df['close']
        df['Upper'], df['avg'], df['lower'] = ta.BBANDS(data_cl, timeperiod = N, \
          nbdevup = b, nbdevdn = b, matype = 0)
        
        df.fillna(0 , inplace = True)
        
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        exec('self.BOL{} = df'.format(num.values[0]))
        
        print ('BolLine for', Symbol, 'is ready')
        
    # 为某一标的执行一天的布林线策略    注意是 单单一天的
    # 先根据昨天的信号交易 再生成 给明天的信号
    def ExeBOL(self, date , Symbol):
        stgL = self.__stglist
        b = stgL.loc[Symbol].Input2
        b = float(b)
        
        print ('BOLline',Symbol, date)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        _locals = locals()
        exec('df = self.BOL{} '.format(num.values[0]),globals(),_locals)
        df = _locals['df']
        
        i = df.loc[df['date'] == date].index
        date = df.iloc[i]['date'] .values[0]
        up = df.iloc[i]['Upper'].values[0]
        low = df.iloc[i]['lower'].values[0]
        price =  df.iloc[i]['close'].values[0]
        avg = df.iloc[i]['avg'].values[0]
            
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        # 信号交易一波
        self.signTrade(Symbol, date)
        
        if avg != 0 :
            
            # 回归均价 平仓
            if price >= avg * (1 - b/2)  and price <= avg * (1 + b/2):
                self.setTranSign(Symbol , 2)
                print ('level' ,date)
                        
            elif price > up and mon > 0:
                self.setTranSign(Symbol , 1)
                print ('Buy',  date , 1)
                        
            elif price < low and mon > 0:
                self.setTranSign(Symbol , -1)
                print ('Buy',  date , -1)
                        
            else:
                self.setTranSign(Symbol , 0)
                print ('Nothinghap' , date)
        else:
            self.setTranSign(Symbol , 0)
            print ('Nothinghap' , date)
            
        net2 = self.getNet(date , Symbol)
        self.__net.set_value(date , Symbol , net2)
    
    # ATR策略装订参数 装填数据 ATR策略代码 ATR 大写
    # Input1 = N 均线周期
    # Input2 = b 偏移系数 通道宽度
    # 用前确保 已从 TXT 中读取 Input1，2 （prepBackTest）
    # 数据计算在这里完成
    def PreATR (self , Symbol):
        
        df = self.getData(Symbol)
        stgL = self.__stglist
        N = stgL.loc[Symbol].Input1
        b = stgL.loc[Symbol].Input2
        
        N = int(N)
        b = float(b)
        
        self.setLastPos(Symbol , 0)
        self.setCost(Symbol, 0)
        self.setTranSign(Symbol, 0)
         
        data_cl = df['close']
        df['avg'] = ta.MA(np.array(data_cl), timeperiod= N, matype=0) 
        df['atr'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod= N)
        
        df.fillna(0 , inplace = True)
        
        df['Upper'] = df['atr'] * (1 + b)
        df['lower'] = df['atr'] * (1 - b)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        exec('self.ATR{} = df'.format(num.values[0]))
        
        print ('ATR for', Symbol, 'is ready')
        
    # 为某一标的执行一天的ATR策略    注意是 单单一天的
    # 先根据昨天的信号交易 再生成 给明天的信号
    def ExeATR(self, date , Symbol):
        
        stgL = self.__stglist
        b = stgL.loc[Symbol].Input2
        b = float(b)
        
        print ('ATR', Symbol, date)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']

        _locals = locals()
        exec('df = self.ATR{} '.format(num.values[0]),globals(),_locals)
        df = _locals['df']
        
        i = df.loc[df['date'] == date].index
        date = df.iloc[i]['date'].values[0]
        up = df.iloc[i]['Upper'].values[0]
        low = df.iloc[i]['lower'].values[0]
        price =  df.iloc[i]['close'].values[0]
        avg = df.iloc[i]['avg'].values[0]
        
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        # 信号交易一波
        self.signTrade(Symbol, date)
    
        if avg != 0 :
            
            # 回归均价 平仓
            if price >= avg * (1 - b/2)  and price <= avg * (1 + b/2):
                self.setTranSign(Symbol , 2)
                print ('level' , Symbol ,date)
                     
            elif price > up and mon > 0:
                self.setTranSign(Symbol , 1)
                print ('Buy', Symbol, date , 1)
                        
            elif price < low and mon > 0:
                self.setTranSign(Symbol , -1)
                print ('Buy', Symbol,  date , -1)
                        
            else:
                self.setTranSign(Symbol , 0)
                print ('Nothinghap', Symbol , date)
        else:
            self.nothingHap (date, Symbol)
            print ('Nothinghap' , Symbol, date)

        net2 = self.getNet(date , Symbol)
        self.__net.set_value(date , Symbol , net2)
    
    # 老的均线突破策略
    # 不需要用 backTest方法 直接能跑
    # 测试用
    def avgLine (self , Symbol , N , b):
        df = self.getData(Symbol)
        
        data_cl = df['close']
        df['avg'] = ta.MA(np.array(data_cl), timeperiod= N, matype=0) 
        
        df['Upper'] = df['avg'] * (1 + b)
        df['lower'] = df['avg'] * (1 - b)
        df.fillna(0 , inplace = True)
        
        # 控制跑的天数 
        for i in range(100):
            date = df.iloc[i]['date'] 
            up = df.iloc[i]['Upper']
            low = df.iloc[i]['lower']
            price =  df.iloc[i]['close']
            avg = df.iloc[i]['avg']
            
            moneyl = self.getMoney(Symbol)
            mon = moneyl.iloc[-1]['Money']
            
            #print i ,date
            
            if avg != 0 :
                if self.cutdown(date , Symbol ) == False :
                    if price >= avg * (1 - b/2)  and price <= avg * (1 + b/2):
                        self.level( date,Symbol )
                        #print 'level' ,date
                        
                    elif price > up and mon > 0:
                        dvol = self.getDvol(Symbol, date)
                        self.buy(Symbol, dvol, date , 1)
                        #print 'Buy', dvol, date , 1
                        
                    elif price < low and mon > 0:
                        dvol = self.getDvol(Symbol, date)
                        self.buy(Symbol, dvol, date , -1)
                        #print 'Buy', dvol, date , -1
                        
                    else:
                        self.nothingHap (date, Symbol)
                        #print 'Nothinghap' , date
                else: 
                    print ('CUTDOWN',date)
            else:
                 self.nothingHap (date, Symbol)
                 #print 'Nothinghap' , date
            
            net2 = self.getNet(date , Symbol)
            self.__net.set_value(date , Symbol , net2)
     
    # 均线突破策略装订参数 装填数据 均线突破策略代码 AVG 大写
    # Input1 = N 均线周期
    # Input2 = b 偏移系数 通道宽度
    # 用前确保 已从 TXT 中读取 Input1，2 （prepBackTest）
    # 数据计算在这里完成
    def PreAVG (self , Symbol):
        stgL = self.__stglist
        N = stgL.loc[Symbol].Input1
        b = stgL.loc[Symbol].Input2
        
        N = int(N)
        b = float(b)
        
        self.setLastPos(Symbol , 0)
        self.setCost(Symbol, 0)
        self.setTranSign(Symbol, 0)
        
        df = self.getData(Symbol)
        
        data_cl = df['close']
        df['avg'] = ta.MA(np.array(data_cl), timeperiod= N, matype=0) 
        
        df['Upper'] = df['avg'] * (1 + b)
        df['lower'] = df['avg'] * (1 - b)
        df.fillna(0 , inplace = True)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        exec('self.AVG{} = df'.format(num.values[0]))
        
        print ('AVG for', Symbol, 'is ready')
        
    # 为某一标的执行一天的均线突破策略    注意是 单单一天的
    # 先根据昨天的信号交易 再生成 给明天的信号   
    def ExeAVG(self , date , Symbol):
        stgL = self.__stglist
        b = stgL.loc[Symbol].Input2
        b = float(b)
        
        print( 'AVG', Symbol, date)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        _locals = locals()
        exec('df = self.AVG{} '.format(num.values[0]),globals(),_locals)
        df = _locals['df']
        
        i = df.loc[df['date'] == date].index
        date = df.iloc[i]['date'].values[0] 
        up = df.iloc[i]['Upper'].values[0]
        low = df.iloc[i]['lower'].values[0]
        price =  df.iloc[i]['close'].values[0]
        avg = df.iloc[i]['avg'].values[0]
            
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
        
        # 信号交易一波
        self.signTrade(Symbol, date)
            
        if avg != 0 :
            # 回归均价 平仓
            if price >= avg * (1 - b/2)  and price <= avg * (1 + b/2):
                self.setTranSign(Symbol , 2)
                print ('level' , Symbol ,date)
                        
            elif price > up and mon > 0:
                self.setTranSign(Symbol , 1)
                print ('Buy', Symbol,  date , 1)
                        
            elif price < low and mon > 0:
                self.setTranSign(Symbol , -1)
                print ('Buy', Symbol,  date , -1)
                        
            else:
                self.setTranSign(Symbol , 0)
                print ('Nothinghap' , Symbol, date)
        else:
            self.setTranSign(Symbol , 0)
            print ('Nothinghap' , Symbol, date)
            
        net2 = self.getNet(date , Symbol)
        self.__net.set_value(date , Symbol , net2)
    
    # MACD策略装订参数 装填数据 MACD策略代码 MACD 大写
    # Input1 = k1 短周期
    # Input2 = k2 长周期
    # Input2 = N 均线周期
    # 用前确保 已从 TXT 中读取 Input1，2，3 （prepBackTest）
    # 数据计算在这里完成
    def PreMACD (self , Symbol):
        
        stgL = self.__stglist
        k1 = stgL.loc[Symbol].Input1
        k2 = stgL.loc[Symbol].Input2
        N = stgL.loc[Symbol].Input3
        N = int(N)
        k1 = int(k1)
        k2 = int(k2)
        
        self.setLastPos(Symbol , 0)
        self.setCost(Symbol, 0)
        self.setTranSign(Symbol, 0)
        
        df = self.getData(Symbol)
        
        data_cl = df['close']
        df['avg'] = ta.MA(np.array(data_cl), timeperiod= N, matype=0) 
        df['DIFF'], df['DEA'], df['MACD'] =  ta.MACD(df['close'], fastperiod= k1, \
          slowperiod= k2, signalperiod= N)
        
        df.fillna(0 , inplace = True)
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        exec('self.MACD{} = df'.format(num.values[0]))
        
        print ('MACD for', Symbol, 'is ready')
        
    # 为某一标的执行一天的MACD策略    注意是 单单一天的
    # 先根据昨天的信号交易 再生成 给明天的信号   
    def ExeMACD(self , date , Symbol):
        
        stgL = self.__stglist
        
        print ('MACD', Symbol, date)
        
        sym = self.getSymlist()
        num = sym.loc[sym.Symbol == Symbol]['Num']
        
        _locals = locals()
        exec('df = self.MACD{} '.format(num.values[0]),globals(),_locals)
        df = _locals['df']
        
        i = df.loc[df['date'] == date].index
        pos1 = self.getLastPos(Symbol)
        date = df.iloc[i]['date'] .values[0] 
        DIF = df.iloc[i]['DIFF'].values[0] 
        MACD =  df.iloc[i]['MACD'].values[0] 
        avg = df.iloc[i]['avg'].values[0] 
            
        moneyl = self.getMoney(Symbol)
        mon = moneyl.iloc[-1]['Money']
            
        self.signTrade(Symbol, date)    
        
        if avg != 0 :
            if DIF > 0 :
                if pos1 < 0:
                    self.setTranSign(Symbol , 2)
                    print ('level' , Symbol ,date  ) 
                    
                if MACD > 0 and mon > 0:
                    self.setTranSign(Symbol , 1)
                    print ('Buy', Symbol,date , 1)
                    
            elif DIF < 0:    
                if pos1 > 0:
                    self.setTranSign(Symbol , 2)
                    print ('level' , Symbol,date)
                    
                if MACD < 0  and mon > 0:
                    self.setTranSign(Symbol , -1)
                    print ('Buy', Symbol,date , -1 )   
                    
            else:
                self.setTranSign(Symbol , 0)
                print ('Nothinghap' , Symbol, date)
        else:
            self.setTranSign(Symbol , 0)
            print ('Nothinghap' , Symbol, date)
            
        net2 = self.getNet(date , Symbol)
        self.__net.set_value(date , Symbol , net2)