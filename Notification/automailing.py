import gmailReader as Reader
import gmailSender as Sender
import time
import SQLconnect
import datetime
import os
import glob

dataFolder = os.path.realpath('..') + "/Algorithm/report/*.html"
hisFolder = os.path.realpath('..') + "/Algorithm/hist/*.html"

managerAccount = "yxc775@case.edu"
RegisterCode= "HKWZ35"

def pullMemberListFromDB(members):
    users = SQLconnect.getdb().get_user_all()
    with open(members, 'w') as fp:
        for i in range(0,len(users)):
            fp.write(str(users[i][6]) +" " + str(users[i][0]) + "\n")

def updateMailingList(members):
    memberlist = []
    with open(members) as fp:
        line = fp.readline()
        while line:
            memberlist.append(line)
            line = fp.readline()
    return memberlist

def startServe(checkingAdmPeriod,checkUserDemandTime, start_time, finaltime, members):

    running = True
    updateStatTime = start_time
    repond_time = start_time
    memberlist = updateMailingList(members)

    while running:
        #if receviing STOP command from manager account
            # running = false
        actions = None
        #Read User info, pull out user options
        #Scan emails based on send date
        if time.time() >= updateStatTime:
            running = checkCommand(updateStatTime,managerAccount,checkingAdmPeriod)
            updateStatTime += checkingAdmPeriod
        if time.time() >= repond_time:
            pullMemberListFromDB(members)
            memberlist = updateMailingList(members)
            sendReports(memberlist)
            searchForNewRegistration(members,checkUserDemandTime)
            actions = checkOnUsers(memberlist,checkUserDemandTime)
            repond_time += checkUserDemandTime
            if len(actions) != 0:
                respondUser(actions)


        #Time Limit on how long this program can run
        if (time.time() >= finaltime):
            running = False
            #Send a message to manager account
            print("Program Done! Time Limit Reached")

def sendReports(members):
    list = glob.glob(dataFolder)
    for i in range(0,len(list)):
        for j in range(0,len(members)):
            idavail = int(list[i].split("/")[-1].split("_")[-1].split(".")[0])
            if idavail == int(members[j].split(" ")[-1]) and len(members[j].split(" ")[0]) > 5:
                today = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
                print("Sending Reports to " + members[j].split(" ")[0])
                Sender.sendEmail("Here is your update from Stock price monitor on " + today ,"Please see attachment",members[j].split(" ")[0],list[i])

def sendhisTo(member, hist):
    list = glob.glob(hisFolder)
    for i in range(0, len(list)):
        idavail = int(list[i].split("/")[-1].split(" ")[0].split("_")[-1])
        dates = list[i].split("/")[-1].split(" ")[1].split(".")[0]
        if idavail == int(member.split(" ")[-1]) and dates in hist:
            today = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            Sender.sendEmail(
                            "Here is your history info from " + dates + " from Stock price monitor on " + today,
                            "Please see attachment", member.split(" ")[0], list[i])

def searchForNewRegistration(members,checkUserDemandTime):
    since = int(time.time() - checkUserDemandTime)
    t = time.localtime(since)
    str = convertToReadFormat(t)
    data,con = Reader.searchBySubjectOn(str,RegisterCode)
    bodys = Reader.getbody(data,con)
    for i in range(0,len(bodys)):
        bodytext = bodys[i].decode("utf-8")
        tlist = bodytext.split("\r\n")
        email = None
        ID = None
        gender = None
        fname = None
        lname = None
        stocklist = None
        pmethod = None
        for i in range(0,len(tlist)):
            substr = tlist[i].split(" ")
            for j in range(0, len(substr)):
                if substr[j] == "Email:":
                    email = substr[j + 1]
                if substr[j] == "ID:":
                    ID = substr[j+1]
                if substr[j] == "Gender(M/FM):":
                    gender = substr[j+1]
                    if gender == "M":
                        gender = 0
                    else:
                        gender = 1
                if substr[j] == "Name:":
                    fname = substr[j + 1]
                    if len(substr) > 2:
                        lname = substr[j+2]
                    else:
                        lname = "N/A"
                if substr[j] == "Stock:":
                    stocklist = substr[j+1:len(substr)]
                if substr[j] == "Method:":
                    pmethod = substr[j+1:len(substr)]
                if email is not None and ID is not None and stocklist is not None and pmethod is not None :
                    insertnewUser(members, fname, lname, email, ID, gender,stocklist,pmethod)

def connectUserMembers(id,stocklist):
    db = SQLconnect.getdb()
    for i in range(0,len(stocklist)):
        try:
            db.insert_user_stock(userid=id,stockid= int(stocklist[i]))
        except:
            print("stock insertion failed")





