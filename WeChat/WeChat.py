'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
Author: Yunxi Kou - yxk383
Feb-15: Initial design.
Feb-22: Address the itchat.run() deadlock.
Mar-1: Add basic reply function and 
'''
from itchat.content import *
import time
import itchat
from itchat.components import hotreload

'''
Parameters
'''
isRunning = True # Flag for auto-reply and report sending.

'''
Retrieve WeChat friends and reply information.
The subscribed users are recorded on a .txt list.
'''
def user_retrieve():
    friendslist = itchat.get_friends(update=True)[1:]
    return friendslist

'''
Auto-reply for interactions.
@param msg: the message intercepted by itchat.msg_register(). In this function, only text messages should be reacted.
'''
@itchat.msg_register(TEXT, isFriendChat = True)
def text_reply(msg):
    #TEST
    #return msg.text #TEST: Immediate return the same message back to user.
    print(msg.text)
    
    friend = itchat.search_friends(name = u'毕业项目测试号') # TEST by sending testing account a confirm message.
    print(friend)
    username = friend[0]['UserName'] # Note, 4/26: this is the way to pull FRIEND's wechat sending ID. This is random every time.
    
    print(itchat.send(msg = 'Test reply', toUserName = username))
    
    if 'help' in msg[TEXT] or 'Help' in msg[TEXT] or 'HELP' in msg[TEXT]:
        #wechat_auto_msg() #PRINT TEST
        return wechat_auto_msg('automsg/helpReply.txt')
    
    if 'uc' in msg[TEXT] or 'UC' in msg[TEXT]:
        unsubscribe()
        return "Unsubscribe successful" #PLACEHOLDER
        
    if 'method' in msg[TEXT] or 'Method' in msg[TEXT] or 'METHOD' in msg[TEXT]:
        return "Print the current analysis method." #PLACEHOLDER
    
    if 'stock' in msg[TEXT] or 'Stock' in msg[TEXT] or 'STOCK' in msg[TEXT]:
        return "This is the stock information." #PLACEHOLDER
    
    if 'report ' in msg[TEXT] or 'Report ' in msg[TEXT] or 'REPORT ' in msg[TEXT]:
        date = msg.text.split()[1]
        print(date)
        send_report(date)
'''
Subscribe information.
'''
@itchat.msg_register('Friends')
def subscribe(msg):
    itchat.add_friend(**msg[TEXT])
    itchat.send_msg(wechat_auto_msg('automsg/newSubscribe.txt'))
    
    
'''
Read and return the helper message defined in txt files in the same folder.
@param filename: The txt file storing the text to be returned.
'''
def wechat_auto_msg(filename):
    file = open(filename, mode = 'r')
    msg = file.read()
    file.close()
    #print(help_msg) #PRINT TEST
    return msg

'''
Retrieve stock data analysis.
'''
def stock_data():
    return None #PLACEHOLDER

'''
Unsubscribe.
'''
def unsubscribe():
    print('Unsubscribed.') #PLACEHOLDER

'''
WeChat text sending.
The indication will be generated and sent automatically once fluctuation occurs.
'''
def send_msg():
    return None #PLACEHOLDER

'''

'''
def send_report(date):
    # TEST
    friend = itchat.search_friends(name = u'杉杉')
    print(friend)
    username = friend[0]['UserName']
    print('The user name is: ')
    print(username)
    itchat.send_file('test.txt', '@56859a2cc5266ad423adb01f68d8e980aca8b23a04890a0fb60c7a42e1e4b415') # TEST
    
'''

'''
def search_friend(Name):
    pass

'''
The operations after login.
'''
def after_login():
    #itchat.send_msg("Hello World", 'filehelper') #TEST
    #print(itchat.search_friends()) # Return account information.
    #print(itchat.send_msg('test.txt', '@56859a2cc5266ad423adb01f68d8e980aca8b23a04890a0fb60c7a42e1e4b415')) # TEST SENDING FILE TO FRIEND.
    print('Login successful as ' + itchat.search_friends()['NickName'])
   
    
'''
The function that executes after auto reply is run, and handles operations apart from auto reply.
The while loop ensures the run of program body. The process terminates when the while loop ends.
'''
def after_run():
    while isRunning:
        pass
    return None #PLACEHOLDER
    
'''
Login and autoreply.
@param hotReload = True: After first login by scanning QR code, 
@param loginCallback: the function that calls back after login completion.
'''
print('Running WeChat.py')
itchat.auto_login(loginCallback = after_login)
itchat.run(blockThread = False) # Start auto reply without blocking thread.
after_run()

itchat.logout() # Log out the WeChat when program terminates.