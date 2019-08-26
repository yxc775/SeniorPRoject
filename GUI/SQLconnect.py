import stockDB
import os
database = os.path.realpath('..') + "/Database/demo.db"

def getdb():
    db = stockDB.stockDB(database)
    return db

def main():
    db = stockDB.stockDB(database)
    try:
        db.insert_user(4, 'Boyuan', 'Cao', 1, '', 'wxid_324267323455', 'byc7@case.edu', 0)
    except:
        print("lol")

if __name__ == '__main__':
    main()
