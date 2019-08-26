'''
A SQLite-based local SQL database for effect testing and verification purposes.
This program is mainly used for testing stock data passing and storage 
in SQL and design improvement.

This part initializes an empty sqlite local database with structures designed in database.jpeg
with no additional table for stocks created, in purpose of database initialization and test.

@author: Yunxi Kou - yxk383
'''
import sqlite3

# Connect to SQLite database.
conn = sqlite3.connect('Stockprice_test.db')
print("Database opened.")

# Create SQL Cursors for command.
curs = conn.cursor()

# table initialize.

'''
method
'''
curs.execute('DROP TABLE IF EXISTS method') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
#conn.commit()
curs.execute(
    '''
    CREATE TABLE IF NOT EXISTS method (
    id INT PRIMARY KEY NOT NULL,
    name CHAR(20) NOT NULL,
    description text
    )
    ''')
conn.commit()

'''
user
'''
curs.execute('DROP TABLE IF EXISTS user') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
#conn.commit()
curs.execute(
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
conn.commit()

'''
report
'''
curs.execute('''DROP TABLE IF EXISTS report''') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
curs.execute(
    '''
    CREATE TABLE IF NOT EXISTS report (
    id INT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    date INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
    )
    ''')
conn.commit()

'''
stock_info
'''
curs.execute('''DROP TABLE IF EXISTS stock_info''') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
curs.execute(
    '''
    CREATE TABLE IF NOT EXISTS stock_info (
    id INT PRIMARY KEY NOT NULL,
    name CHAR(30),
    market TEXT
    )
    ''')
conn.commit()

'''
user_stock
'''
curs.execute('''DROP TABLE IF EXISTS user_stock''') # DATABASE STRUCTURE TEST DROP. COMMENT OUT AFTER COMPLETION.
curs.execute(
    '''
    CREATE TABLE IF NOT EXISTS user_stock (
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
    FOREIGN KEY(stock_id) REFERENCES stock_info(id)
    )
    ''')

print('Database re-initialize complete.')
conn.close()