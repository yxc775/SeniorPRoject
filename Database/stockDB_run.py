'''
The program responsible to run and test SQLite local database.
NOTE: IF ERRORS SHOW THAT A DATA EXISTS DURING TESTING, RUN stockDB_init TO RE-INITIALIZE.
RECOMMEND TO USE "INSERT IF NOT EXISTS" QUERY.

3/8: Currently this program is used for test purpose. May subject to change.

@author: Yunxi Kou - yxk383
'''
import sqlite3

# Connect to SQLite database.
conn = sqlite3.connect('Stockprice_test.db')
print("Database opened.")

# Create SQL Cursors for command.
curs = conn.cursor()

# TEST INSERT DATA
curs.execute('''INSERT INTO method VALUES (1, 'MACD', 'Moving Average Convergence/Divergence')''') #TEST INSERT: method
conn.commit()

curs.execute('''INSERT INTO method VALUES (3, 'MASS', 'Mass Index')''') #TEST INSERT: method
conn.commit()

curs.execute('''INSERT INTO user VALUES (1, 'Yunxi', '','Kou', 0, 'wxid_0scyfs9rr92c21', 'yxk383@case.edu', 3)''') #TEST INSERT: user
conn.commit()

curs.execute('''SELECT * FROM user JOIN method ON user.prefer_method_id = method.id''') #TEST QUERY: method
print(curs.fetchall()) #TEST PRINT

curs.execute('''INSERT INTO stock_info VALUES (4, 'SANY', 'Shanghai')''') #TEST INSERT: stock
conn.commit()

curs.execute('''INSERT INTO user_stock VALUES (1, 4)''') #TEST INSERT :relationship
conn.commit()

curs.execute('''SELECT user.id, user.first_name, user.last_name FROM user JOIN
                (user_stock JOIN stock_info ON user_stock.stock_id = stock_info.id)
                ON user.id = user_stock.user_id
                WHERE stock_info.name = 'SANY' ''') #TEST QUERY: relationship
print(curs.fetchall())

conn.close()