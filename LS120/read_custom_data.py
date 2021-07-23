#!/usr/bin/env python3
"""
    read_custom_data.py

    This file reads custom data from youless sqlite3 database and returns it
"""
import ast  # for converting string representation of a list to a list
from datetime import datetime, timedelta
import calendar

# sqlite
import sqlite3 as sl
from sqlite3.dbapi2 import OperationalError

# Youless setup
from .constants import Settings, Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("read_custom_data.py started")


class read_custom_data:
    """
        class to read custom data from youless database.
    """
    __path = Settings.path + Settings.dbname  # path to the youless database

    def __init__(self) -> None:
        self.__db_file = read_custom_data.__path
        self.conn = None

    def db_connect(self):
        """
            function to test if database exists and then connect to it.\n
            returns None if database does not exist.
        """
        try:
            self.conn = sl.connect(f'file:{self.__db_file}?mode=ro', uri=True)  # try to open the database file in read only mode
            logger.debug("connected to %s" % self.__db_file)
            return self.conn
        except OperationalError as e:  # raise exception if file is not found
            logger.error(e)
            logger.error("file not found %s" % self.__db_file)
            return None

    def check_existence(self, **kwargs):
        """
            function to check if item exists in sqlite database.\n
            returns 1 if row exists and 0 if not.

            :table= str
            :column= str
            :item= str/int (int gets transformed to str in process)
        """
        self.conn = read_custom_data().db_connect()
        if read_custom_data().db_connect() is None:
            return 0
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
        """
            returns 1 item from database corresponding to the given query and kwargs
        """
        self.conn = read_custom_data().db_connect()
        if read_custom_data().db_connect() is None:
            return 0
        self.q = Youless.sql('queries')[kwargs.get('query')]
        self.query = self.q % tuple(kwargs.values())[1:]
        self.cur = self.conn.cursor()
        with self.conn:
            self.data = self.cur.execute(self.query)
        self.outcome = [row for row in self.data]
        self.conn.close()
        return self.outcome

    def get_yeardays(self, **kwargs):
        """
            return list of all occuring day numbers (zero padded).
                given a weekday in a date period\n
                given a date period\n

            Examples:
                get_yeardays(start=datetime(2021,1,1), end=datetime(2021,12,31), day='wednesday')\n
                get_yeardays(start=datetime(2021,3,1), end=datetime(2021,3,31))\n

            :start= datetime(year,month,day)
            :end= datetime(year,month,day)
            :day= str e.g. 'monday'
        """
        self.weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')
        self.day = kwargs.get('day') if 'day' in kwargs else None
        self.day_calc = (self.start + timedelta(days=i) for i in range((self.end - self.start).days + 1))
        yearday_list = [d for d in self.day_calc if d.weekday() in [self.weekdays.index(self.day), ]] if self.day is not None else [d for d in self.day_calc if d.weekday() in [n for n, d in enumerate(self.weekdays)]]
        return [d.date().strftime('%j') for d in yearday_list]

    def get_date_range_from_week(self, **kwargs):
        """
            source: http://mvsourcecode.com/python-how-to-get-date-range-from-week-number-mvsourcecode/

            return start and enddate fomr given weeknumber in given year.\n
            example:
                get_date_range_from_week(year=2020,week=24)

            :year= int
            :week= int
        """
        self.year = kwargs.get('year')
        self.week = kwargs.get('week')
        self.first_day = datetime.strptime(f'{self.year}-W{int(self.week)}-1', "%Y-W%W-%w")
        self.last_day = self.first_day + timedelta(days=6.9)
        return self.year, self.week, self.first_day, self.last_day

    def get_average(self, **kwargs):
        """
            return average for:
                specified weekday in a year,\n
                specified week in a year,\n
                specified month in a year,\n
                specified weekday in a month in a year.

            gets data from table dayhours_X based on yearday numbers.

            :year= int: 2021
            :day= dayname
            :month= monthname
            :etype= 'E' or 'G'
        """
        if 'year' in kwargs:  # check if year is passed as keyword argument
            self.year = kwargs.get('year')
            self.start = datetime(self.year, 1, 1)  # a full year is always from january 1st to december 31st
            self.end = datetime(self.year, 12, 31)  # a full year is always from january 1st to december 31st
        if 'year' in kwargs and 'month' in kwargs:
            self.month = kwargs.get('month')
            self.start = datetime(self.year, datetime.strptime(self.month, '%B').month, 1)  # a month always starts at day 1, it is always the same
            self.end = datetime(self.year,
                                datetime.strptime(self.month, '%B').month,
                                calendar.monthrange(self.year, datetime.strptime(self.month, '%B').month)[1])  # get last day of month from calendar
        if 'day' in kwargs:
            self.day = kwargs.get('day')
        if 'week' in kwargs:
            self.week = kwargs.get('week')
            self.start = read_custom_data().get_date_range_from_week(year=self.year, week=self.week)[2]
            self.end = read_custom_data().get_date_range_from_week(year=self.year, week=self.week)[3]
        if 'etype' in kwargs:
            self.table = Youless.sql('dbtables')[kwargs.get('etype')][1]
            self.select = Youless.sql('av_select')[kwargs.get('etype')]

        if 'day' not in kwargs:
            self.get_yeardays = read_custom_data().get_yeardays(start=self.start, end=self.end)
        else:
            self.get_yeardays = read_custom_data().get_yeardays(start=self.start, end=self.end, day=self.day)
        logger.debug("get_yeardays: %s" % self.get_yeardays)

        check_exist = [yearday.lstrip('0') for yearday in self.get_yeardays if read_custom_data().check_existence(table=self.table, column='yearday', item=yearday) == 1]
        logger.debug("exists yearday check: %s" % check_exist)
        if check_exist == []:
            return 0

        self.get_item = [[i for i in read_custom_data().get_item(query='select_one_and',
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
