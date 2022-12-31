#!/usr/bin/env python3
"""
    File name: db_write_data.py
    Author: LouDFPV
    Date created: 26/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file stores read data from a Youless LS120 device in to an existing sqlite3 database.
"""
import ast  # for converting string representation of a list to a list
# initialize logging
import logging
import sys

# Youless setup
from LS120 import Youless, db_connect

logger = logging.getLogger(__name__)
logger.debug("db_write_data.py started")

sys.stdin.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding
sys.stdout.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding


class parse_data:
    """class to parse data read from youless"""

    def __init__(self) -> None:
        self.__headers = Youless.web("HEADERS")  # acceptable html headers
        self.__url = Youless.web("URL")  # base url
        self.__ele = Youless.web("ELE")
        self.__gas = Youless.web("GAS")
        self.__snul = Youless.web("S0")
        self.__json = Youless.web("JSON")
        self.__month = Youless.web("M")
        self.__day = Youless.web("W")
        self.__kwh = Youless.sql("valuenaming")[0]
        self.__m3 = Youless.sql("valuenaming")[1]
        self.__watt = Youless.sql("valuenaming")[2]
        self.__ltr = Youless.sql("valuenaming")[3]
        self.conn = db_connect().connect_and_return_readwrite()

    def parse_tenminutes(self, etype, data):
        """Function to parse the information retrieved by read_ten_minutes

        example:
        parse_tenminutes(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by read_ten_minutes
        """
        self.__table = Youless.sql("dbtables")[etype][2]
        self.__type = self.__watt if etype == 'E' and etype != 'G' else self.__ltr
        logger.debug("Connected to table {}".format(self.__table))
        for key in data.keys():
            write_data().write_tenminutes(self.conn, (key, data[key]), self.__table, self.__type)
        self.conn.close()
        logger.debug("Database connection closed...")

    def parse_days(self, etype, data):
        """Function to parse the information retrieved by retrieve_days

        example:
        parse_days(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by retrieve_days
        """
        self.__table = Youless.sql("dbtables")[etype][1]
        self.__type = self.__watt if etype == 'E' and etype != 'G' else self.__ltr
        logger.debug("Connected to table {}".format(self.__table))
        for item in data:
            write_data().write_dayhours(self.conn, item, self.__table, self.__type)
        self.conn.close()
        logger.debug("Database connection closed...")

    def parse_months(self, etype, data):
        """Function to parse the information retrieved by retrieve_months

        example:
        parse_months(etype, data)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        :data is a list with tuples retrieved by retrieve_months
        """
        self.__table = Youless.sql("dbtables")[etype][0]
        self.__type = self.__kwh if etype == 'E' and etype != 'G' else self.__m3
        logger.debug("Connected to table {}".format(self.__table))
        for item in data:
            write_data().write_yeardays(self.conn, item, self.__table, self.__type)
        self.conn.close()
        logger.debug("Database connection closed...")


