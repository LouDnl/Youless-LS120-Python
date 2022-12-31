#!/usr/bin/env python3
"""
    File name: db_retrieve_data.py
    Author: LouDFPV
    Date created: 25/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file retrieves data from youless sqlite3 database and returns it
"""
import ast  # for converting string representation of a list to a list
import calendar
# initialize logging
import logging
from datetime import datetime, timedelta

from dateutil import parser

# Youless setup
from LS120 import Youless, db_connect

logger = logging.getLogger(__name__)
logger.debug("db_retrieve_data.py started")


class retrieve_data:
    """class to retrieve data within a defined set from the youless database"""

    def __init__(self) -> None:
        self.conn = db_connect().connect_and_return_read()

    def retrieve_hours(self, table, year, month, startday, starthour, *args):
        """Retrieve data from table dayhours_X and return list with items.
        Retrieve hour data for given year, month and days with a minimum of 1 hour and a maximum of 24 hours in a list with hours and values.
        Since we dont know if the end day/hour is the same as the start day/hour we use *args to accept this.
        When only startday and starthour is given, only that single hour will be retrieved.

        Examples:
            retrieve_hours('dayhours_g', 2021, 3, 2, 3, 3, 6) # year: 2021, month: 3, startday: 2, starthour: 5, endday: 3, endhour: 6\n
            retrieve_hours('dayhours_e', 2020, 10, 1, 12) # year: 2020, month: 10, startday: 1, starthour: 12\n
            retrieve_hours('dayhours_e', 2020, 11, 2, 11, 18) # year: 2020, month: 11, startday: 2, starthour: 11, endhour: 18\n

        args:
        :table as string
        :year as integer
        :month as integer (min is 1, max is 12)
        :startday as integer (min is 1, max is 30)
        :endday as integer (min is 2, max is 31)
        :starthour as integer (min is 0 (00:00), max is 23 (23:00))
        :endhour as integer (min is 1 (01:00), max is 24 (24:00))
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
            self.query = (Youless.sql("queries")["s_dayhours2"] % (self.table, self.year, self.month, self.startday, self.endday))
            self.lst = [self.year, self.month, self.startday, self.starthour, self.endday, self.endhour, self.hourlist]
        elif (len(args) == 1):
            self.endhour = args[0]
            self.query = (Youless.sql("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year, self.month, self.startday, self.starthour, self.endhour, self.hourlist]
        else:
            self.query = (Youless.sql("queries")["s_dayhours"] % (self.table, self.year, self.month, self.startday))
            self.lst = [self.year, self.month, self.startday, self.starthour, self.hourlist]
        logger.debug("Starting hour retrieval from table %s" % self.table)
        self.cur = self.conn.cursor()
        with self.conn:
            data = self.cur.execute(self.query)
            rows = (len(self.cur.fetchall()))
            logger.debug("Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query)  # execute query again because fetchall() mangles the data to a list of tuples with strings
                rowcount = 0
                for row in data:
                    rowcount += 1
                    self.values = row[7]  # x is string representation of list
                    self.values = ast.literal_eval(self.values)  # convert x to real list

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
        logger.debug("Retrieved list:")
        logger.debug(self.lst)
        return self.lst

    def retrieve_day(self, year, month, day, table):
        """Retrieve data from table dayhours_X and return list with items.
        Retrieves day data for given year, month and day in a list with hours and values.

        example:
        retrieve_day(2021, 1, 19, 'dayhours_e')

        args:
        :year as integer
        :month as integer
        :day as integer
        :table as string
        """
        self.year = year
        self.month = month
        self.day = day
        self.table = table
        logger.debug("Starting day retrieval %d %d %d from table %s" % (self.year, self.month, self.day, self.table))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Youless.sql("queries")["s_dayhours"] % (self.table, str(self.year), str(self.month), str(self.day)))
            data = self.cur.execute(self.query)
            rows = len(self.cur.fetchall())
            logger.debug("Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.cur.execute(self.query)  # execute query again because fetchall() mangles the data to a list of tuples with strings
                for row in data:
                    self.values = row[7]  # x is string representation of list
                    self.values = ast.literal_eval(self.values)  # convert x to real list
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0
        self.conn.close()

        self.lst = [self.year, self.month, self.day, self.values]
        logger.debug("Retrieved list:")
        logger.debug(self.lst)
        return self.lst

    def retrieve_month(self, year, month, table):
        """Retrieve data from table yeardays_X and return list.
        Retrieves monthdata for given month of given year in a list with days and values

        example:
        retrieve_month(2021, 1, 'yeardays_e')

        args:
        :year as integer
        :month as integer
        :table as string
        """
        self.year = year
        self.month = month
        self.table = table
        logger.debug("Starting month retrieval %d %d from table %s" % (self.year, self.month, self.table))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Youless.sql("queries")["s_yeardays"] % (self.table, str(self.year), str(self.month)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            logger.debug("Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                for row in data:
                    self.values = row[4]  # x is string representation of list
                    self.values = ast.literal_eval(self.values)  # convert x to real list
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
            else:
                return 0
        self.conn.close()

        self.lst = [self.year, self.month, self.values]
        logger.debug("Retrieved list:")
        logger.debug(self.lst)
        return self.lst

    def retrieve_year(self, year, totals, table):
        """Retrieve data from table yeardays_X and return list with items.
        Retrieves available data for given year per month and day in values.
        Returns either month totals or day totals for the entire year.

        example:
        retrieve_year(2021, 2, 'yeardays_g')

        args:
        :year as integer
        :totals as integer (1 is month totals, 2 is day per month totals)
        :table as string
        """
        self.year = year
        self.totals = totals
        self.table = table
        if (self.totals != 1 and self.totals != 2):
            logger.error("error: type can only be 1 or 2")
            return "error: type can only be 1 or 2"
        logger.debug("Starting year retrieval %d" % (self.year))
        self.cur = self.conn.cursor()
        with self.conn:
            self.query = (Youless.sql("queries")["so_yeardays"] % (self.table, str(self.year)))
            data = self.conn.execute(self.query)
            rows = len(data.fetchall())
            logger.debug("Rows retrieved: %d" % rows)
            if (rows >= 1):
                data = self.conn.execute(self.query)
                self.lst = []
                for row in data:
                    self.values = row[4]  # x is string representation of list
                    self.values = ast.literal_eval(self.values)  # convert x to real list
                    total = 0
                    for v, n in enumerate(self.values):
                        self.values[v] = float(self.values[v])
                        total += float(self.values[v])
                    if (self.totals == 1):  # month totals
                        self.tmplst = [[row[1], row[2], row[3], int(total)]]
                    elif (self.totals == 2):  # day totals
                        self.tmplst = [[row[1], row[2], row[3], self.values]]
                    self.lst.extend(self.tmplst)
                    self.tmplst.clear()
            else:
                return 0
        self.conn.close()
        logger.debug("Retrieved list:")
        logger.debug(self.lst)
        return self.lst


class retrieve_custom_data:
    """class to retrieve custom (based on kwargs) data from the youless database"""

    def __init__(self) -> None:
        self.conn = db_connect().connect_and_return_read()

    def check_existence(self, **kwargs):
        """function to check if item exists in sqlite database.\n
        returns 1 if row exists and 0 if not.

        :table= str
        :column= str
        :item= str/int (int gets transformed to str in process)
        """
        if self.conn is None:
            return None
        self.table = kwargs.get('table')
        self.column = kwargs.get('column')
        self.item = kwargs.get('item')
        self.q = Youless.sql('queries')['if_exists']
        self.query = self.q.format(self.table, self.column, self.item)
        self.cur = self.conn.cursor()
        with self.conn:
            self.data = self.cur.execute(self.query)
        self.outcome = [row for row in self.data]
        self.conn.close()
        return int(self.outcome[0][0])

    def get_item(self, **kwargs):
        """returns item from database corresponding to the given query and kwargs

        examples:
            retrieve_custom_data().get_item(query='select_one_and',
                                            select=('*'),
                                            table='dayhours_e',
                                            id='year',
                                            item='2021',
                                            id2='yearday',
                                            item2='44')
            retrieve_custom_data().get_item(query='select_one',
                                            select='yearday,watt',
                                            table='dayhours_e',
                                            id='year',
                                            item='2021')

        kwargs:
        :query= str
        :select= str
        :table= str
        :id= str
        :item= str
        :id2= str (optional)
        :item2= str (optional)
        """
        if self.conn is None:
            return None
        self.q = Youless.sql('queries')[kwargs.get('query')]
        self.query = self.q % tuple(kwargs.values())[1:]
        self.cur = self.conn.cursor()
        with self.conn:
            self.data = self.cur.execute(self.query)
        self.outcome = [row for row in self.data]
        self.conn.close()
        return self.outcome

    def get_yeardays(self, **kwargs):
        """returns list of all occuring day numbers (zero padded).
            given a weekday in a date period\n
            given a date period

        examples:
            get_yeardays(start=datetime(2021,1,1), end=datetime(2021,12,31), day='wednesday')\n
            get_yeardays(start=datetime(2021,3,1), end=datetime(2021,3,31))

        kwargs:
        :start= datetime(year,month,day)
        :end= datetime(year,month,day)
        :day= str e.g. 'monday'
        """
        self.weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.day = kwargs.get('day').lower() if 'day' in kwargs else None
        self.day_calc = (self.start + timedelta(days=i) for i in range((self.end - self.start).days + 1))
        yearday_list = [d for d in self.day_calc if d.weekday() in [self.weekdays.index(self.day), ]] if self.day is not None else [d for d in self.day_calc if d.weekday() in [n for n, d in enumerate(self.weekdays)]]
        return [d.date().strftime('%j') for d in yearday_list]

    def get_date_range_from_week(self, **kwargs):
        """returns start and enddate fomr given weeknumber in given year.
            source: http://mvsourcecode.com/python-how-to-get-date-range-from-week-number-mvsourcecode/

        example:
            get_date_range_from_week(year=2020,week=24)

        kwargs:
        :year= int
        :week= int
        """
        self.year = kwargs.get('year')
        self.week = kwargs.get('week')
        self.first_day = datetime.strptime(f'{self.year}-W{int(self.week)}-1', "%Y-W%W-%w")
        self.last_day = self.first_day + timedelta(days=6.9)
        return self.year, self.week, self.first_day, self.last_day

    def get_dayhours_average(self, **kwargs):
        """gets data from table dayhours_X based on yearday numbers and return average for:
            :specified weekday in a year,
            :specified week in a year,
            :specified month in a year,
            :specified weekday in a month in a year.

        kwargs:
        :year= int: 2021
        :day= dayname
        :month= monthname
        :etype= 'E' or 'G'
        """
        if 'year' in kwargs:  # check if year is passed as keyword argument
            self.year = kwargs.get('year')
            self.start = parser.parse(f'{self.year} 1 1')  # a full year is always from january 1st to december 31st
            self.end = parser.parse(f'{self.year} 12 31')  # a full year is always from january 1st to december 31st
            # self.start = datetime(self.year, 1, 1)  # a full year is always from january 1st to december 31st
            # self.end = datetime(self.year, 12, 31)  # a full year is always from january 1st to december 31st
        if 'year' in kwargs and 'month' in kwargs:
            self.month = kwargs.get('month').lower().capitalize()
            self.start = parser.parse(f'{self.year} {self.month} 1')  # a month always starts at day 1, it is always the same
            self.end = parser.parse(f'{self.year} {self.month} {calendar.monthrange(self.year, self.start.month)[1]}')  # get last day of month from calendar
            # self.start = datetime(self.year, datetime.strptime(self.month, '%B').month, 1)  # a month always starts at day 1, it is always the same
            # self.end = datetime(self.year,
            #                     datetime.strptime(self.month, '%B').month,
            #                     calendar.monthrange(self.year, datetime.strptime(self.month, '%B').month)[1])  # get last day of month from calendar
        if 'day' in kwargs:
            self.day = kwargs.get('day').lower().capitalize()
        if 'week' in kwargs:
            self.week = kwargs.get('week')
            self.start = retrieve_custom_data().get_date_range_from_week(year=self.year, week=self.week)[2]
            self.end = retrieve_custom_data().get_date_range_from_week(year=self.year, week=self.week)[3]
        if 'etype' in kwargs:
            self.table = Youless.sql('dbtables')[kwargs.get('etype')][1]
            self.select = Youless.sql('av_select')[kwargs.get('etype')]

        if 'day' not in kwargs:
            self.get_yeardays = retrieve_custom_data().get_yeardays(start=self.start, end=self.end)
        else:
            self.get_yeardays = retrieve_custom_data().get_yeardays(start=self.start, end=self.end, day=self.day)
        logger.debug("get_yeardays: %s" % self.get_yeardays)

        check_exist = [yearday.lstrip('0') for yearday in self.get_yeardays if retrieve_custom_data().check_existence(table=self.table, column='yearday', item=yearday) == 1]
        logger.debug("exists yearday check: %s" % check_exist)
        if check_exist == []:
            return None

        self.get_item = [[i for i in retrieve_custom_data().get_item(query='select_one_and',
                                                                     select=self.select,
                                                                     table=self.table,
                                                                     id='year',
                                                                     item=self.year,
                                                                     id2='yearday',
                                                                     item2=n)] for n in check_exist]
        logger.debug("get_item: %s" % self.get_item)

        lists = [list(elem[0]) for elem in self.get_item]  # remove nested tuple and change to list
        lists = [[elem[0], ast.literal_eval(elem[1])] for elem in lists]  # convert every 2nd item in the list to a real list (was a string)
        lists = [[elem[0], int(sum(elem[1])/len(elem[1]))] for elem in lists]  # get the sum of all values of retrieved day
        average = int(sum(elem[1] for elem in lists)/len(lists))  # get the average over all said days

        # return the average and the amount of days the average is based on including the provided kwargs
        if 'day' in dir(self):
            if 'month' in dir(self):
                return self.year, self.day, self.month, self.table, average, len(lists)
            else:
                return self.year, self.day, self.table, average, len(lists)
        elif 'month' in dir(self):
            return self.year, self.month, self.table, average, len(lists)
        else:
            return self.year, self.week, self.table, average, len(lists)
