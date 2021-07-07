"""
    Read live data from Youless LS120
"""

#defaults
import sys, os, datetime, re, time, sched, locale

# web connects
import requests

# graph
# import plotly.express as px

# dash webpage
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State

# json
import json

# youless specific
from globals import *
# from plotData import *
# from webElements import *
# import importData_toDB as db

# Set locale
Vars.youlessLocale()

## Data read with these methods get read live from the youless device and is not store in a database.
class readLiveData:

    def __init__(self):
        self.__headers = Vars.web("HEADERS") # acceptable html headers
        self.__url = Vars.web("URL") # base url
        self.__ele = Vars.web("ELE")
        self.__gas = Vars.web("GAS")
        self.__json = Vars.web("JSON")
        self.__month = Vars.web("M")
        self.__day = Vars.web("W")
        self.__stats = Vars.web("STATS")
        self.__D = Vars.web("D")
        self.__H = Vars.web("H")

    def readLive(self):
        """
        read live energy data from Youless 120
        returns a dictionary with data
        example return: {'cnt': ' 29098,470', 'pwr': 581, 'lvl': 0, 'dev': '', 'det': '', 'con': 'OK', 'sts': '(48)', 'cs0': ' 0,000', 'ps0': 0, 'raw': 0}
        """
        self.api = requests.get(self.__url + self.__stats + self.__json).json()
        return self.api

    def readMinutes(self):
        """
        read per minute energy data from Youless 120
        data is always 1 minute behind live
        returns a dictionary with 2 lists consisting of time values and watts values
        example return:
        {'time': ['value', 'value'], 'watts': ['value', 'value']}
        """
        self.maxPage = Vars.web("maxMinutePage")
        self.minPage = Vars.web("minMinutePage")
        self.maxMinute = Vars.web("maxMinute")
        self.minMinute = Vars.web("minMinute")
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

                dbg(lambda: 'Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            self.counter -= 1
        data['time'] = time
        data['watts'] = watts
        return data

    def readTenMinutes(self):
        """
        Import per ten minute data from Youless 120
        Not working properly yet.
        """
        self.maxPage = Vars.web("maxTenMinPage")
        self.minPage = Vars.web("minTenMinPage")
        self.maxEntry = Vars.web("maxTen")
        self.minEntry = Vars.web("minTen")
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
                dbg(lambda: 'Time: {} Usage: {} Watt'.format(self.time, self.watt))
                i += 1
            self.counter += 1
        data['time'] = time
        data['watts'] = watts
        log(lambda: data)
        return data

def main():
    log(lambda: "I do not run on my own...")

if __name__ == '__main__':
        main()        
