#!/usr/bin/env python3
"""
    import_data.py

    This file imports data from a Youless LS120 device in to existing sqlite3 database.
"""
import sys
import datetime
import ast  # for converting string representation of a list to a list

# web
from requests import get

# sqlite
import sqlite3 as sl

# Youless setup
from .constants import Settings, Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("import_data.py started")


sys.stdin.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding
sys.stdout.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding


class parse_data:
    """
        class to retrieve data from youless, parse it into data and import it into an sqlite3 database.
    """

    def __init__(self):
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

    def create_connection(self, db_file):
        """
            Internal function to create a connection to the database
        """
        self.conn = None
        try:
            self.conn = sl.connect(db_file)
            logger.debug(("Connected to: {}".format(db_file)))
        except Exception as e:
            logger.error(e)
        return self.conn

    def insert_dayhours(self, conn, insertion, table, type):
        """
            Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, week, month, monthname, day, yearday, values per hour
            example:
            ('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
            INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
            INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
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

        existingEntry = self.check.fetchall()  # fetch the complete entry from the database

        try:
            existingKey = existingEntry[0][0]  # assign existing key
            existingValues = existingEntry[0][7]  # assign existing value string
            existingValues = ast.literal_eval(existingValues)  # convert string representation of list to real list
            first_set = set(existingValues)  # create set from existing values
            sec_set = set(x)  # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set)  # compare differences between two sets
            differences = len(differences)
        except Exception:
            logger.debug("no existing Primary Key for {}".format(insertion[0]))
            if ('existingKey' not in locals()):
                logger.debug("double check for existingKey, no existingKey.")
                existingKey = None

        if (existingKey is not None) and (differences == 0):  # check if the primary key exists and list has 24 hour values
            logger.debug("Primary key %s exists, has %i entries and %i differences, skipping!" % (self.date, lenX, differences))
            return
        else:
            try:
                logger.debug("Primarykey %s has %i entries and/or %i differences. Overwriting and appending data!" % (self.date, lenX, differences))
            except Exception:
                logger.debug("existingKey variable was not created, assigning None")
        try:
            cur.execute((self.sql % (self.table, self.type)), insertion)
            logger.debug("Updating the database with: {}".format(insertion))
        except Exception as E:
            logger.error("An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def insert_yeardays(self, conn, insertion, table, type):
        """
            Internal function to store values in sqlite3 database in the following format (all strings):
            date, year, month, monthname, values per day
            example return:
            ('2020-12-01', 2020, 12, 'December',
            '[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06,
            15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')
            INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
            INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
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

        existingEntry = self.check.fetchall()  # fetch the complete entry from the database

        try:
            existingKey = existingEntry[0][0]  # assign existing key
            existingValues = existingEntry[0][4]  # assign existing value string
            existingValues = ast.literal_eval(existingValues)  # convert string representation of list to real list
            first_set = set(existingValues)  # create set from existing values
            sec_set = set(x)  # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set)  # compare differences between two sets
            differences = len(differences)
        except Exception:
            logger.debug("no existing Primary Key for {}".format(insertion[0]))
            if ('existingKey' not in locals()):
                logger.debug("existingKey variable was not created, assigning None")
                existingKey = None

        if (existingKey is not None) and (differences == 0):
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

    def parse_days(self, etype, data):
        """
            Function to parse the information retrieved by retrieve_days

            :parse_days(etype, data)
            :etype is 'E' or 'G' for Electricity or Gas
            :data is a list with tuples retrieved by retrieve_days
        """
        self.__table = Youless.sql("dbtables")[etype][1]
        self.__type = self.__watt if etype == 'E' and etype != 'G' else self.__ltr
        self.conn = self.create_connection(Settings.path+Settings.dbname)
        logger.debug("Connected to table {}".format(self.__table))
        for item in data:
            self.insert_dayhours(self.conn, item, self.__table, self.__type)
        self.conn.close()
        logger.debug("Database connection closed...")

    def parse_months(self, etype, data):
        """
            Function to parse the information retrieved by retrieve_months

            :parse_months(etype, data)
            :etype is 'E' or 'G' for Electricity or Gas
            :data is a list with tuples retrieved by retrieve_months
        """
        self.__table = Youless.sql("dbtables")[etype][0]
        self.__type = self.__kwh if etype == 'E' and etype != 'G' else self.__m3
        self.conn = self.create_connection(Settings.path+Settings.dbname)
        logger.debug("Connected to table {}".format(self.__table))
        for item in data:
            self.insert_yeardays(self.conn, item, self.__table, self.__type)
        self.conn.close()
        logger.debug("Database connection closed...")

    def retrieve_days(self, etype):
        """
            Function to retrieve all Electricity and Gas hour values from Youless 120
            with a maximum history of 70 days back (youless max).
            returns a list with tuples of data.

            :retrieve_days(etype)
            :etype is 'E' or 'G' for Electricity or Gas
        """
        self.__urltype = self.__ele if etype == 'E' and etype != ('G', 'S') else self.__gas if etype == 'G' else self.__snul
        self.max_page = Youless.web("maxDayPage")
        self.min_page = Youless.web("minDayPage")
        self.max_hour = Youless.web("maxHour")
        self.min_hour = Youless.web("minHour")
        self.counter = self.max_page
        self.return_list = []
        while (self.counter >= self.min_page):
            self.api = get(self.__url + self.__urltype + self.__json + self.__day + str(self.counter))
            readapi = self.api.json()
            json_date = datetime.datetime.strptime(readapi['tm'], '%Y-%m-%dT%H:%M:%S')
            date = json_date.date()
            year = json_date.date().strftime('%Y')
            week_no = json_date.date().strftime('%W')
            month_no = json_date.date().strftime('%m')
            month_name = json_date.date().strftime('%B')
            month_day = json_date.date().strftime('%d')
            year_day = json_date.date().strftime('%j')
            raw_values = readapi['val']
            lst = []
            self.hours = self.min_hour
            for y, s in enumerate(raw_values):
                try:
                    raw_values[y] = s.strip()
                    raw_values[y] = float(s.replace(',', '.'))
                except AttributeError:
                    pass
                except IndexError:
                    break
                finally:
                    lst.append(raw_values[y])
            if raw_values[y] is None:
                lst.pop()
            strlst = '{}'.format(lst)
            task = (str(date), int(year), int(week_no), int(month_no), month_name, int(month_day), int(year_day), strlst)
            self.return_list.append(task)
            lst.clear()
            self.counter -= 1
        return self.return_list

    def retrieve_months(self, etype):
        """
            Function to retrieve days per month from Youless 120
            up to 11 months back for Electricity and Gas.
            returns a list with tuples of data.

            :retrieve_months(etype)
            :etype is 'E' or 'G' for Electricity or Gas
        """

        self.__urltype = self.__ele if etype == 'E' and etype != ('G', 'S') else self.__gas if etype == 'G' else self.__snul
        self.__type = self.__kwh if etype == 'E' and etype != 'G' else self.__m3
        self.max_page = Youless.web("maxMonthPage")
        self.min_page = Youless.web("minMonthPage")
        self.counter = self.max_page
        self.return_list = []
        while (self.counter >= self.min_page):
            self.api = get(self.__url + self.__urltype + self.__json + self.__month + str(self.counter))
            readapi = self.api.json()
            json_date = datetime.datetime.strptime(readapi['tm'], '%Y-%m-%dT%H:%M:%S')
            date = json_date.date()
            year = json_date.date().strftime('%Y')
            month_no = json_date.date().strftime('%m')
            month_name = json_date.date().strftime('%B')
            raw_values = readapi['val']
            lst = []
            for y, s in enumerate(raw_values):
                try:
                    raw_values[y] = s.strip()
                    raw_values[y] = float(s.replace(',', '.'))
                except AttributeError:
                    pass
                except IndexError:
                    break
                finally:
                    lst.append(raw_values[y])
            if raw_values[y] is None:
                lst.pop()
            strlst = '{}'.format(lst)
            task = (str(date), int(year), int(month_no), month_name, strlst)
            self.return_list.append(task)
            lst.clear()
            self.counter -= 1
        return self.return_list


def main():
    # check if database exists
    try:
        f = open(Settings.path+Settings.dbname, 'rb')
    except Exception:
        logger.error("database not found")
        sys.exit(1)  # exiting with a non zero value is better for returning from an error
    else:
        f.close()
        for type in Youless.sql("dbtables").keys():
            parse_data().parse_days(type, parse_data().retrieve_days(type))
            parse_data().parse_months(type, parse_data().retrieve_months(type))


if __name__ == '__main__':
    main()
