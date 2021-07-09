#!/bin/sh
"""
    read_live.py
    
    This file reads live data directly from a Youless LS120
"""
import sys, datetime

# web
import requests

# Youless setup
from LS120.settings import Youless

# set language
Youless.youless_locale()

# initialize logging
import logging
import LS120.logger_init
logger = logging.getLogger(__name__)
logger.debug("read_live.py started")

## Data read with these methods get read live from the youless device and is not store in a database.
class read_live_data:

    def __init__(self):
        self.__headers = Youless.web("HEADERS") # acceptable html headers
        self.__url = Youless.web("URL") # base url
        self.__ele = Youless.web("ELE")
        self.__gas = Youless.web("GAS")
        self.__json = Youless.web("JSON")
        self.__month = Youless.web("M")
        self.__day = Youless.web("W")
        self.__stats = Youless.web("STATS")
        self.__D = Youless.web("D")
        self.__H = Youless.web("H")

    def read_live(self):
        """
        read live energy data from Youless 120
        returns a dictionary with data
        example return: {'cnt': ' 29098,470', 'pwr': 581, 'lvl': 0, 'dev': '', 'det': '', 'con': 'OK', 'sts': '(48)', 'cs0': ' 0,000', 'ps0': 0, 'raw': 0}
        """
        self.api = requests.get(self.__url + self.__stats + self.__json).json()
        return self.api

    def read_minutes(self):
        """
        read per minute energy data from Youless 120
        data is always 1 minute behind live
        returns a dictionary with 2 lists consisting of time values and watts values
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
                self.time = '%02d:%02d' % (h,m)# str(self.date.time())[0:5]
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

    def read_ten_minutes(self):
        """
        Import per ten minute data from Youless 120
        Not working properly yet.
        """
        self.maxPage = Youless.web("maxTenMinPage")
        self.minPage = Youless.web("minTenMinPage")
        self.maxEntry = Youless.web("maxTen")
        self.minEntry = Youless.web("minTen")
        self.counter = self.minPage
        data = {}
        time = []
        watts = []
    
        while (self.counter <= self.maxPage):
            self.api = requests.get(self.__url + self.__ele + self.__json + self.__H + str(self.counter)).json()
            self.date = datetime.datetime.strptime(self.api['tm'], '%Y-%m-%dT%H:%M:%S')
            i = self.minEntry
            while (i <= self.maxEntry):
                h = self.date.hour
                m = self.date.minute + (10 * i)
                if (m == 60):
                    h += 1
                    m = 0
                self.time = '%02d:%02d' % (h,m)# str(self.date.time())[0:5]
                self.watt = int(self.api['val'][i])
                time.append(self.time)
                watts.append(self.watt)
                logger.debug('Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            self.counter += 1
        data['time'] = time
        data['watts'] = watts
        logger.debug(data)
        return data

if __name__ == '__main__':
    sys.exit()