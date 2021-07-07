"""
    Script to create the youless database, does not overwrite existing database.
    Checks if the database exists, creates it if none existant.
    If database exists checks if all tables are created, if not creates them.
"""

import sqlite3 as sl

from globals import *

path = Vars.path + Vars.dbname

def isSqlite3Db(db): # method credits: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
    if not os.path.isfile(db): return False
    sz = os.path.getsize(db)

    # file is empty, give benefit of the doubt that its sqlite
    # New sqlite3 files created in recent libraries are empty!
    if sz == 0: return True

    # SQLite database file header is 100 bytes
    if sz < 100: return False

    # Validate file header
    with open(db, 'rb') as fd: header = fd.read(100)

    return (header[:16] == b'SQLite format 3\x00')

def isTableExists(table):
    con = sl.connect(path)
    with con:
        check = Vars.conf("queries")["table_exist"]
        table = (table,)
        run = con.execute(check, table)
        e = int(run.fetchone()[0])

        dbg(lambda: e)

        rtn = True if (e != 0) else False
        dbg(lambda: "table {} existence is {}".format(table, rtn))
        return rtn

        # if (e != 0):
        #     # dayhours_e = True
        #
        #
        #     return True

def main():
    if not isSqlite3Db(path):
        log(lambda: "Database {} non existant, creating database".format(Vars.dbname))
        for v in Vars.conf("dbtables").values():
            for i in v:
                con = sl.connect(path)
                with con:
                    con.execute(Vars.conf("queries")[i])
                    log(lambda: "Table {} created".format(i))
    else:
        log(lambda: "Database {} exists, checking and creating tables".format(Vars.dbname))
        for v in Vars.conf("dbtables").values():
            for i in v:
                if (isTableExists(i)):
                    log(lambda: "Table {} already exists, doing nothing".format(i))
                else:
                    log(lambda: "Table {} does not exist, creating".format(i))
                    con = sl.connect(path)
                    # CREATE TABLE
                    with con:
                        con.execute(Vars.conf("queries")[i])
                        
if __name__ == '__main__':
    main()