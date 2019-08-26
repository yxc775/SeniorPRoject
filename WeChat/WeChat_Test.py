import itchat
import time
import os
import sys

TEXT = itchat.content.TEXT
print(sys.path)
parent_path = os.path.dirname(sys.path[0])
if parent_path not in sys.path:
    sys.path.append(parent_path)
print(sys.path)
from stockDB import stockDB

# Database location
database = os.path.realpath('..') + '\\Database\\demo.db'
print(database)

# Report location
report = os.path.realpath('..') + '\\Algorithm\\report'

#from itchat import content

def login():
    try:
        print("Running: WeChat_Test")
        isRunning = True
        db = stockDB(database)
        print("Database opened.")
    except PermissionError as pe:
        print("Login timeout. No permission given.")
        
    def current_subscriber():
        user_list = db.get_user_name() # Retrieve all user names in database. Assume that all current user exist in both DB and wechat.
        user_info = []
        for user in user_list:
            if user[3] != '': # Middle name not empty.
                user_name = user[1] + '_' + user[3] + '_' + user[2]
            else:
                user_name = user[1] + '_' + user[2]
            u_id_name = [user[0], user_name]
            user_info.append(u_id_name)
        return user_info
    
    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):
        #itchat.send('auto replying', toUserName=msg['FromUserName']) # WORKS, IMPORTANT METHOD FOR FILE REPLY. WILL BE IMPLEMENTED.
        #print(msg[itchat.content.TEXT])
        #return msg.text # TEST if itchat can receive autoreply. WORKS.
        print(msg.text)
        
        if 'help' in msg[TEXT] or 'Help' in msg[TEXT] or 'HELP' in msg[TEXT]:
            #wechat_auto_msg() #PRINT TEST
            return wechat_auto_msg('automsg\\helpReply.txt')
        
        if 'method' in msg[TEXT] or 'Method' in msg[TEXT] or 'METHOD' in msg[TEXT]:
            
            db_temp = stockDB(database)
            user_list = db_temp.get_user_name()
            user_info = []
            for user in user_list:
                if user[3] != '': # Middle name not empty.
                    user_name = user[1] + '_' + user[3] + '_' + user[2]
                else:
                    user_name = user[1] + '_' + user[2]
                u_id_name = [user[0], user_name]
                user_info.append(u_id_name)
            for u in user_info:
                friend = itchat.search_friends(name ='{id}'.format(id = u[0]))[0]['UserName']
                u.append(friend)
            
            for user_id_un in user_info:
                if msg['FromUserName'] == user_id_un[2]:
                        method = db_temp.get_user_prefer_method(uid = user_id_un[0])
            #print(method)
            return "Your current method is: " + method[0][1]
        
        if 'stock' in msg[TEXT] or 'Stock' in msg[TEXT] or 'STOCK' in msg[TEXT]:
            db_temp = stockDB(database)
            user_list = db_temp.get_user_name()
            user_info = []
            for user in user_list:
                if user[3] != '': # Middle name not empty.
                    user_name = user[1] + '_' + user[3] + '_' + user[2]
                else:
                    user_name = user[1] + '_' + user[2]
                u_id_name = [user[0], user_name]
                user_info.append(u_id_name)
            for u in user_info:
                friend = itchat.search_friends(name ='{id}'.format(id = u[0]))[0]['UserName']
                u.append(friend)
            
            for user_id_un in user_info:
                if msg['FromUserName'] == user_id_un[2]:
                        stock = db_temp.get_user_stock(uid = user_id_un[0])
            #print(stock)
            stock_string = ''
            for stock_info in stock:
                stock_string += (stock_info[1] + '\n')
            print(stock_string)
            return "Your current subscribed share(s) are:\n" + stock_string
    
        if 'report ' in msg[TEXT] or 'Report ' in msg[TEXT] or 'REPORT ' in msg[TEXT]:
            db_temp = stockDB(database)
            user_list = db_temp.get_user_name()
            user_info = []
            for user in user_list:
                if user[3] != '': # Middle name not empty.
                    user_name = user[1] + '_' + user[3] + '_' + user[2]
                else:
                    user_name = user[1] + '_' + user[2]
                u_id_name = [user[0], user_name]
                user_info.append(u_id_name)
            for u in user_info:
                friend = itchat.search_friends(name ='{id}'.format(id = u[0]))[0]['UserName']
                u.append(friend)
            #print(user_info)
            #print(msg['FromUserName'])
            for user_id_un in user_info:
                if msg['FromUserName'] == user_id_un[2]:
                    print("User found, sending current report...")
                    send_result = itchat.send('@fil@' + report + '\\{name}_{id}.html'.format(name = user_id_un[1], id = user_id_un[0]), toUserName=msg['FromUserName'])
                    print(send_result)
            
    '''
    Subscribe information.
    '''
    @itchat.msg_register('Friends')
    def subscribe(msg):
        itchat.add_friend(**msg[TEXT])
        itchat.send_msg(wechat_auto_msg('automsg/newSubscribe.txt'))

    def after_run():
        while isRunning:
            auto_report() # TEST alias date.
        return None
    
    def delete_user():
        db.delete_user()
    
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
    
    """
    At the specific time, send report automatically to user.
    Assume that all users' database id is stored as WeChat NickName
    Time of sending report is handled by outer functions.
    """
    def auto_report():
        user_info = current_subscriber()
        #print(user_info)
        # For every users whose id in uid_list, locate their UserName in WeChat and send them report.
            #itchat search ID as NickName, which is assumed to be database user id
        for u in user_info:
            friend = itchat.search_friends(name ='{id}'.format(id = u[0]))[0]['UserName']
            #print(friend)
            u.append(friend)
            print('Itchat send file return: ')
            print(itchat.send('@fil@' + report + '\\{name}_{id}.html'.format(name = u[1], id = u[0]), toUserName = u[2]))
        time.sleep(60)
            #wechat_UserNmae_list.append(friend)
        #print(user_info)
        
        
            #using the found ID, send the report of the specific date. Path of report to be found.
        
        
    
    itchat.auto_login(hotReload = True, picDir='QR.png') #This is for auto-login QR storage. No need in here, but keep for reference if needed.
    itchat.run(blockThread = False)
    after_run()
    
        #itchat.logout()
    
if __name__ == "__main__":
    login()
