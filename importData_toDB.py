import sys, os, datetime, re, time
import requests
from requests import get
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError
import ast # for converting string representation of a list to a list

# import globals
# import globals as gl
from globals import *

sys.stdin.reconfigure(encoding=Vars.web("ENCODING")) # set encoding
sys.stdout.reconfigure(encoding=Vars.web("ENCODING")) # set encoding

class parseData:

    def __init__(self):
        self.__headers = Vars.web("HEADERS") # acceptable html headers
        self.__url = Vars.web("URL") # base url
        self.__ele = Vars.web("ELE")
        self.__gas = Vars.web("GAS")
        self.__snul = Vars.web("S0")
        self.__json = Vars.web("JSON")
        self.__month = Vars.web("M")
        self.__day = Vars.web("W")
        self.__kwh = Vars.conf("valuenaming")[0]
        self.__m3 = Vars.conf("valuenaming")[1]
        self.__watt = Vars.conf("valuenaming")[2]
        self.__ltr = Vars.conf("valuenaming")[3]

    def create_connection(self, db_file):
        """
        Function to create a connection to the database
        """
        self.conn = None
        try:
            self.conn = sl.connect(db_file)
            dbg(lambda: ("Connected to: {}".format(db_file)))
        except Error as e:
            log(lambda: e)
        return self.conn

    def insert_dayhours(self, conn, insertion, table, type):
        """
        Store values in sqlite3 database in the following format (all strings):
        date, year, week, month, monthname, day, yearday, values per hour
        example:
        ('2021-04-03', 2021, 13, 4, 'April', 3, 93, '[428.0, 385.0, 400.0, 391.0, 386.0, 398.0, 403.0, 485.0, 759.0, 611.0, 650.0, 1225.0, 626.0, 940.0, 534.0, 630.0, 751.0, 630.0, 1194.0, 951.0, 934.0, 893.0, 628.0, 581.0]')
        INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
        INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
        """
        # log(lambda: "Opening table dayhours_e")
        # self.table = 'dayhours_e' if (type == 'E') else 'dayhours_g'
        self.table = table
        self.type = type
        self.sql = Vars.conf("queries")["i_dayhours"]
        # self.query = '''
        #              SELECT EXISTS(SELECT 1 FROM dayhours_e WHERE date=? COLLATE NOCASE) LIMIT 1
        #              '''
        self.query = Vars.conf("queries")["s_table"]
        self.datequery = (insertion[0].strip(),) # create primary key check
        self.date = insertion[0] # create primary key check

        cur = conn.cursor()

        self.check = cur.execute((self.query % self.table), self.datequery) # check the database for existing primary keys

        x = insertion[7] # x is string representation of list
        x = ast.literal_eval(x) # convert x to real list
        lenX = len(x)

        existingEntry = self.check.fetchall() # fetch the complete entry from the database

        try:
            existingKey = existingEntry[0][0] # assign existing key
            existingValues = existingEntry[0][7] # assign existing value string
            existingValues = ast.literal_eval(existingValues) # convert string representation of list to real list
            first_set = set(existingValues) # create set from existing values
            sec_set = set(x) # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set) # compare differences between two sets
            differences = len(differences)
        except:
            dbg(lambda: "no existing Primary Key for {}".format(insertion[0]))
            if ('existingKey' not in locals()):
                dbg(lambda: "double check for existingKey, no existingKey.")
                existingKey = None


        # for i in existingValues:
        #     i = float(i)

        # log(lambda: type(existingValues[0]))
        # log(lambda: type(x[0]))
        # log(lambda: x)
        # log(lambda: existingValues)

        #log(lambda: first_set)

        #log(lambda: sec_set)

        # log(lambda: differences)

        # log(lambda: differences)
        # log(lambda: len(differences)) # check if there are 1 ore more differences

        if (existingKey is not None) and (differences == 0): # check if the primary key exists and list has 24 hour values
            log(lambda: "Primary key %s exists, has %i entries and %i differences, skipping!" % (self.date, lenX, differences))
            # for i in x:
            #     log(lambda: i)
            # log(lambda: self.check2.fetchone())
            return
        else:
            try:
                log(lambda: "Primarykey %s has %i entries and/or %i differences. Overwriting and appending data!" % (self.date, lenX, differences))
            except:
                log(lambda: "existingKey variable was not created, assigning None")
        try:
            cur.execute((self.sql % (self.table, self.type)), insertion)
            log(lambda: "Updating the database with: {}".format(insertion))
        except Exception as E:
            log(lambda: "An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def insert_yeardays(self, conn, insertion, thismonth, table, type):
        """
        Store values in sqlite3 database in the following format (all strings):
        date, year, month, monthname, values per day
        example:
        ('2020-12-01', 2020, 12, 'December', '[18.85, 15.12, 19.72, 13.76, 13.93, 20.7, 17.66, 18.57, 14.14, 13.23, 12.72, 15.38, 16.89, 16.06, 15.39, 22.16, 15.0, 15.34, 12.61, 17.17, 18.85, 15.25, 20.22, 13.51, 15.35, 13.49, 12.99, 21.87, 14.2, 16.7, 15.45]')
        INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
        INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
        """
        # log(lambda: "Opening table yeardays_e")
        self.table = table
        self.type = type

        self.sql = Vars.conf("queries")["i_yeardays"]
        # self.query = '''
        #              SELECT EXISTS(SELECT 1 FROM yeardays_e WHERE date=? COLLATE NOCASE) LIMIT 1
        #              '''
        self.query = Vars.conf("queries")["s_table"]
        self.datequery = (insertion[0].strip(),) # create primary key check
        self.date = insertion[0] # create primary key check

        cur = conn.cursor()
        self.check = cur.execute((self.query % self.table), self.datequery) # check the database for existing primary keys

        # log(lambda: type(insertion))
        # log(lambda: insertion[0]) # returns the primary key
        # log(lambda: self.check.fetchone()[0]) # returns 1 if primary key exists
        # log(lambda: monthnow) # returns the month now check

        x = insertion[4] # x is string representation of list
        x = ast.literal_eval(x) # convert x to real list
        lenX = len(x)

        m = int(insertion[2])

        existingEntry = self.check.fetchall() # fetch the complete entry from the database

        try:
            existingKey = existingEntry[0][0] # assign existing key
            existingValues = existingEntry[0][4] # assign existing value string
            existingValues = ast.literal_eval(existingValues) # convert string representation of list to real list
            first_set = set(existingValues) # create set from existing values
            sec_set = set(x) # create set from new values
            differences = (first_set - sec_set).union(sec_set - first_set) # compare differences between two sets
            differences = len(differences)
        except:
            dbg(lambda: "no existing Primary Key for {}".format(insertion[0]))
            if ('existingKey' not in locals()):
                log(lambda: "existingKey variable was not created, assigning None")
                existingKey = None

        # existingKey = existingEntry[0][0] # assign existing key
        # existingValues = existingEntry[0][4] # assign existing value string
        # existingValues = ast.literal_eval(existingValues) # convert string representation of list to real list

        # first_set = set(existingValues) # create set from existing values
        # log(lambda: first_set)
        # sec_set = set(x) # create set from new values
        # log(lambda: sec_set)
        # differences = (first_set - sec_set).union(sec_set - first_set) # compare differences between two sets
        # log(lambda: differences)
        # differences = len(differences)
        # log(lambda: differences)

        # if (existingEntry) and (insertion[0] != thismonth): # check if the primary key exists and is not the current month
        #     if (differences == 0):
        #         if (m in lowMonths) and (len(x) == 30):
        #             log(lambda: "Primary key %s exists, should have 30 days and has %i days, skipping!" % (insertion[0], len(x)))
        #             return
        #         elif (m in highMonths) and (len(x) == 31):
        #             log(lambda: "Primary key %s exists, should have 31 days and has %i days, skipping!" % (insertion[0], len(x)))
        #             return
        #         elif (m == excMonth) and (len(x) >= 28):
        #             log(lambda: "Primary key %s exists, should have 28 or 29 days and has %i days, skipping!" % (insertion[0], len(x)))
        #             return
        #         else:
        #             log(lambda: "Month not complete, continuing to update")
        #     else:
        #         log(lambda: "Month has %i differences, continuing to update" % differences)
        if (existingKey is not None) and (differences == 0):
            log(lambda: "Primary key %s exists and has %i differences, skipping!" % (insertion[0], differences))
            return
        else:
            try:
                log(lambda: "Primary key is %s and has %i differences. Overwriting and appending data!" % (insertion[0], differences))
            except:
                log(lambda: "Primarykey did not exist. Creating new entry")

        # if (insertion[0] == monthnow): # check if the primary key is the same as the current month
        #     log(lambda: "We have a hit! %s" % insertion[0])
        #

        try:
            # t = (self.sql % self.table, self.type)
            # dbg(lambda: t)
            cur.execute((self.sql % (self.table, self.type)), insertion)
            dbg(lambda: "Updating the database with: {}".format(insertion))
        except Exception as E:
            log(lambda: "An error occured, skipping the update.\n Error: {}\n sql: {}".format(E, insertion))
            pass
        conn.commit()
        return cur.lastrowid

    def parseDays(self):
        """
        Retrieve daily Electricity and Gas hour value from Youless 120 with a maximum history of 70 days back
        """
        for x in Vars.conf("dbtables"):
            self.__table = Vars.conf("dbtables")[x][1]
            self.__urltype = self.__ele if x == 'E' and x != ('G', 'S') else self.__gas if x == 'G' else self.__snul
            self.__type = self.__watt if x == 'E' and x != 'G' else self.__ltr
            self.maxPage = Vars.web("maxDayPage")
            self.minPage = Vars.web("minDayPage")
            self.maxHour = Vars.web("maxHour")
            self.minHour = Vars.web("minHour")
            self.counter = self.maxPage
            self.conn = self.create_connection(Vars.path+Vars.dbname)
            log(lambda: "Connected to table {}".format(self.__table))
            while (self.counter >= self.minPage):
                self.api = get(self.__url + self.__urltype + self.__json + self.__day + str(self.counter))
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
                self.insert_dayhours(self.conn, task, self.__table, self.__type)
                lst.clear()
                self.counter -= 1
            self.conn.close()
            log(lambda: "Database connection closed...")

    def parseMonths(self):#, type):
        """
        Retrieve days per month from Youless 120 up to 11 months back for Electricity and Gas
        and call insert_yeardays() with the values
        """
        # self.tablecount = len(Variables.dbtables)
        # self.count = 0
        # if (type == 'E'):
        #     self.__type = self.__ele
        # elif (type == 'G'):
        #     self.__type = self.__gas

        for x in Vars.conf("dbtables"):
            self.__table = Vars.conf("dbtables")[x][0]
            self.__urltype = self.__ele if x == 'E' and x != ('G', 'S') else self.__gas if x == 'G' else self.__snul
            self.__type = self.__kwh if x == 'E' and x != 'G' else self.__m3
            self.maxPage = Vars.web("maxMonthPage")
            self.minPage = Vars.web("minMonthPage")
            self.counter = self.maxPage
            self.conn = self.create_connection(Vars.path+Vars.dbname)
            log(lambda: "Connected to table {}".format(self.__table))
            while (self.counter >= self.minPage):
                self.api = get(self.__url + self.__urltype + self.__json + self.__month + str(self.counter))
                readapi = self.api.json()
                jsonDate = datetime.datetime.strptime(readapi['tm'], '%Y-%m-%dT%H:%M:%S')
                date = jsonDate.date()
                year = jsonDate.date().strftime('%Y')
                monthNo = jsonDate.date().strftime('%m')
                monthName = jsonDate.date().strftime('%B')
                thismonth = Runtime.dt.strftime('%Y-%m-01')
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
                self.insert_yeardays(self.conn, task, str(thismonth), self.__table, self.__type)
                lst.clear()
                self.counter -= 1
            self.conn.close()
            log(lambda: "Database connection closed...")

def main():
    # check if database exists
    try:
        f = open(Vars.path+Vars.dbname, 'rb')
    except:
        print("database not found")
        sys.exit(1) # exiting with a non zero value is better for returning from an error
    else:
        f.close()
        parseData().parseDays()
        parseData().parseMonths()
    # finally:
        # f.close()



if __name__ == '__main__':
    main()