def insertnewUser(memberFile, fname, lname, email, ID, gender,stocklist, pmethod):
    database = SQLconnect.getdb()
    try:
        database.insert_user(user_id=int(ID),first_name=fname,last_name=lname,email=email,gender=gender)
        database.edit_user_prefer_method(uid= int(ID),newmethodid=int(pmethod[0]))
        connectUserMembers(ID, stocklist)

    except:
        print("...")
    pullMemberListFromDB(memberFile)

def deleteUser(userID):
    db = SQLconnect.getdb()
    try:
        db.edit_user_info(uid=userID,newEmail="")
    except:
        print("delete fail")
    pullMemberListFromDB("memberList")


def respondUser(actions):
    for x in actions:
        if x[0] == 1:
            Sender.sendEmail("We received your notification","Manager will contact you within 24 hours, thanks for you patience!","419873387chen@gmail.com","")

        elif x[0] == 2:
            hist = x[1]
            sendhisTo(x[2], hist)

        elif x[0] == 3:
            userinfo = x[2]
            deleteUser(userinfo.split(" ")[1])
            Sender.sendEmail("Thank you, you are removed from our subscription list", "We are sorry to hear your leave\n Best", userinfo.split(" ")[0],"")

        elif x[0] == 4:
            settingOptions = x[1]
        elif x[0] == 5:
            Sender.sendEmail("We received your registration",
                             "Your email is added into mailing list, thank you",
                             x[1], "")


def checkOnUsers(members,checkUserDemandTime):
    actions = []
    for mem in members:
        if mem.strip() != "":
            print("is Checking User " + mem)
            actions.append(checkUserhelper(time.time() - checkUserDemandTime, mem))
    return actions


def daysToSec(days):
    return days * 24 * 60 * 60

def hoursToSec(hours):
    return hours * 60 * 60

def minutes(min):
    return min * 60

def checkUserhelper(since, userstring):
    action = 0
    since = int(since)
    additionalInfo = None
    useremail = userstring.split(" ")[0]
    if len(useremail) > 4:
        t = time.localtime(since)
        str = convertToReadFormat(t)

        data,con = Reader.searchBySenderOn(str,useremail)
        if len(data) > 0:
            bodyCodes = Reader.getbody(data,con)
            for i in range(0,len(bodyCodes)):
                stringtext = bodyCodes[i].decode("utf-8")
                #start to encoding which context match with which action
                if "NEED HELP" in stringtext:
                    action = 1
                elif "NEED REPORT ON" in stringtext:
                    action = 2
                    additionalInfo = stringtext.split(" ")[-1]
                elif "NEED CANCEL" in stringtext:
                    action = 3
                elif "CHANGES SETTING" in stringtext:
                    action = 4
                    additionalInfo = stringtext
                    #check through list for stop code
                    #update check
                    #no stopping command
    return action,additionalInfo,userstring


def checkCommand(nextcheck,manager,checkCommandPeriod):
    newintcheck = int(nextcheck)
    t = time.localtime(newintcheck - checkCommandPeriod)
    str = convertToReadFormat(t)
    print("is Checking Manager")
    data,con = Reader.searchBySenderOn(str,manager)
    shouldrun = True
    if(len(data) > 0):
        stringtext = Reader.getbody(data,con)
        for x in range(0,len(stringtext)):
            if b"STOP" in stringtext[x]:
                print("Service Stop!!!")
                shouldrun = False;
        #check through list for stop code
        #update check
        #no stopping command
    return shouldrun

def convertToReadFormat(t):
    month = ""
    if(t.tm_mon == 1):
        month = "Jan"
    elif(t.tm_mon == 2):
        month = "Feb"
    elif(t.tm_mon == 3):
        month = "Mar"
    elif(t.tm_mon == 4):
        month = "Apr"
    elif(t.tm_mon == 5):
        month = "May"
    elif(t.tm_mon == 6):
        month = "Jun"
    elif(t.tm_mon == 7):
        month = "Jul"
    elif(t.tm_mon == 8):
        month = "Aug"
    elif(t.tm_mon == 9):
        month = "Sep"
    elif(t.tm_mon == 10):
        month = "Oct"
    elif(t.tm_mon == 11):
        month = "Nov"
    else:
        month = "Dec"
    return "{}-{}-{}".format(t.tm_mday,month,t.tm_year)


def main():
    members = "memberList"
    pullMemberListFromDB(members)
    start_time = time.time()
    #userinfo  retrieved from database
    now = time.localtime(start_time)
    print("the now time is " + str(now))
    print(start_time)
    serverRunTime = daysToSec(10)
    startServe(60,60,start_time,start_time + serverRunTime,members)
    return 0


if __name__ == '__main__':
    main()
