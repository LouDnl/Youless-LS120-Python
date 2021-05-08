"""
Basic configuration holder objects.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import sys, os, datetime, time
import warnings

class Runtime:
    DEBUG = True # enable/disable debug messages
    LOG = True # enable/disable log messages

    dt = datetime.datetime.today() # get current datetime
    date_now = dt
    current_date = ("{:4d}-{:02d}-{:02d}".format(dt.year,dt.month,dt.day))
    current_time = ("{:02d}:{:02d}:{:02d}".format(dt.hour,dt.minute,dt.second))
    today = ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day))
    yesterday = ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day-1))
    day_now = date_now.day
    month_now = date_now.month
    last_month = date_now.month-1
    year_now = date_now.year #% 100 # last two digits
    last_year = date_now.year-1 # last year

class Vars:
    ## Static variables
    ip = '192.168.0.5'
    port = '8080'
    path = "./" # static path, assumes db is in same folder as script
    dbname = "youless.db"

    ## Unused variables
    months = (range(1,13,1)) # url months
    weeks = (range(1,54,1))  # url weeks
    days = (range(1,32,1))   # url days
    hours = (range(1,25,1))  # url hours
    years = (range(2020, 2031, 1)) # years
    # lowMonths = (4,6,9,11)
    # highMonths = (1,3,5,7,8,10,12)
    # excMonth = 2

    ## Configuration dictionary
    __conf = {
        "valuenaming": ('kWh', 'm3', 'watt', 'ltr'), # Tuple with fixed value naming 0, 1, 2, 3
        "energytypes": {
            "list": ("E", "G", "W"), # 0, 1, 2
            "E": "Electricity in watts or kilowatts (per hour)",
            "G": "Gas usage in liters or cubic meters",
            "W": "Water usage in liters or cubic meters"
        },
        "dbtables": { # Database table naming
            "E": ('yeardays_e', 'dayhours_e'),#, 'dayminutes_e'), # tuple 0, 1, 3
            "G": ('yeardays_g', 'dayhours_g')#, 'dayminutes_g'), # tuple 0, 1, 3
            # "S": ('yeardays_s', 'dayhours_s'), # tuple 0, 1
        },
        "queries": { # All used SQL queries
            "yeardays_e":
            """
                CREATE TABLE yeardays_e (

                    date TEXT NOT NULL PRIMARY KEY,
                    year TEXT NOT NULL,
                    month TEXT NOT NULL,
                    monthname TEXT NOT NULL,
                    kwh TEXT NOT NULL
                );
            """,
            "dayhours_e":
            """
                CREATE TABLE dayhours_e (
                    date TEXT NOT NULL PRIMARY KEY,
                    year TEXT NOT NULL,
                    week TEXT NOT NULL,
                    month TEXT NOT NULL,
                    monthname TEXT NOT NULL,
                    day TEXT NOT NULL,
                    yearday TEXT NOT NULL,
                    watt TEXT NOT NULL
                );
            """,
            "dayminutes_e":
            """
                "NON EXISTANT"
            """,
            "yeardays_g":
            """
                CREATE TABLE yeardays_g (

                    date TEXT NOT NULL PRIMARY KEY,
                    year TEXT NOT NULL,
                    month TEXT NOT NULL,
                    monthname TEXT NOT NULL,
                    m3 TEXT NOT NULL
                );
            """,
            "dayhours_g":
            """
                CREATE TABLE dayhours_g (
                    date TEXT NOT NULL PRIMARY KEY,
                    year TEXT NOT NULL,
                    week TEXT NOT NULL,
                    month TEXT NOT NULL,
                    monthname TEXT NOT NULL,
                    day TEXT NOT NULL,
                    yearday TEXT NOT NULL,
                    ltr TEXT NOT NULL
                );
            """,
            "dayminutes_g":
            """
                "NON EXISTANT"
            """,
            "i_dayhours":
            """
                INSERT OR REPLACE INTO %s (date,year,week,month,monthname,day,yearday,%s)
                VALUES(?,?,?,?,?,?,?,?)
            """,
            "i_yeardays":
            """
                INSERT OR REPLACE INTO %s (date,year,month,monthname,%s)
                VALUES(?,?,?,?,?)
            """,
            "s_table":
            """
                SELECT * FROM %s WHERE date=?
            """,
            "table_exist": # query credits: https://stackoverflow.com/posts/8827554/revisions
            """
                SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?
            """,
            "s_dayhours":
            """
                SELECT * FROM %s WHERE year = %s AND month = %s AND day = %s
            """,
            "s_yeardays":
            """
                SELECT * FROM %s WHERE year = %s AND month = %s
            """,
            "so_yeardays":
            """
                SELECT * FROM %s WHERE year = %s ORDER BY date
            """
        }
    }

    ## Youless webpage links and naming
    __web = {
        "LANG": "NL", # NL or EN only for now
        "LOCALE": "nl_NL.utf8", # Need to set this to nl_NL er en_US aswell
        "ENCODING": "utf-8",
        "HEADERS": { "Accept-Language": "en-US, en;q=0.5"},
        "URL": "http://192.168.0.40", # base url
        "ELE": "/V?", # url for electricity
        "GAS": "/W?", # url for gas
        "S0": "/Z?", # url for S0 bus
        "STATS": "/a?", # url for live statistics
        "JSON": "f=j&", # json link
        "M": "m=", # url represented in months (number) 1 to 12 and goes back 1 year, kWh for E and m3 for G
        "W": "d=", # url represented per day, history goes back 70 days, Watt for E and ltr for G
        "D": "h=", # url represented in 20 parts of half an hour with usage per minute, counting back from the current moment. Watt for E
        "H": "w=",  # url represented in 30 parts of 8 hours per part in 10 minute representations, counting back from the current moment. Watt for E and ltr for G
        "maxDayPage": 70, # max for d=
        "minDayPage": 1, # min for d=
        "maxMonthPage": 12, # max for m=
        "minMonthPage": 1, # min for m=
        "maxMinutePage": 20, # max for h=
        "minMinutePage": 1, # min for h=
        "maxHour": 24, # max hour in a day -1
        "minHour": 0, # min hour in a day
        "maxMinute": 29, # max minutes per part for h=
        "minMinute": 0, # min minutes per part for h=
    }

    ## Languages
    __langNL = {
        "livegraphtitle": "Live verbruik: {} watt, {} {}uur",
        "liveminutegraphtitle": "Live verbruik per minuut: {} watt, {} {} uur",
        "dayhourtitle": "%s %d %d %s per uur, totaal verbruik: %g %s",
        "yearmonthtitle": "%s %d %s per dag, totaal verbruik: %g %s",
        "yeardaytitle": "jaar %d %s per dag, totaal verbruik: %g %s",
        "yeartitle": "jaar %d %s per maand, totaal verbruik: %g %s",
        "D": "Dag",
        "DT": "Datum",
        "KH": "kiloWatt uur",
        "KWH": "kWh",
        "M": "maand",
        "T": "Tijd",
        "U": "Uur",
        "W": "Watt",
        "WH": "Watt uur",
        "KM": "Kubieke Meter",
        "M3": "m3",
        "L": "Liter"
    }

    __langEN = {
        "livegraphtitle": "Live usage: {} watt, {} {} hours",
        "liveminutegraphtitle": "Live usage per minute: {} watt, {} {} hour",
        "dayhourtitle": "%s %d %d %s per hour, total usage: %g %s",
        "yearmonthtitle": "%s %d %s per day, total usage: %g %s",
        "yeardaytitle": "year %d %s per day, total usage: %g %s",
        "yeartitle": "year %d %s per month, total usage: %g %s",
        "D": "Day",
        "DT": "Date",
        "KH": "kiloWatt hour",
        "KWH": "kWh",
        "M": "month",
        "T": "Time",
        "U": "Hour",
        "W": "Watts",
        "WH": "Watts hour",
        "KM": "Cubic meters",
        "M3": "m3",
        "L": "Liter"
    }

    @staticmethod
    def conf(name): # return items from config dictionary
        return Vars.__conf[name]

    @staticmethod
    def web(name): # return items from web dictionary
        return Vars.__web[name]

    @staticmethod
    def lang(text): # return items from language dictionary
        if Vars.__web["LANG"] == "NL":
            return Vars.__langNL[text]
        elif Vars.__web["LANG"] == "EN":
            return Vars.__langEN[text]

# debug messages method
def dbg(s):
    """
    Usage:
    dbg(lambda: "TEXT")
    dbg(lambda: "TEXT and %s" % variable)
    """
    if Runtime.DEBUG:
        print(s())

# log messages method
def log(s):
    """
    Usage:
    log(lambda: "TEXT")
    log(lambda: "TEXT and %s" % variable)
    """
    if Runtime.LOG:
        print(s())

# type defining
# def datatype(t):
#     types = {
#         "E": "Electricity",
#         "G": "Gas",
#         "W": "Water"
#     }
#     for k, v in types.items():
#         if t in v:
#             return(v)
