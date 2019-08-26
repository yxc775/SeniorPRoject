"""
#######################################################################################################################################
stockDB Database wrapper.
The SQLite method wrapper with quick DB creation, insert and search methods.
The database schema follows the schema designed before. (Maybe changed in practice, but any change will provided here).
Some methods take reference from goldsborough from github:
https://gist.github.com/goldsborough/c973d934f620e16678bf
Apr. 19: Finalize: fill in several methods.
        Change the format of SQLite. Now all None inputs with format will be automatically transferred to empty string ('') without explicit definition.
        -The fmt.format references the code of Antonio Cuni from ActiveState Code:
        http://code.activestate.com/recipes/577227-string-formatter-that-renders-none-values-as-empty/
        For those which require integer inputs:
        -The id and user.gender, whenever were input, will be not None and therefore have no worry.
        -The user.prefer_method_id, though, can be input as None and therefore generates typeError. Detail in README.
        Solve a bug in insert_user that the prefer_method_id can be None while None id can raise exception.
        Resolve a typo in function transaction_data_table

Apr. 5 : Address the SQLite query language glitch that is responsible for table insert integrity error.
        The database schema has a slight modification. For each "new table" created to include the transaction data of 
            a specific stock, the primary key is now changed from record date to index (ind), to prevent a not allowed,
            yet possible scenario to create exception that two records from a same stock have the same transaction date.
        Additionally, a new attribute Name is added to all such tables. The name is the stock name, as a foreign key to table stock_id.
            This table serves for security purpose, since in theory each record in a single transaction table should belong to the same
            stock, and therefore have the same name.
        An "insert method" function is created for quick analysis method insert in the database.
        Finish the function for transaction table. Now the total number of data in transaction table can be no more than 200.
            If more data exists in insertion, the database will remove the data with the least index.
        Add a function that can check if all stocks (in name) in table stock_info has a corresponding transaction table.
        Non-structural change: all function notes and multi-line comments now use double-quotation mark in order to separate from
                                multi-line SQLite query langage, which still maintains single quotation mark.
                                
        
        

Mar.29 : Add delete for user, creation of stock data and analysis, and .csv reading.
        Modify database shchema, two more relationship tables, stock_trade and stock_analysis are added.
        stock_trade: for each time a stock trade record is created, a new table recording the trades of the stock is added.
                    The stock_trade provides a relationship between each stock and its trade date.
        stock_analysis: similarly, an analysis table will be created for each stock. This table is their relationship.

Mar.22 : Base wrapper design.

@author: Yunxi Kou - yxk383
########################################################################################################################################
"""
import sqlite3
import csv
from string import Formatter

class EmptyNoneType(object):

    def __nonzero__(self):
        return False

    def __str__(self):
        return ''

    def __getattr__(self, name):
        return EmptyNone

    def __getitem__(self, idx):
        return EmptyNone
    

EmptyNone = EmptyNoneType()

class EmptyNoneFormatter(Formatter):

    def get_value(self, field_name, args, kwds):
        v = Formatter.get_value(self, field_name, args, kwds)
        if v is None:
            return EmptyNone
        return v
    
fmt = EmptyNoneFormatter()

