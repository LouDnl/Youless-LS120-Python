#!/usr/bin/env python3
"""
    File name: read_youless.py
    Author: LouDFPV
    Date created: 9/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file reads data from the youless returns it as a list
"""
import sys
import datetime

# web
import requests

# Youless setup
from LS120 import Youless

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("read_youless.py started")

sys.stdin.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding
sys.stdout.reconfigure(encoding=Youless.web("ENCODING"))  # set encoding


class read_youless:
    """class to read data from the Youless LS120"""

    def __init__(self) -> None:
        self.__headers = Youless.web("HEADERS")  # acceptable html headers
        self.__url = Youless.web("URL")  # base url
        self.__ele = Youless.web("ELE")
        self.__gas = Youless.web("GAS")
        self.__snul = Youless.web("S0")
        self.__json = Youless.web("JSON")
        self.__month = Youless.web("M")
        self.__day = Youless.web("W")
        self.__stats = Youless.web("STATS")
        self.__D = Youless.web("D")
        self.__H = Youless.web("H")
        self.__kwh = Youless.sql("valuenaming")[0]
        self.__m3 = Youless.sql("valuenaming")[1]
        self.__watt = Youless.sql("valuenaming")[2]
        self.__ltr = Youless.sql("valuenaming")[3]

    def read_live(self):
        """read live energy data from Youless 120, only works with electricity.
        returns a json dictionary with data.

        example return:
            {'cnt': ' 29098,470', 'pwr': 581, 'lvl': 0, 'dev': '', 'det': '', 'con': 'OK', 'sts': '(48)', 'cs0': ' 0,000', 'ps0': 0, 'raw': 0}
        """
        self.api = requests.get(self.__url + self.__stats + self.__json).json()
        return self.api

    def read_minutes(self):
        """read per minute energy data from Youless 120, data is always 1 minute behind live.
        returns a dictionary with 2 lists consisting of time values and watts values.

        example return:
            {'time': ['value', 'value'], 'watts': ['value', 'value']}
        """
        self.maxPage = Youless.web("maxMinutePage")
        self.minPage = Youless.web("minMinutePage")
        self.maxMinute = Youless.web("maxMinute")
        self.minMinute = Youless.web("minMinute")
        self.counter = self.maxPage
        data = {}
        time = []
        watts = []

        while (self.counter >= self.minPage):
            self.api = requests.get(self.__url + self.__ele + self.__json + self.__D + str(self.counter)).json()
            self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%m-%dT%H:%M:%S')
            i = self.minMinute
            while (i <= self.maxMinute):
                h = self.date.hour
                m = self.date.minute + i
                if (m >= 60):
                    m -= 60
                    h += 1
                self.time = '%02d:%02d' % (h, m)  # str(self.date.time())[0:5]
                self.watt = int(self.api['val'][i])
                time.append(self.time)
                watts.append(self.watt)

                logger.debug('Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            self.counter -= 1
        data['time'] = time
        data['watts'] = watts
        logger.debug(data)
        return data

    def read_ten_minutes(self, etype):
        """Read per ten minute data from Youless 120.
        Returned data is always 10 minutes behind last occuring rounded 10 minute interval.
            e.g. at 18.58hours the newest entry is 18.40hours and at 19.00hours it will be 18.50hours
        Returns dictionary with date as key containing a lists with time:value key/value dictionaries\n

        example:
            read_ten_minutes(etype)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        """
        self.__urltype = self.__ele if etype == 'E' and etype != ('G', 'S') else self.__gas if etype == 'G' else self.__snul
        self.max_page = Youless.web("max_tenminutepage")
        self.min_page = Youless.web("min_tenminutepage")
        self.max_ten = Youless.web("max_ten")
        self.min_ten = Youless.web("min_ten")
        self.counter = self.min_page
        self.period = 10  # 10 minute steps
        data = {}

        while (self.counter <= self.max_page):
            self.api = requests.get(self.__url + self.__urltype + self.__json + self.__H + str(self.counter)).json()
            self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%m-%dT%H:%M:%S')
            hour = self.date.hour
            minute = self.date.minute - 10  # current time is 10 minutes less then json start time. subtract 10 minutes from json start time
            year = self.date.date().strftime('%Y')
            week_no = self.date.date().strftime('%W')
            month_no = self.date.date().strftime('%m')
            month_name = self.date.date().strftime('%B')
            month_day = self.date.date().strftime('%d')
            year_day = self.date.date().strftime('%j')
            if self.date.date().strftime('%Y-%m-%d') not in data.keys():
                data[self.date.date().strftime('%Y-%m-%d')] = []
                data[self.date.date().strftime('%Y-%m-%d')].insert(0, (year, week_no, month_no, month_name, month_day, year_day))
                data[self.date.date().strftime('%Y-%m-%d')].insert(1, [])
            i = self.min_ten
            while (i <= self.max_ten):
                minute += self.period
                if minute >= 60:
                    minute = 0
                    hour += 1
                if hour >= 24:
                    hour = 0
                    self.date += datetime.timedelta(days=1)
                self.time = '%02d:%02d' % (hour, minute)  # str(self.date.time())[0:5]
                self.value = int(self.api['val'][i])
                logger.debug('Time: {} Usage: {} {}'.format(self.time, self.value, etype))
                data[self.date.date().strftime('%Y-%m-%d')][1].insert(0, {self.time: self.value})
                i += 1
            self.counter += 1

        for key in data.keys():  # for date in dictionary
            sorted_values = sorted(data[key][1], key=lambda d: list(d.keys()), reverse=True)  # order the list hour/value dictionaries in reverse
            data[key][1] = sorted_values  # write the sorted list over the original list

        logger.debug(data)
        return data

    def read_days(self, etype):
        """read all Electricity or Gas hour values from Youless 120 with a maximum history of 70 days back (youless max).
        returns a list with tuples of data.

        example:
            read_days(etype)

        args:
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
            self.api = requests.get(self.__url + self.__urltype + self.__json + self.__day + str(self.counter))
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

    def read_months(self, etype):
        """Function to retrieve days per month from Youless 120 up to 11 months back for Electricity and Gas.
        returns a list with tuples of data.

        eaxmple:
            read_months(etype)

        args:
        :etype is 'E' or 'G' for Electricity or Gas
        """

        self.__urltype = self.__ele if etype == 'E' and etype != ('G', 'S') else self.__gas if etype == 'G' else self.__snul
        self.__type = self.__kwh if etype == 'E' and etype != 'G' else self.__m3
        self.max_page = Youless.web("maxMonthPage")
        self.min_page = Youless.web("minMonthPage")
        self.counter = self.max_page
        self.return_list = []
        while (self.counter >= self.min_page):
            self.api = requests.get(self.__url + self.__urltype + self.__json + self.__month + str(self.counter))
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
