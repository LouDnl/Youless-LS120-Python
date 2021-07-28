#!/usr/bin/env python3
"""
    File name: db_connect.py.py
    Author: LouDFPV
    Date created: 25/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file contains an internal class that connects to the database and returns the connection
"""
# sqlite
import sqlite3 as sl
from sqlite3.dbapi2 import OperationalError

# Youless setup
from LS120 import Settings

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("db_connect.py started")


class db_connect():
    """class to return a read or read/write connection to the database"""

    def __init__(self) -> None:
        self.path = Settings.path + Settings.dbname

    def connect_and_return_read(self):
        """db_connect().connect_and_return_read() -> returns sqlite database connection in read only mode"""
        self.__db_file = self.path
        logger.debug("Starting read only database connection...")
        self.conn = None
        try:
            self.conn = sl.connect(f'file:{self.__db_file}?mode=ro', uri=True)  # try to open the database file in read only mode
            logger.debug("Connected to: %s" % self.__db_file)
            return self.conn
        except OperationalError as e:  # raise exception if file is not found
            logger.error(e)
            logger.error("file not found %s" % self.__db_file)
            return e

    def connect_and_return_readwrite(self):
        """db_connect().connect_and_return_readwrite() -> returns sqlite database connection in read/write mode"""
        self.__db_file = self.path
        logger.debug("Starting read write database connection...")
        self.conn = None
        try:
            self.conn = sl.connect(f'file:{self.__db_file}?mode=rw', uri=True)  # try to open the database file in read only mode
            logger.debug("Connected to: %s" % self.__db_file)
            return self.conn
        except OperationalError as e:  # raise exception if file is not found
            logger.error(e)
            logger.error("file not found %s" % self.__db_file)
            return e
