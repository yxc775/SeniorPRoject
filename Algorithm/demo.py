# -*- coding: utf-8 -*-
"""
Created on Wed May  1 16:25:49 2019

@author: Lishan Jin
"""
import gen 
import dataprep
<<<<<<< HEAD
from WeChat import WeChat_Test
=======
import time
>>>>>>> dbc114daab9c794476255db58eb7a26893f57cd8


def oneday1(date):
    dataprep.prepData(date) 
    gen.genReport1(date)
    
def oneday2(date):
    dataprep.prepData(date) 
    gen.genReport2(date)

date = '2018-06-04'
<<<<<<< HEAD
oneday1(date)
date = '2018-06-05'
oneday2(date)
WeChat_Test.login()
=======
date2 = '2018-06-05'

if __name__ == '__main__':
    oneday1(date)
    print("Pause")
    time.sleep(80)
    oneday2(date2)
>>>>>>> dbc114daab9c794476255db58eb7a26893f57cd8
