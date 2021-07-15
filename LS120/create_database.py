#!/usr/bin/env python3
"""
    create_database.py

    This file creates an sqlite3 database to store youless data in, it does not overwrite an existing database.
    Checks if the database exists, creates it if none existant.
    If database exists checks if all tables are present, if not creates them.
"""
import os
import sqlite3 as sl

# Youless setup
from .constants import Settings, Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("create_database.py started")

path = Settings.path + Settings.dbname


def isSqlite3Db(db):  # method credits: https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
    if not os.path.isfile(db):
        return False
    sz = os.path.getsize(db)

    # file is empty, give benefit of the doubt that its sqlite
    # New sqlite3 files created in recent libraries are empty!
    if sz == 0:
        return True

    # SQLite database file header is 100 bytes
    if sz < 100:
        return False

    # Validate file header
    with open(db, 'rb') as fd:
        header = fd.read(100)

    return (header[:16] == b'SQLite format 3\x00')


def is_table_exists(table):
    con = sl.connect(path)
    with con:
        check = Youless.sql("queries")["table_exist"]
        table = (table,)
        run = con.execute(check, table)
        e = int(run.fetchone()[0])  # returns 1 if exists

        rtn = True if (e != 0) else False  # 1 == True else False
        logger.debug("table {} existence is {}".format(table, rtn))
        return rtn


def main():
    if not isSqlite3Db(path):
        logger.warning("Database {} non existant, creating database".format(Settings.dbname))
        for v in Youless.sql("dbtables").values():
            for i in v:
                con = sl.connect(path)
                with con:
                    con.execute(Youless.sql("queries")[i])
                    logger.warning("Table {} created".format(i))
    else:
        logger.warning("Database {} exists, checking and creating tables".format(Settings.dbname))
        for v in Youless.sql("dbtables").values():
            for i in v:
                if (is_table_exists(i)):
                    logger.warning("Table {} already exists, doing nothing".format(i))
                else:
                    logger.warning("Table {} does not exist, creating".format(i))
                    con = sl.connect(path)
                    # CREATE TABLE
                    with con:
                        con.execute(Youless.sql("queries")[i])


if __name__ == '__main__':
    main()