class write_data:
    """class to write parsed data from youless in an sqlite3 database"""

    def __init__(self) -> None:
        self.__headers = Youless.web("HEADERS")  # acceptable html headers
        self.__url = Youless.web("URL")  # base url
        self.__ele = Youless.web("ELE")
        self.__gas = Youless.web("GAS")
        self.__snul = Youless.web("S0")
        self.__json = Youless.web("JSON")
        self.__month = Youless.web("M")
        self.__day = Youless.web("W")
        self.__kwh = Youless.sql("valuenaming")[0]
        self.__m3 = Youless.sql("valuenaming")[1]
        self.__watt = Youless.sql("valuenaming")[2]
        self.__ltr = Youless.sql("valuenaming")[3]

    def write_tenminutes(self, conn, insertion, table, type):
        """Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, week, month, monthname, day, yearday, values per hour

        example insertion:
            ('2021-07-16', [('2021', '28', '07', 'July', '16', '197'), [{'23:50': 264}, {'23:40': 432}, {'23:30': 600}, {'23:20': 648}, {'23:10': 540}]])
        example converted_insertion:
            ('2021-07-16', '2021', '28', '07', 'July', '16', '197', "[{'23:50': 264}, {'23:40': 432}]")
        """
        self.table = table
        self.type = type
        self.sql = Youless.sql("queries")["i_daytenminutes"]
        self.query = Youless.sql("queries")["s_table"]
        self.datequery = (insertion[0].strip(),)  # create primary key check
        self.date = insertion[0]  # create primary key check
        converted_insertion = (insertion[0], insertion[1][0][0], insertion[1][0][1], insertion[1][0][2], insertion[1][0][3], insertion[1][0][4], insertion[1][0][5], f'{insertion[1][1]}')

        cur = conn.cursor()
        self.check = cur.execute((self.query % self.table), self.datequery)  # check the database for existing primary keys
        new_list = insertion[1][1]  # x list of key:value dictionaries
        lenX = len(new_list)  # amount of key:value items (144 items of 10 minutes for a 24 hour day)

        existing_entry = self.check.fetchall()  # fetch the complete entry from the database
        try:
            existing_key = existing_entry[0][0]  # assign existing key
            existing_values = ast.literal_eval(existing_entry[0][7])  # convert string representation of list to real list
            existing_list = existing_values
            # source: https://stackoverflow.com/questions/9845369/comparing-2-lists-consisting-of-dictionaries-with-unique-keys-in-python
            list_pair = zip(existing_list, new_list)  # create zipped list pair
            if any(x != y for x, y in list_pair) is True:  # compare the lists with dictionaries for differences
                differences = [(x, y) for x, y in list_pair if x != y]  # if there are any then get the differences
                differences = len(differences)  # get the amount of differences
            else:
                differences = 0
        except Exception as E:
            logger.debug("{}, no existing Primary Key for {}".format(E, insertion[0]))
            if ('existing_key' not in locals()):
                logger.debug("double check for existing_key {}, no existing_key.".format(insertion[0]))
                differences = 0
                existing_key = None

        if (existing_key is not None) and (differences == 0):  # check if the primary key exists and list has 24 hour values
            logger.debug("Primary key %s exists, has %i entries and %i differences, skipping!" % (self.date, lenX, differences))
            return
        else:
            try:
                logger.debug("Creating primary key %s with %i entries and/or %i differences. Overwriting and appending data!" % (self.date, lenX, differences))
            except Exception as E:
                logger.debug("existing_key variable was not created, assigning None")
                logger.error(E)

        try:
            cur.execute((self.sql % (self.table, self.type)), converted_insertion)
            logger.debug("Updating the database with: {}".format(converted_insertion))
        except Exception as E:
            logger.error("An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, converted_insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def write_dayhours(self, conn, insertion, table, type):
        """Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, week, month, monthname, day, yearday, values per hour

        example insertion:
            ('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
        """
        self.table = table
        self.type = type
        self.sql = Youless.sql("queries")["i_dayhours"]
        self.query = Youless.sql("queries")["s_table"]
        self.datequery = (insertion[0].strip(),)  # create primary key check
        self.date = insertion[0]  # create primary key check

        cur = conn.cursor()
        self.check = cur.execute((self.query % self.table), self.datequery)  # check the database for existing primary keys

        x = insertion[7]  # x is string representation of list
        x = ast.literal_eval(x)  # convert x to real list
        lenX = len(x)

        existing_entry = self.check.fetchall()  # fetch the complete entry from the database

        try:
            existing_key = existing_entry[0][0]  # assign existing key
            existing_values = existing_entry[0][7]  # assign existing value string
            existing_values = ast.literal_eval(existing_values)  # convert string representation of list to real list
            first_set = set(existing_values)  # create set from existing values
            sec_set = set(x)  # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set)  # compare differences between two sets
            differences = len(differences)
        except Exception:
            logger.debug("no existing Primary Key for {}".format(insertion[0]))
            if ('existing_key' not in locals()):
                logger.debug("double check for existing_key, no existing_key.")
                existing_key = None

        if (existing_key is not None) and (differences == 0):  # check if the primary key exists and list has 24 hour values
            logger.debug("Primary key %s exists, has %i entries and %i differences, skipping!" % (self.date, lenX, differences))
            return
        else:
            try:
                logger.debug("Primarykey %s has %i entries and/or %i differences. Overwriting and appending data!" % (self.date, lenX, differences))
            except Exception:
                logger.debug("existing_key variable was not created, assigning None")
        try:
            cur.execute((self.sql % (self.table, self.type)), insertion)
            logger.debug("Updating the database with: {}".format(insertion))
        except Exception as E:
            logger.error("An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def write_yeardays(self, conn, insertion, table, type):
        """Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, month, monthname, values per day

        example insertion:
            ('2020-12-01', 2020, 12, 'December',
            '[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06,
            15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')
        """
        self.table = table
        self.type = type
        self.sql = Youless.sql("queries")["i_yeardays"]
        self.query = Youless.sql("queries")["s_table"]
        self.datequery = (insertion[0].strip(),)  # create primary key check
        self.date = insertion[0]  # create primary key check

        cur = conn.cursor()
        self.check = cur.execute((self.query % self.table), self.datequery)  # check the database for existing primary keys

        x = insertion[4]  # x is string representation of list
        x = ast.literal_eval(x)  # convert x to real list
        lenX = len(x)

        m = int(insertion[2])

        existing_entry = self.check.fetchall()  # fetch the complete entry from the database

        try:
            existing_key = existing_entry[0][0]  # assign existing key
            existing_values = existing_entry[0][4]  # assign existing value string
            existing_values = ast.literal_eval(existing_values)  # convert string representation of list to real list
            first_set = set(existing_values)  # create set from existing values
            sec_set = set(x)  # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set)  # compare differences between two sets
            differences = len(differences)
        except Exception:
            logger.debug("no existing Primary Key for {}".format(insertion[0]))
            if ('existing_key' not in locals()):
                logger.debug("existing_key variable was not created, assigning None")
                existing_key = None

        if (existing_key is not None) and (differences == 0):
            logger.debug("Primary key %s exists and has %i differences, skipping!" % (insertion[0], differences))
            return
        else:
            try:
                logger.debug("Primary key is %s and has %i differences. Overwriting and appending data!" % (insertion[0], differences))
            except Exception:
                logger.debug("Primarykey did not exist. Creating new entry")

        try:
            cur.execute((self.sql % (self.table, self.type)), insertion)
            logger.debug("Updating the database with: {}".format(insertion))
        except Exception as E:
            logger.error("An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid
