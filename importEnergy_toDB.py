import sys, os, datetime, re, time
import requests
from requests import get
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError
import ast # for converting string representation of a list to a list

sys.stdin.reconfigure(encoding='utf-8') # set encoding
sys.stdout.reconfigure(encoding='utf-8') # set encoding

dt = datetime.datetime.today() # get current datetime

# global variables
months = (range(1,13,1)) # url months
weeks = (range(1,54,1))  # url weeks
days = (range(1,32,1))   # url days
hours = (range(1,25,1))  # url hours
years = (range(2020, 2031, 1)) # years
date_now = dt
current_date = ("{:4d}-{:02d}-{:02d}".format(dt.year,dt.month,dt.day))
current_time = ("{:02d}:{:02d}:{:02d}".format(dt.hour,dt.minute,dt.second))
month_now = date_now.month
year_now = date_now.year #% 100 # last two digits
last_year = date_now.year-1 # last year
lowMonths = (4,6,9,11)
highMonths = (1,3,5,7,8,10,12)
excMonth = 2

# path and file naming
# cwd = os.getcwd() # get current working directory
path = "t:\\workspaces\\Atom\\Youless\\"
dbname = "youless.db"

# enable debug messages
DEBUG = True
def log(s):
    """
    Usage:
    log(lambda: "TEXT")
    log(lambda: "TEXT and %s" % variable)
    """
    if DEBUG:
        print(s())

