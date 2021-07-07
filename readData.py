"""
    Read data from sqlite database
"""

import sys, os, datetime, re, time, locale
import calendar
import sqlite3 as sl
from sqlite3 import IntegrityError
import ast # for converting string representation of a list to a list

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# youless specific
from globals import *

# set language
Vars.youlessLocale()

class retrieveData:
    # global class variables
    __path = Vars.path + Vars.dbname

    def __init__(self):
        """
        Automatic database connection when called
        """
        self.__db_file = retrieveData.__path
        log(lambda: "Starting database connection...")
        self.conn = None
        try:
            self.conn = sl.connect(self.__db_file)
            log(lambda: "Connected to: %s" % self.__db_file)
        except Error as e:
            log(lambda: e)

    def retrieve_hours(self, table, year, month, startday, starthour, *args):
        """
        Retrieve data from table dayhours_X and return list with items.
        Retrieve hour data for given year, month and days with a minimum of 1 hour and a maximum of 24 hours in a list with hours and values.
        Since we dont know if the end day/hour is the same as the start day/hour we use *args to accept this.
        When only startday and starthour is given, only that single hour will be retrieved
        Examples:
            retrieve_hours('dayhours_g', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6
            retrieve_hours('dayhours_e', 2020, 10, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12
            retrieve_hours('dayhours_e', 2020, 11, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18
        table as string
        year as integer
        month as integer (min is 1, max is 12)
        startday as integer (min is 1, max is 30)
        endday as integer (min is 2, max is 31)
        starthour as integer (min is 0 (00:00), max is 23 (23:00))
        endhour as integer (min is 1 (01:00), max is 24 (24:00))
        """
        self.table = table
        self.year = year
        self.month = month
        self.startday = startday
        self.starthour = starthour
        self.hourlist = []
        if (len(args) == 2):
            self.endday = args[0]
            self.endhour = args[1]
            self.query = (Vars.conf("queries")["s_dayhours2"] % (self.table, self.year, self.month, self.startday, self.endday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.endday,self.endhour,self.hourlist]
        elif (len(args) == 1):
            self.endhour = args[0]
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.endhour,self.hourlist]
        else:
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year,self.month,self.startday,self.starthour,self.hourlist]
        log(lambda: "Starting hour retrieval from table %s" % self.table)
        self.cur = self.conn.cursor()
        with self.conn:
            data = self.cur.execute(self.query)
            rows = (len(self.cur.fetchall()))
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query) # execute query again because fetchall() mangles the data to a list of tuples with strings
                rowcount = 0
                for row in data:
                    rowcount += 1
                    self.values = row[7] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list

                    for n, v in enumerate(self.values):
                        self.values[n] = int(self.values[n])
                        if (rowcount == 1) and (n >= self.starthour):
                            self.hourlist.append((n, v))
                            if (len(args) == 1) and (n == self.endhour):
                                break
                        elif (rowcount == 2) and (n <= self.endhour):
                            self.hourlist.append((n, v))
            else:
                return 0

        self.conn.close()
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_day(self, year, month, day, table):
        """
        Retrieve data from table dayhours_X and return list with items.
        Retrieves day data for given year, month and day in a list with hours and values.
        retrieve_day(2021, 1, 19, 'dayhours_e')
        year as integer
        month as integer
        day as integer
        table as string
        """
        self.year = year
        self.month = month
        self.day = day
        self.table = table
        log(lambda: "Starting day retrieval %d %d %d from table %s" % (self.year, self.month, self.day, self.table))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Vars.conf("queries")["s_dayhours"] % (self.table, str(self.year), str(self.month), str(self.day)))
            data = self.cur.execute(self.query)
            rows = len(self.cur.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query) # execute query again because fetchall() mangles the data to a list of tuples with strings
                for row in data:
                    self.values = row[7] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                #     tmp = row[7]
                #     tmp = tmp.replace(" ", "")
                #     tmp = tmp.replace("[", "")
                #     tmp = tmp.replace("]", "")
                #     tmp = tmp.split(',')
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0
        self.conn.close()
        # self.values = tmp[:]
        self.lst = [self.year,self.month,self.day,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_month(self, year, month, table):
        """
        Retrieve data from table yeardays_X and return list.
        Retrieves monthdata for given month of given year in a list with days and values
        retrieve_month(2021, 1, 'yeardays_e')
        year as integer
        month as integer
        table as string
        """
        self.year = year
        self.month = month
        self.table = table
        log(lambda: "Starting month retrieval %d %d from table %s" % (self.year, self.month, self.table))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Vars.conf("queries")["s_yeardays"] % (self.table, str(self.year), str(self.month)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                for row in data:
                    self.values = row[4] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                    # tmp = row[4]
                    # tmp = tmp.replace(" ", "")
                    # tmp = tmp.replace("[", "")
                    # tmp = tmp.replace("]", "")
                    # tmp = tmp.split(',')
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0
        self.conn.close()
        # self.values = tmp[:] # copy tmp list to values list
        self.lst = [self.year,self.month,self.values]
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

    def retrieve_year(self, year, totals, table):
        """
        Retrieve data from table yeardays_X and return list with items.
        Retrieves available data for given year per month and day in values
        Returns either month totals or day totals for the entire year.
        retrieve_year(2021, 2, 'yeardays_g')
        year as integer
        totals as integer (1 is month totals, 2 is day totals)
        table as string
        """
        self.year = year
        self.totals = totals
        self.table = table
        if (self.totals != 1 and self.totals != 2):
            log(lambda: "error: type can only be 1 or 2")
            return "error: type can only be 1 or 2"
        log(lambda: "Starting year retrieval %d" % (self.year))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Vars.conf("queries")["so_yeardays"] % (self.table, str(self.year)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            log(lambda: "Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                self.lst = []
                for row in data:
                    self.values = row[4] # x is string representation of list
                    self.values = ast.literal_eval(self.values) # convert x to real list
                    # tmp = row[4]
                    # tmp = tmp.replace(" ", "")
                    # tmp = tmp.replace("[", "")
                    # tmp = tmp.replace("]", "")
                    # tmp = tmp.split(',')
                    total = 0
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
                        total += float(self.values[v])
                    if (self.totals == 1): # month totals
                        self.tmplst = [[row[1], row[2], row[3], int(total)]]
                    elif (self.totals == 2): # day totals
                        self.tmplst = [[row[1], row[2], row[3], self.values]]
                    self.lst.extend(self.tmplst)
                    self.tmplst.clear()
            else:
                return 0
        self.conn.close()
        log(lambda: "Retrieved list:")
        log(lambda: self.lst)
        return self.lst

def main():
    log(lambda: "I do not run on my own...")

if __name__ == '__main__':
        main()        