class stockDB:
    
    """
    Constructor:
    
    The constructor stores the following when created:
    1. conn: the connection between instance and SQLite .db file
    2. curs: the cursor for operating database.
    
    The database can be opened in the following 3 ways:
    1. Use constructor and pass a valid .db file name.
    2. Use empty constructor and use open() method with a valid .db file name.
    3. Use empty constructor and use new() method to create a new stockDB database.
    """
    def __init__(self, dbName = None):
        self.conn = None
        self.curs = None
        
        if dbName:
            self.open(dbName)
    """
    The method that opens an existing database.
    @param name: .db file name to be opened.
    """
    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.curs = self.conn.cursor()
            self.conn.execute("PRAGMA foreign_keys = 1") # Allows foreign key check.
            
        except sqlite3.Error as dbe:
            print("Error connecting to database.")
            print("Error code: " + dbe)
    
    """
    Create a new stockDB database file.
    @param name: database name to be created.
    """
    def new(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.curs = self.conn.cursor()
            """
            method
            Apr. 19: Method with id 0 is preoccupied as 'Undetermined' to solve None method type conflict.
            """
            self.curs.execute('DROP TABLE IF EXISTS method')
            self.curs.execute(
                '''
                CREATE TABLE IF NOT EXISTS method (
                id INT PRIMARY KEY NOT NULL,
                name CHAR(20) NOT NULL,
                description text
                )
                ''')
            self.curs.execute(
                '''
                INSERT INTO method VALUES (0, 'Undetermined', 'The reserved method slot for users who yet determine analysis methods')
                ''')
            """
            user
            """
            self.curs.execute('DROP TABLE IF EXISTS user')
            self.curs.execute(
                '''
                CREATE TABLE IF NOT EXISTS user (
                id INT PRIMARY KEY NOT NULL,
                first_name CHAR(20) NOT NULL,
                middle_name CHAR(20),
                last_name CHAR(20) NOT NULL,
                gender INT NOT NULL,
                wechat_id CHAR(20),
                email CHAR(30),
                prefer_method_id INT,
                FOREIGN KEY(prefer_method_id) REFERENCES method(id)
                )
                ''')
            self.conn.commit()

            """
            report
            """
            self.curs.execute('''DROP TABLE IF EXISTS report''') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
            self.curs.execute(
                '''
                CREATE TABLE IF NOT EXISTS report (
                id INT PRIMARY KEY NOT NULL,
                user_id INT NOT NULL,
                date INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                )
                ''')

            """
            stock_info
            """
            self.curs.execute('''DROP TABLE IF EXISTS stock_info''')
            self.curs.execute(
                '''
                CREATE TABLE IF NOT EXISTS stock_info (
                id INT PRIMARY KEY NOT NULL,
                name CHAR(30),
                market TEXT,
                UNIQUE(name)
                )
                ''')

            """
            user_stock
            """
            self.curs.execute('''DROP TABLE IF EXISTS user_stock''') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
            self.curs.execute(
                '''
                CREATE TABLE IF NOT EXISTS user_stock (
                user_id INT NOT NULL,
                stock_id INT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                FOREIGN KEY(stock_id) REFERENCES stock_info(id) ON DELETE CASCADE
                )
                ''')
            self.conn.commit()
            print("Database initialization complete.")
            
        except sqlite3.Error as dbe:
            print("Error creating database.")
            print("Error code: " + dbe)
            
            
            
            
    """
    Read .csv file that records the stock and rate information.
    The .csv file is read in text mode. The numbers in which (e.g. the trade price) should be transformed to doubles later if required.
    The first row of .csv file contains headers.
    @param csv_filename: the name of .csv file, specified as <name of share>.csv
    @return: a dictionary that stores data from .csv column-wise.
    """
    def read_csv(self, csv_filename):
        try:
            with open(csv_filename, 'rt') as file:
                trade_info = csv.reader(file)
                headers = next(trade_info) # This .csv table has headers. This line skips the header to its data.
                data = {}
                for h in headers:
                    data[h] = []
            
                for row in trade_info:
                    for head, value in zip(headers, row):
                        data[head].append(value)
            
            return data
        except FileNotFoundError:
            print('ERROR: File not found.')
    """
    Quick insert stock data with stock id, name, and optional description
    @param stock_id: id INT PRIMARY KEY NOT NULL
    @param stoca_name: name CHAR(20) NOT NULL
    @param stock_descrtiption: description text
    """
    def insert_stock(self, stock_id, stock_name, stock_description = None):
        if stock_id is not None and stock_name is not None:
            self.curs.execute(
                fmt.format('''
                INSERT INTO stock_info VALUES ({sid}, \'{sname}\', \'{sdes}\')
                ''', sid = stock_id, sname = stock_name, sdes = stock_description)
                )
            self.conn.commit()
        else:
            print('Invalid insert. Check the input.')
            return None
        
    """
    Quick search stock with either stock id or stock name.
    Passing no variable to this method is legal, and will return an empty list.
    @param stock_id: stock_id
    @param stock_name: stock_name
    """
    def search_stock(self, stock_id = None, stock_name = None):
        if stock_id:
            self.curs.execute(
                'SELECT * FROM stock_info WHERE id = ' + str(stock_id)
                )
        elif stock_name:
            self.curs.execute(
                'SELECT * FROM stock_info WHERE name = ' + '\'' + stock_name + '\''
                )
        return self.curs.fetchall()
    
    """
    Quick insert user with user id, first name, last name, gender, middle name, wechat id, email and prefered method
    Gender is represented in binary. 0 is male and 1 is female.
    To comply with None passing, the order of this function is different from that stored in database. 
    The parameter order in description follows the order from the function.
    NOTE: The middle name, along with all strings without value, is empty string instead of None.
    @param user_id: id INT PRIMARY KEY NOT NULL
    @param first_name: first_name CHAR(20) NOT NULL
    @param last_name: last_name CHAR(20) NOT NULL
    @param gender: gender int NOT NULL
    @param middle_name: middle_name CHAR(20)
    @param wechat_id: wechat_id CHAR(20)
    @param email:  email CHAR(30),
    @param method: prefer_method_id INT,
                FOREIGN KEY(prefer_method_id) REFERENCES method(id)
    """
    def insert_user(self, user_id, first_name, last_name, gender, middle_name = None, wechat_id = None, email = None, method = 0):
        if user_id is not None and first_name is not None and last_name is not None and gender is not None:
            self.curs.execute(
            fmt.format(
                '''
                INSERT INTO user VALUES ({uid}, \'{ufname}\', \'{umname}\', \'{ulname}\', {gend}, \'{wechat}\', \'{em}\', {pref_method})
                ''', uid = user_id, ufname = first_name, umname = middle_name, ulname = last_name,\
                gend = gender, wechat = wechat_id, em = email, pref_method = method
                )
            )
            self.conn.commit()
        else:
            print('Invalid insert. Check the input.')
            return None
    
    
    
    """
    Quick insert analysis method (with optional description).
    To avoid the format changes "None" into string and insert in description, the default of description uses empty string.
    Apr. 19: Method with id 0 is preoccupied as 'Undetermined' to solve None method type conflict.
    @param method_id: the id of the search method in database.
    @param method_name: the method name of method in search.
    At least one of such parameters should be present.
    """
    def insert_method(self, method_id, method_name, desc = None):
        if method_id is not None and method_name is not None:
            self.curs.execute(
                fmt.format('''
                INSERT INTO method VALUES ({mid}, \'{mname}\', \'{description}\')
                ''', mid = method_id, mname = method_name, description = desc)
                )
            self.conn.commit()
        else:
            print('Invalid insert. Check the input')
    
    
    """
    Quick search user with user id, or first AND last name.
    First and last names MUST be put together, while id can present individually or together.
    @param user_id: user_id
    @param first_name: first_name
    @param last_name: last_name
    """
    def search_user(self, user_id = None, first_name = None, last_name = None):
        if user_id:
            self.curs.execute(
                'SELECT * FROM user WHERE id = ' + str(user_id)
                )
            return self.curs.fetchall()
        elif first_name is not None and last_name is not None:
            self.curs.execute(
                'SELECT * FROM user WHERE first_name = ' + '\'' + first_name + '\'' + ' AND last_name = '+ '\'' + last_name + '\''
                )
            return self.curs.fetchall()
        else:
            print('Invalid search. Check the input.')
            return None
    
    """
    Return all information in user table.
    """
    def get_user_all(self):
        self.curs.execute(
            '''
            SELECT * FROM user
            '''
            )
        return self.curs.fetchall()
    
    """
    Return a list of all user id and name.
    """
    def get_user_name(self):
        self.curs.execute(
            '''
            SELECT id, first_name, last_name, middle_name FROM user
            '''
            )
        return self.curs.fetchall()
    
    """
    Return a list of all stock name.
    """
    def get_stock_name(self):
        self.curs.execute(
            '''
            SELECT name FROM stock_info
            '''
            )
        return self.curs.fetchall()
    
    """
    Insert the relationship between a user and a stock. The user SUBSCRIBES such a stock given this relationship.
    Assume that both records of user and stock already exist in database.
    The inserted user requires either user's id or full name (in separation of first and last names)
    The stock requires either stock id or stock name.
    To pass a user, both the first name and the last name have to be passed.
    @param userid: user.id
    @param userfirstname: user.first_name
    @param userlastname: user.last_name
    @param stockid: stock_info.id
    @param stockname: stock_info.name
    """
    def insert_user_stock(self, userid = None, userfirstname = None, userlastname = None, stockid = None, stockname = None):
        if (userid is not None or (userfirstname is not None and userlastname is not None)) and (stockid is not None or stockname is not None):
            uid = 0
            sid = 0
            
            if userid is not None:
                uid = userid
            elif userfirstname is not None and userlastname is not None:
                self.curs.execute(
                    '''
                    SELECT id FROM user
                    WHERE user.first_name = \'{ufn}\'
                    AND user.last_name = \'{uln}\' 
                    '''.format(ufn = userfirstname, uln = userlastname)
                    )
                uid = self.curs.fetchall()[0][0]
            
            if stockid is not None:
                sid = stockid
            else:
                self.curs.execute(
                    '''
                    SELECT id FROM stock_info
                    WHERE stock_info.name = \'{sname}\'
                    '''.format(sname = stockname)
                    )
                sid = self.curs.fetchall()[0][0]
            
            self.curs.execute(
                '''
                INSERT OR IGNORE INTO user_stock VALUES ({userid} , {stockid})
                '''.format(userid = uid, stockid = sid) # If the relationship exists, the insertion will be ignored.
                )
            self.conn.commit()
        
        else:
            print('Invalid insert input.')
            return None
            
    """
    Input either user full name (In first, middle and last), return all stock id and name this user subscribed.
    @param uid: user.id
    @param ufname: user.first_name
    @param umname: user.middle_name
    @param ulname: user.last_name
    """
    def get_user_stock(self, uid = None, ufname = None, umname = '', ulname = None):
        # SIDE NOTE: THIS IS THE FIRST METHOD THAT IS UNDER "SQLite COLLECTIVE WHERE CONDITION" TO ELIMINATE "IF/ELSE MESS" OF INPUT
        # HOWEVER, IT IS UNDER RISK OF TYPECASTING NONE INPUT. CHECK IT OUT.
        # OK, the thing is, the uid will be typecaseted to String, and therefore OperationalError occurs since id DN allow string.
        if uid is not None:
            self.curs.execute(
                '''
                SELECT s.id, s.name
                FROM (user AS u INNER JOIN user_stock AS us ON u.id = us.user_id)
                INNER JOIN stock_info AS s ON s.id = us.stock_id
                WHERE (u.id = {userid})
                '''.format(userid = uid)
            )
            return self.curs.fetchall()
        
        elif ufname is not None and ulname is not None:
            self.curs.execute(
                fmt.format('''
                SELECT s.id, s.name
                FROM (user AS u INNER JOIN user_stock AS us ON u.id = us.user_id)
                INNER JOIN stock_info AS s ON s.id = us.stock_id
                WHERE (u.first_name = \'{userfname}\' AND u.middle_name = \'{usermname}\' AND u.last_name = \'{userlname}\')
                ''', userfname = ufname, usermname = umname, userlname = ulname)
            )
            return self.curs.fetchall()
        
        else:
            print("Invalid input.")
            return None
        
    """
    Input either user id or full name, edit the wechat id and/or email of this user.
    @param uid: user.id
    @param ufname: user.first_name
    @param umname: user.middle_name
    @param ulname: user.last_name
    @param newWeChat: The new WeChat account to be modified.
    @param newEmail: The new email to be modified.
    """
    def edit_user_info(self, uid = None, ufname = None, umname = None, ulname = None, newWeChat = None, newEmail = None):
        if uid is not None:
            if newWeChat is not None and newEmail is not None:
                self.curs.execute(
                    fmt.format('''
                    UPDATE user
                    SET wechat_id = \'{nwechat}\', email = \'{nemail}\'
                    WHERE id = {userid}
                    ''', nwechat = newWeChat, nemail = newEmail, userid = uid)
                    )
                self.conn.commit()
            elif newWeChat is not None and newEmail is None:
                self.curs.execute(
                    fmt.format('''
                    UPDATE user
                    SET wechat_id = \'{nwechat}\'
                    WHERE id = {userid}
                    ''', nwechat = newWeChat, userid = uid)
                    )
                self.conn.commit()
            elif newWeChat is None and newEmail is not None:
                self.curs.execute(
                    fmt.format('''
                    UPDATE user
                    SET email = \'{nemail}\'
                    WHERE id = {userid}
                    ''', nemail = newEmail, userid = uid)
                    )
                self.conn.commit()
            else:
                print('No value has been changed.')
        elif ufname is not None and ulname is not None:
            if newWeChat is not None and newEmail is not None:
                self.curs.execute(
                    fmt.format(
                    '''
                    UPDATE user
                    SET wechat_id = \'{nwechat}\', email = \'{nemail}\'
                    WHERE first_name = \'{fname}\' AND middle_name = \'{mname}\' AND last_name = \'{lname}\'
                    ''', nwechat = newWeChat, nemail = newEmail, fname = ufname, mname = umname, lname = ulname)
                    )
                self.conn.commit()
            elif newWeChat is not None and newEmail is None:
                self.curs.execute(
                    fmt.format(
                    '''
                    UPDATE user
                    SET wechat_id = \'{nwechat}\'
                    WHERE first_name = \'{fname}\' AND middle_name = \'{mname}\' AND last_name = \'{lname}\'
                    ''', nwechat = newWeChat, fname = ufname, mname = umname, lname = ulname)
                    )
                self.conn.commit()
            elif newWeChat is None and newEmail is not None:
                self.curs.execute(
                    fmt.format(
                    '''
                    UPDATE user
                    SET email = \'{nemail}\'
                    WHERE first_name = \'{fname}\' AND middle_name = \'{mname}\' AND last_name = \'{lname}\'
                    ''', nemail = newEmail, fname = ufname, mname = umname, lname = ulname)
                    )
                self.conn.commit()
            else:
                print('No value has been changed.')
        else:
            print('Invalid user information.')
            
    """
    Edit the perferred method of the user, identified by either id or name, to the given method ID
    """
    def edit_user_prefer_method(self, uid = None, ufname = None, umname = None, ulname = None, newmethodid = None):
        if uid is not None:
            self.curs.execute(
                fmt.format('''
                UPDATE user
                SET prefer_method_id = {mid}
                WHERE id = {user_id}
                ''', mid = newmethodid, user_id = uid)
                )
            self.conn.commit()
        elif ufname is not None and ulname is not None:
            self.curs.execute(
                fmt.format(
                    '''
                    UPDATE user
                    SET prefer_method_id = {mid}
                    WHERE first_name = \'{fname}\' AND middle_name = \'{mname}\' AND last_name = \'{lname}\'
                    ''', mid = newmethodid, fname = ufname, mname = umname, lname = ulname
                    )
                )
            self.conn.commit()
        else:
            print('Invalid user information.')
    """
    Return the preferred user method. At least one of the user ID and the user full name (First AND last name) is required.
    Apr. 19: Method with id 0 is preoccupied as 'Undetermined' to solve None method type conflict.
    @param uid: the id of user.
    @param ufname: the first name of user.
    @param umname: the (optional) user middle name.
    Following the previous procotol, the default of middle name is empty string instead of None.
    @param ulname: the last name of user.
    """
    def get_user_prefer_method(self, uid = None, ufname = None, umname = None, ulname = None):
        if uid is not None:
            self.curs.execute(
                '''
                SELECT method.id, method.name
                FROM user JOIN method ON user.prefer_method_id = method.id
                WHERE user.id = {id}
                '''.format(id = uid)
            )
            return self.curs.fetchall()
        elif ufname is not None and ulname is not None:
            self.curs.execute(
                fmt.format('''
                SELECT method.id, method.name
                FROM user JOIN method ON user.prefer_method_id = method.id
                WHERE user.first_name = \'{firstname}\' AND user.middle_name = \'{middlename}\' AND user.last_name = \'{lastname}\'
                ''', firstname = ufname, middlename = umname, lastname = ulname)
            )
            return self.curs.fetchall()
        else:
            print("Empty search condition.")
    
    
    """
    A function that checks if all stocks in stock_info table has its corresponding transaction table.
    If all have one, return true. Otherwise, return false.
    """
    def is_transaction_table_match(self):
        self.curs.execute(
            '''
            SELECT name FROM stock_info
            '''
            )
        stocks = self.curs.fetchall()
        for stockname_tuple in stocks:
            stockname = stockname_tuple[0]
            #print(stockname) # TEST
            self.curs.execute(
                '''
                SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'transaction_{sname}\'
                '''.format(sname = stockname)
                )
            if(self.curs.fetchall() == []):
                return False
        return True
    
    
    
    
    """
    Create a table of transaction data record of a particular stock into the database.
    The .csv is required to contain the following five columns in the particular order:
        ind: the index of the transaction. The table will only save the latest 200 transaction days record. Use as primary key.
        name: the stock name. Used to reference stock_info table. All names in the same table should be the same.
        date: the date of a transaction.
        open: the price of the stock when market is opened for a particular day.
        high: the highest price of stock for a particular day.
        close: the price of the stock when market is closed for a particular day.
        low: the lowest price of stock for a particular day.
    @param filename: the .csv file that stores data of a particular stock. The name of .csv file must be the same as the corresponding stock name.
    """
    def transaction_data_table(self, filename):
        transaction_data_dict = self.read_csv(filename)
        if filename.endswith('.csv'):
            stock_name = filename[:-4] # File name with the removal of '.csv' should be the name of the corresponding stock.
            #print(stock_name) # TEST
            self.curs.execute(
                '''
                SELECT name FROM stock_info WHERE name = {stockname}
                '''.format(stockname = stock_name)
                ) # check if the .csv name corresponds to one of the stock name.
            stock_name_check = self.curs.fetchall()
            if stock_name == stock_name_check[0][0]: # The name should return the only value, as the first in returned list and tuple.
                self.curs.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS transaction_{stockname} (
                    ind INT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    close REAL NOT NULL,
                    low REAL NOT NULL,
                    FOREIGN KEY(name) REFERENCES stock_info(name) ON DELETE CASCADE
                    )
                    '''.format(stockname = stock_name) #
                    ) # Create a new table of transaction of this stock if not exists.
                self.conn.commit()
                
                index = 0;
                while(index < len(transaction_data_dict['ind'])):
                    # 4/5: The conflict of data insert is solved
                    # Assumption: No two stock data has identical primary key. Or the later one will be ignored.
                    self.curs.execute(
                        '''
                        INSERT OR IGNORE INTO transaction_{stockname} VALUES ({ind}, \'{name}\', \'{date}\', {open}, {high}, {close}, {low} )
                        '''.format(stockname = stock_name,
                                   ind = transaction_data_dict['ind'][index],
                                   name = stock_name,
                                   date = transaction_data_dict['date'][index],
                                   open = transaction_data_dict['open'][index],
                                   high = transaction_data_dict['high'][index],
                                   close = transaction_data_dict['close'][index],
                                   low = transaction_data_dict['low'][index], 
                                   )
                        )
                    self.conn.commit()
                    # Delete the smallest-index data if more than 200 data exist.
                    self.curs.execute(
                        '''
                        SELECT COUNT(ind) FROM transaction_{stockname}
                        '''.format(stockname = stock_name)
                        )
                    num_count = self.curs.fetchall()[0][0] # Return a dictionary that contains a single value as number of data. Retrieve that value.
                    if(num_count > 200):
                        self.curs.execute(
                            '''
                            DELETE FROM transaction_{stockname}
                            WHERE ind = (SELECT MIN(ind) FROM transaction_{stockname})
                            '''.format(stockname = stock_name)
                            )
                        self.conn.commit()
                    index += 1
                print('Table creation successful.')
            else:
                print("Filename and stock do not match. Check file.")
        else:
            print('Incorrect file input. Check file.')
            return None
    
    
    
    
    """
    Insert the corresponding stock analysis of the stock.
    """
    def insert_stock_analysis(self):
        pass # STOCK ANALYSIS TABLE MIGHT BE CANCELLED. AWAIT.
    
    """
    Unsubscribe a user a particular share given their relationship exists in user_stock
    if not, or the input is incorrect, no action will be taken.
    At least one of the id or the full name of user, AND one of the stock id and name must be passed.
    @param uid: user.id
    @param ufname: user.first_name
    @param umname: user.middle_name
    @param ulname: user.last_name
    @param sid: stock_info.id
    @param sname: stock_info.name
    """
    def unsubscribe_share(self, uid = None, ufname = None, umname = None, ulname = None, sid = None, sname = None):
        if uid is not None:
            if sid is not None:
                self.curs.execute(
                    '''
                    DELETE FROM user_stock
                    WHERE user_id = {userid} AND stock_id = {stockid}
                    '''.format(userid = uid, stockid = sid)
                    )
                self.conn.commit()
            elif sname is not None:
                self.curs.execute(
                    fmt.format('''
                    DELETE FROM user_stock
                    WHERE user_id = {userid}
                    AND stock_id = (SELECT id FROM stock_info WHERE name = \'{stockname}\')
                    ''', userid = uid, stockname = sname)
                    )
                self.conn.commit()
            else:
                print("No proper stock info is passed. No action.")
        elif ufname is not None and umname is not None and ulname is not None:
            if sid is not None:
                self.curs.execute(
                    fmt.format('''
                    DELETE FROM user_stock
                    WHERE user_id = (SELECT id FROM user WHERE first_name = \'{fname}\'
                    AND middle_name = \'{mname}\'
                    AND last_name = \'{lname}\')
                    AND stock_id = {stockid}
                    ''', fname = ufname, mname = umname, lname = ulname, stockid = sid)
                    )
                self.conn.commit()
            elif sname is not None:
                self.curs.execute(
                    fmt.format('''
                    DELETE FROM user_stock
                    WHERE user_id = (SELECT id FROM user WHERE first_name = \'{fname}\'
                    AND middle_name = \'{mname}\'
                    AND last_name = \'{lname}\')
                    AND stock_id = (SELECT id FROM stock_info WHERE name = \'{stockname}\')
                    ''', fname = ufname, mname = umname, lname = ulname, stockid = sid, stockname = sname)
                    )
                self.conn.commit()
            else:
                print("No proper stock info is passed. No action.")
        else:
            print("No proper user id or name is passed. No action.")
    
    """
    Delete a particular user given at least one of his/her id, email and/or wechat account.
    This deletion only executes within database. separated from email and wehcat unsubscribes.
    @param user_id: the user_id INT to be deleted from DB. user_id will be considered with priority if available.
    @param email: the email CHAR(30) to be deleted from DB.
    @param wechat: the wechat CHAR(20) to be deleted from DB.
    """
    def delete_user(self, user_id = None, email = None, wechat_id = None):
        if user_id:
            self.curs.execute(
                '''
                DELETE FROM user
                WHERE EXISTS (
                    SELECT * FROM user WHERE id = {uid}
                )
                '''.format(uid = user_id)
                )
            self.conn.commit()
        elif email:
            self.curs.execute(
                fmt.format('''
                DELETE FROM user
                WHERE EXISTS (
                    SELECT * FROM user WHERE email = \'{emailadd}\'
                )
                ''', emailadd = email)
                )
            self.conn.commit()
        elif wechat_id:
            self.curs.execute(
                fmt.format('''
                DELETE FROM user
                WHERE EXISTS (
                    SELECT * FROM user WHERE wechat_id = \'{wechat}\'
                )
                ''', wechat = wechat_id)
                )
            self.conn.commit()
        else:
            print('No parameter is given. No deletion executed.')
            
    
    
    
    """
    Manual SQL query function.
    After running this function, run <instance_name>.curs.fetchall() (or any other fetch) manually to return any select operation
    and to run <instance_name>.conn.commit() manually to return other operations.
    @param sql: The SQL query language to be executed.
    """
    def query(self, sql):
        self.curs.execute(sql)
        self.conn.commit()
    
    def __enter__(self):
        return self
    
    def __exit__(self):
        self.close()
    
    
    
    
    """
    Disconnect and close the database.
    """
    def close(self):
        if self.conn:
            self.conn.commit()
            self.curs.close()
            self.conn.close()
    
 
# TEST    
def test():
    # initialize
    db = stockDB()
    db.new('test.db')
    
    # TEST csv read
    csv_dict = db.read_csv('Cu2.csv')
    print(csv_dict)
    print(csv_dict['high']) # TEST print all high values in .csv
    
    # TEST insert method
    db.insert_method(1, 'MASS', 'MASS analysis')
    db.insert_method(2, 'MACD')
    print('method table return: ')
    db.query('SELECT * FROM method')
    print(db.curs.fetchall())
    
    # TEST insert stock
    db.insert_stock(4, '600004', 'Shanghai')
    
    # TEST query
    db.query(
        '''
        SELECT * FROM stock_info
        '''
        )
    
    # TEST database return print
    print(db.curs.fetchall())
    
    # TEST search stock
    print(db.search_stock(stock_id = 4))
    print(db.search_stock(stock_name = '600004'))
    print(db.search_stock()) # EMPTY SEARCH, SHOULD RETURN NO RESULT.
    
    # TEST insert user
    db.insert_user(1, 'Yunxi', 'Kou', 0, '', 'wxid_0scyfs9rr92c21', 'yxk383@case.edu', 3) # THE ORDER OF DATA SHOULD BE PAID ATTN.
    db.insert_user(2, 'Lishan', 'Jin', 0, '', 'wxid_111111111111', 'lxj150@case.edu', 2)
    db.insert_user(3, 'Yufan', 'Chen', 1, '', 'wxid_222222222222', 'yfc2@case.edu', 3)
    db.insert_user(4, 'Boyuan', 'Cao', 1, '', 'wxid_324267323455', 'byc7@case.edu', 1)
    # RECOMMEND FILLING THE EMPTY PLACE WITH EMPTY STRING ''.
    
    # TEST get names:
    print(db.get_stock_name())
    print(db.get_user_name())
    
    # TES query
    db.query(
        '''
        SELECT name FROM stock_info WHERE name = '600004'
        '''
        )
    print(db.curs.fetchall())
    
    # TEST delete user
    #db.delete_user(wechat_id='wxid_0scyfs9rr92c21')
    
    # TEST search user
    print(db.search_user(first_name = 'Yunxi', last_name = 'Kou'))
    print(db.search_user(user_id = 1))
    print(db.search_user(user_id = 2)) # EMPTY RESULT
    
    # TEST insert transaction table
    db.transaction_data_table('600004.csv')
    
    # TEST check transaction table
    db.query('SELECT * FROM transaction_600004 WHERE ind = 0')
    print(db.curs.fetchall())
    
    # TEST: Additional SQL text: aggregate function.
    print('The total number of records in transaction_600004 is: ')
    db.query('SELECT COUNT(ind) FROM transaction_600004') # Return: dictionary of int. Find a way to call it out.
    print(db.curs.fetchall()[0][0])
    
    # TEST SQL least index delete statement. Will be commented out in runnable.
    """
    db.curs.execute(
                            '''
                            DELETE FROM transaction_600004
                            WHERE ind = (SELECT MIN(ind) FROM transaction_600004)
                            '''
                            )
    db.conn.commit()
    """
    db.query('SELECT * FROM transaction_600004')
    print(db.curs.fetchall())
    
    # TEST STOCK NAME
    db.curs.execute(
            '''
            SELECT name FROM stock_info
            '''
            )
    print(db.curs.fetchall())
    
    # TEST IF A TABLE EXISTS. WILL BE USED IN is_transaction_table_match FUNCTION.
    db.curs.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'transaction_600005\'')
    print(db.curs.fetchall())
    
    # TEST is_transaction_table_match. Should return true in test since already created.
    print(db.is_transaction_table_match())
    
    # TEST Relationship insert:
    print("\nTEST STOCK_INFO PRINT")
    db.query('SELECT id FROM stock_info WHERE stock_info.name = \'600004\'')
    print(db.curs.fetchall()[0][0])
    
    db.insert_user_stock(userid = 1, stockid = 4) # Yunxi Kou subscribes stock 600004
    db.insert_user_stock(userfirstname = 'Boyuan', userlastname = 'Cao', stockname = '600004')
    db.curs.execute('''
                SELECT * FROM user_stock
                    '''
                    )
    print(db.curs.fetchall())
    
    # TEST get_user_stock
    print('Test get_user_stock\n')
    print('TESTING user_stock DATA:')
    db.query('SELECT * FROM user_stock')
    print(db.curs.fetchall())
    print(db.get_user_stock(uid = 1))
    print(db.get_user_stock(ufname = 'Yunxi', umname = '', ulname = 'Kou')) # Print a list with a tuple (stock_id, stock_name)
    print(db.get_user_stock(uid = 3)) #Print empty dictionary
    print(db.get_user_stock()) #Print invalid, return none
    
    # TEST edit_user_info
    print("\nTest edit_user_info:")
    db.edit_user_info(1, newEmail = '840670877@qq.com')
    print(db.search_user(1))
    db.edit_user_info(1, newEmail= 'yxk383@case.edu', newWeChat='wxid_..........')
    print(db.search_user(1))
    db.edit_user_info(ufname = 'Yunxi', umname = '', ulname = 'Kou', newWeChat = 'wxid_0scyfs9rr92c21')
    print(db.search_user(1))
    
    # TEST unsubscribe_share
    print("\nTest unsubscribe_share:")
    print(db.get_user_stock(1))
    db.unsubscribe_share(ufname='Yunxi', umname='', ulname='Kou', sname = '600004')
    print(db.get_user_stock(1)) # Should return empty list.
    
    # TEST NONE INFO INSERT
    print('\nTesting None middle name.')
    # Invalid insert since id is None. 
    db.insert_user(user_id = None, first_name = 'John', last_name = 'Doe', gender = 0,\
                    middle_name = None, wechat_id = None, email = None, method = None) 
    #
    #db.insert_user(user_id = 5, first_name = 'Jane', last_name = 'Smith', gender = 1, middle_name = None)
    db.insert_user(5, 'Jane', 'Smith', 1)
    print(db.search_user(user_id = 5))
    
    # TEST method
    print('\nmethod test:')
    db.query('SELECT * FROM method WHERE id = 0')
    print(db.curs.fetchall())
    print(db.get_user_prefer_method(uid = 5)) # Undetermined
    print(db.get_user_prefer_method(uid = 1)) # In this example, prefer_method id is 3. Which isn't inserted yet. Therefore, print empty list.
    print(db.get_user_prefer_method(uid = 2)) # Return Method ID as 2, which is MACD (in this example)
    
    print("\nChange user-prefer method test:")
    db.edit_user_prefer_method(ufname='Yunxi',umname = '', ulname='Kou', newmethodid=2)
    print(db.get_user_prefer_method(uid=1))
    
    db.close()


"""
Generate demo database file
"""
def main(argv = None):
    if argv == 'test': # test run
        test()
    else: # generate demo database
        demodb = stockDB()
        demodb.new("demo.db")
        demodb.insert_method(1, "MASS")
        demodb.insert_method(2, "MACD")
        demodb.insert_method(3, "KDJ")
        demodb.insert_user(1, first_name = "Yunxi", last_name = "Kou", gender = 0, email = 'yxk383@case.edu', method=1)
        demodb.insert_user(2, first_name = "Lishan", last_name = "Jin", gender = 0, email = 'lxj150@case.edu', method=2)
        demodb.insert_user(user_id = 3, first_name = "Yufan", last_name = "Chen", gender = 0, method=3)
        demodb.insert_stock(1, "sh")
        demodb.insert_stock(2, "hs300")
        demodb.insert_stock(stock_id = 3, stock_name = "600037")
        demodb.insert_stock(stock_id = 4, stock_name = "600704")
        demodb.insert_stock(stock_id = 5, stock_name = "600004")
        demodb.insert_stock(stock_id = 6, stock_name = "600008")
        demodb.insert_stock(stock_id = 7, stock_name = "600848")
        demodb.insert_user_stock(userid = 1, stockid = 3)
        demodb.insert_user_stock(userid = 1, stockid = 4)
        demodb.insert_user_stock(userid = 1, stockid = 5)
        demodb.insert_user_stock(userid = 1, stockid = 6)
        demodb.insert_user_stock(userid = 1, stockid = 7)
        demodb.insert_user_stock(userid = 2, stockid = 3)
        demodb.insert_user_stock(userid = 2, stockid = 4)
        demodb.insert_user_stock(userid = 2, stockid = 5)
        demodb.insert_user_stock(userid = 2, stockid = 6)
        demodb.insert_user_stock(userid = 2, stockid = 7)
        demodb.insert_user_stock(userid = 3, stockid = 3)
        demodb.insert_user_stock(userid = 3, stockid = 4)
        demodb.insert_user_stock(userid = 3, stockid = 5)
        demodb.insert_user_stock(userid = 3, stockid = 6)
        demodb.insert_user_stock(userid = 3, stockid = 7)
        #TEST
        demodb.query('SELECT name FROM sqlite_master WHERE type = \'table\' AND name NOT LIKE \'sqlite_%\'')
        print(demodb.curs.fetchall()) # Check tables.
        
        demodb.query('SELECT * FROM method')
        print(demodb.curs.fetchall())
        print(demodb.get_user_all()) #user
        demodb.query('SELECT * FROM stock_info')
        print(demodb.curs.fetchall()) #stock
        demodb.query('SELECT * FROM user_stock')
        print(demodb.curs.fetchall()) #user_stock
        
        print("TEST GET USER PREFER METHOD BY NAME:")
        print(demodb.get_user_prefer_method(ufname = 'Yunxi', umname='', ulname = 'Kou'))
        
        print("TEST SEARCH USER:")
        print(demodb.search_user(first_name = 'Lishan', last_name = 'Jin'))
        
        print("TEST GET USER STOCK:")
        print(demodb.get_user_stock(ufname = 'Lishan', ulname = 'Jin'))
        
        
    
if __name__ == "__main__":
    main()