class parseData:

    def __init__(self):
        self.__headers = { "Accept-Language": "en-US, en;q=0.5"} # acceptable html headers
        self.__url = "http://192.168.0.40" # base url
        self.__ele = "/V?" # url year, week, day, hour
        self.__gas = "/W?" # url year, week, day
        self.__json = "f=j&"
        self.__month = "m=" # url represented in months, history goes to next month
        self.__day = "d=" # url represented in weeks, history goes to next week
        # self.__X = "w="  # url represented in 3 parts, shows only one day 24hrs back up to current hour
        # self.__Y = "h=" # url represented in 20 parts of one hour counting back from the current moment

    def create_connection(self, db_file):
        """
        Function to create a connection to the database
        """
        self.conn = None
        try:
            self.conn = sl.connect(db_file)
            log(lambda: ("Connected to: {}".format(db_file)))
        except Error as e:
            log(lambda: e)
        return self.conn

    def insert_dayhours(self, conn, insertion):
        """
        Store values in sqlite3 database in the following format (all strings):
        date, year, week, month, monthname, day, yearday, values per hour
        example:
        ('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
        INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
        INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
        """
        self.sql = '''
                    INSERT OR REPLACE INTO dayhours_e(date,year,week,month,monthname,day,yearday,watt)
                    VALUES(?,?,?,?,?,?,?,?)
                  '''
        self.query = '''
                     SELECT EXISTS(SELECT 1 FROM dayhours_e WHERE date=? COLLATE NOCASE) LIMIT 1
                     '''
        self.date = (insertion[0].strip(),) # create primary key check
        cur = conn.cursor()
        self.check = cur.execute(self.query, self.date) # check the database for existing primary keys

        x = insertion[7] # x is string representation of list
        x = ast.literal_eval(x) # convert x to real list

        if (self.check.fetchone()[0] == 1) and (len(x) == 24): # check if the primary key exists and list has 24 hour values
            log(lambda: "Primary key %s exists, skipping!" % insertion[0])
            return
        else:
            log(lambda: "Primary key %s has less then 24 entries. Overwriting and appending data!" % insertion[0])
        try:
            cur.execute(self.sql, insertion)
            log(lambda: "Updating the database with: {}".format(insertion))
        except Exception as E:
            log(lambda: "An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def insert_yeardays(self, conn, insertion, thismonth):
        """
        Store values in sqlite3 database in the following format (all strings):
        date, year, month, monthname, values per day
        example:
        ('2020-12-01', 2020, 12, 'December', '[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06, 15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')
        INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
        INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
        """

        self.sql = '''
                    INSERT OR REPLACE INTO yeardays_e(date,year,month,monthname,kwh)
                    VALUES(?,?,?,?,?)
                   '''
        self.query = '''
                     SELECT EXISTS(SELECT 1 FROM yeardays_e WHERE date=? COLLATE NOCASE) LIMIT 1
                     '''
        self.date = (insertion[0].strip(),) # create primary key check

        cur = conn.cursor()
        self.check = cur.execute(self.query, self.date) # check the database for existing primary keys

        # log(lambda: type(insertion))
        # log(lambda: insertion[0]) # returns the primary key
        # log(lambda: self.check.fetchone()[0]) # returns 1 if primary key exists
        # log(lambda: monthnow) # returns the month now check

        x = insertion[4] # x is string representation of list
        x = ast.literal_eval(x) # convert x to real list
        # log(lambda: x)
        # log(lambda: len(x))
        m = int(insertion[2])

        if (self.check.fetchone()[0] == 1) and (insertion[0] != thismonth): # check if the primary key exists and is not the current month
            if (m in lowMonths) and (len(x) == 30):
                log(lambda: "Primary key %s exists, should have 30 days and has %i days, skipping!" % (insertion[0], len(x)))
                return
            elif (m in highMonths) and (len(x) == 31):
                log(lambda: "Primary key %s exists, should have 31 days and has %i days, skipping!" % (insertion[0], len(x)))
                return
            elif (m == excMonth) and (len(x) >= 28):
                log(lambda: "Primary key %s exists, should have 28 or 29 days and has %i days, skipping!" % (insertion[0], len(x)))
                return
            else:
                log(lambda: "Month not complete, continuing")
        else:
            log(lambda: "Primary key %s equals month %s and is not complete. Overwriting and appending data!" % (insertion[0], thismonth))

        # if (insertion[0] == monthnow): # check if the primary key is the same as the current month
        #     log(lambda: "We have a hit! %s" % insertion[0])
        #
        try:
            cur.execute(self.sql, insertion)
            log(lambda: "Updating the database with: {}".format(insertion))
        except Exception as E:
            log(lambda: "An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def parseDays(self):
        """
        Retrieve daily hour value from Youless 120 with a maximum history of 70 days back
        """

        self.maxPage = 70
        self.minPage = 1
        self.maxHour = 24
        self.minHour = 0
        self.counter = self.maxPage
        self.conn = self.create_connection(path+dbname)
        while (self.counter >= self.minPage):
            self.api = get(self.__url + self.__ele + self.__json + self.__day + str(self.counter))
            readapi = self.api.json()
            jsonDate = datetime.datetime.strptime(readapi['tm'], '%Y-%m-%dT%H:%M:%S')
            date = jsonDate.date()
            year = jsonDate.date().strftime('%Y')
            weekNo = jsonDate.date().strftime('%W')
            monthNo = jsonDate.date().strftime('%m')
            monthName = jsonDate.date().strftime('%B')
            monthDay = jsonDate.date().strftime('%d')
            yearDay = jsonDate.date().strftime('%j')
            rawValues = readapi['val']
            lst = []
            self.hours = self.minHour
            for y, s in enumerate(rawValues):
                try:
                    rawValues[y] = s.strip()
                    rawValues[y] = float(s.replace(',', '.'))
                except AttributeError:
                    pass
                except IndexError:
                    break
                finally:
                    lst.append(rawValues[y])
            if (rawValues[y] == None):
                lst.pop()
            strlst = '{}'.format(lst)

            task = (str(date),int(year),int(weekNo),int(monthNo),monthName,int(monthDay),int(yearDay),strlst)
            self.insert_dayhours(self.conn, task)
            lst.clear()
            self.counter -= 1
        self.conn.close()
        log(lambda: "Database connection closed...")

    def parseMonths(self):
        """
        Retrieve days per month from Youless 120 up to 11 months back
        and call insert_yeardays() with the values
        """
        self.maxPage = 12
        self.minPage = 1
        self.counter = self.maxPage
        self.conn = self.create_connection(path+dbname)
        while (self.counter >= self.minPage):
            self.api = get(self.__url + self.__ele + self.__json + self.__month + str(self.counter))
            readapi = self.api.json()
            jsonDate = datetime.datetime.strptime(readapi['tm'], '%Y-%m-%dT%H:%M:%S')
            date = jsonDate.date()
            year = jsonDate.date().strftime('%Y')
            monthNo = jsonDate.date().strftime('%m')
            monthName = jsonDate.date().strftime('%B')
            thismonth = dt.strftime('%Y-%m-01')
            rawValues = readapi['val']
            lst = []
            for y, s in enumerate(rawValues):
                try:
                    rawValues[y] = s.strip()
                    rawValues[y] = float(s.replace(',', '.'))
                except AttributeError:
                    pass
                except IndexError:
                    break
                finally:
                    lst.append(rawValues[y])
            if (rawValues[y] == None):
                lst.pop()
            strlst = '{}'.format(lst)
            task = (str(date),int(year),int(monthNo),monthName,strlst)
            # log(lambda: task)
            self.insert_yeardays(self.conn, task, str(thismonth))
            lst.clear()
            self.counter -= 1
        self.conn.close()
        log(lambda: "Database connection closed...")

def main():
    parseData().parseDays()
    parseData().parseMonths()

if __name__ == '__main__':
    main()
