#!/bin/sh
"""
    settings.py
    
    Settings class: network, path and database name setttings
    Runtime class: datetime and debug settings
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import sys, os, datetime, locale

# initialize logging
import logging
import LS120.logger_init
logger = logging.getLogger(__name__)
logger.debug("settings.py loaded")

class Settings:
    ## Static variables
    local_ip = '127.0.0.1' # static home ip for testing the webpage
    external_ip = '192.168.0.5' # external webpage ip when hosting
    port = '80' # connection port
    # path = "./" # static path, assumes db is in same folder as script
    # path = os.getcwd() # path is current working directory
    path = os.path.dirname(os.path.realpath(__file__)) + '/' # path is the full path of where ever this file resides
    dbname = "youless.db" # database name
    
    youless_ip = "192.168.0.40"
    language = "NL" # or EN
    locale = "nl_NL.utf8" # or en_US.utf8

class Runtime:
    DASHDEBUG = True # enable/disable local serving of dash webservices

    @staticmethod
    def td(request):
        dt = datetime.datetime.today()

        if (request == 'dt'):
            return dt
        elif (request == 'current_date'):
            return ("{:4d}-{:02d}-{:02d}".format(dt.year,dt.month,dt.day))
        elif (request == 'current_time'):
            return ("{:02d}:{:02d}:{:02d}".format(dt.hour,dt.minute,dt.second))
        elif (request == 'today'):
            return ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day))
        elif (request == 'yesterday'):
            return ("{:4d},{:02d},{:02d}".format(dt.year,dt.month,dt.day-1))
        elif (request == 'seconds'):
            return dt.second
        elif (request == 'day_now'):
            return dt.day
        elif (request == 'day_yesterday'):
            return dt.day-1
        elif (request == 'month_now'):
            return dt.month
        elif (request == 'last_month'):
            return dt.month-1
        elif (request == 'year_now'):
            return dt.year #% 100 # last two digits
        elif (request == 'last_year'):
            return dt.year-1 # last year
        elif (request == 'date_live'):
            return dt.strftime("%A %d %B %Y")
        elif (request == 'time_live'):
            return dt.strftime("%H:%M")
        elif (request == 'secs_live'):
            return dt.strftime("%H:%M:%S")        
        else:
            pass

class Youless:

    live_dict = {'timelst': [], 'wattlst': []} # dictionary for temporary storage of live values

    ## Youless webpage links, locale, naming and css settings
    __web = {
        "LANG": Settings.language, # NL or EN only for now
        "LOCALE": Settings.locale, # Need to set this to nl_NL er en_US aswell
        "ENCODING": "utf-8",
        "HEADERS": { "Accept-Language": "en-US, en;q=0.5"},
        "URL": "http://" + Settings.youless_ip, # base url
        "ELE": "/V?", # url for electricity
        "GAS": "/W?", # url for gas
        "S0": "/Z?", # url for S0 bus
        "STATS": "/a?", # url for live statistics
        "JSON": "f=j&", # json link
        "M": "m=", # url represented in months (number) 1 to 12 and goes back 1 year, kWh for E and m3 for G
        "W": "d=", # url represented per day, history goes back 70 days, Watt for E and ltr for G
        "D": "h=", # url represented in 20 parts of half an hour (10 hours total) with usage per minute, counting back from the current moment (last entry of page 1). Watt for E
        "H": "w=",  # url represented in 30 parts of 8 hours (10 days total) per part in 47 representations (10 minutes), counting back from the current moment -10mins (last entry of page 1). Watt for E and ltr for G
        "maxDayPage": 70, # max for d=
        "minDayPage": 1, # min for d=
        "maxMonthPage": 12, # max for m=
        "minMonthPage": 1, # min for m=
        "maxMinutePage": 20, # max for h=
        "minMinutePage": 1, # min for h=
        "maxTenMinPage": 30, # max for w=
        "minTenMinPage": 1, # min for w=
        "maxHour": 24, # max hour in a day -1
        "minHour": 0, # min hour in a day
        "maxMinute": 29, # max minutes per part for h=
        "minMinute": 0, # min minutes per part for h=
        "minTen": 0, # min entry for w=
        "maxTen": 47, # max entry for w=
        "css": {
            "page_css": {'position': 'fixed', 'top': '0', 'left': '0', 'right': '0', 'bottom': '0', 'overflow': 'auto', 'width': '100%', 'height': '100%'},
            "row_title": {'text-align':'center', 'font-size': 'x-large', 'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'},
            "subrow_title": {'text-align':'center', 'font-size': 'large', 'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'},
            "table_css": {'margin': '0px', 'padding': '0px'},
            "column_css": {'border': 'none', 'border-collapse': 'collapse', 'margin': '0px', 'padding': '0px'}
        }
    }

    ## Languages. Tuple within a dictionary item. 0 == NL, 1 == EN
    __lang = {
        "livegraphtitle": 
        (
            "Live verbruik: {} watt, {} {}uur<br>Meterstand: {} {}",
            "Live usage: {} watt, {} {} hours<br>Meter: {} {}",
        ),
        "liveminutegraphtitle": 
        (
            "Live verbruik per minuut: {} watt, {} {} uur",
            "Live usage per minute: {} watt, {} {} hour",
        ),
        "tenminutegraphtitle": 
        (
            "Verbruik per tien minuten:",
            "Usage per ten minutes:",
        ),
        "customhourtitle": (
            "%s %d t/m %d %d %s per uur, totaal verbruik: %g %s",
            "%s %d - %d %d %s per hour, total usage: %g %s",
        ),
        "dayhourtitle": 
        (
            "%s %d %d %s per uur, totaal verbruik: %g %s",
            "%s %d %d %s per hour, total usage: %g %s",
        ),
        "yearmonthtitle": 
        (
            "%s %d %s per dag, totaal verbruik: %g %s",
            "%s %d %s per day, total usage: %g %s",
        ),
        "yeardaytitle": 
        (
            "jaar %d %s per dag, totaal verbruik: %g %s",
            "year %d %s per day, total usage: %g %s",
        ),
        "yeartitle": 
        (
            "jaar %d %s per maand, totaal verbruik: %g %s",
            "year %d %s per month, total usage: %g %s",
        ),
        "ELE": 
        (
            "Elektriciteit verbruik",
            "Electricity usage",
        ),
        "GAS": 
        (
            "Gas verbruik",
            "Gas usage",
        ),
        "LIVE": 
        (
            "Live Informatie Elektriciteit",
            "Live Electricity Information",
        ),
        "TOYE": 
        (
            "Vandaag en gisteren",
            "Today and yesterday",
        ),
        "CMLM": 
        (
            "Deze maand en vorige maand",
            "This month and last month",
        ),
        "TYLYM": 
        (
            "Dit jaar en vorig jaar in maanden",
            "This year and last year in months",
        ),
        "TYLYD": 
        (
            "Dit jaar en vorig jaar in dagen",
            "This year and last year in days",
        ),
        "TOD": ("Vandaag", "Today"),
        "YDY": ("Gisteren", "Yesterday"),
        "TMO": ("Deze maand", "This month"),
        "LMO": ("Vorige maand", "Last month"),
        "TYE": ("Dit jaar", "This year"),
        "LYE": ("Vorig jaar", "Last year"),
        "D": ("Dag","Day",),
        "DT": ("Datum","Date",),
        "M": ("maand","month"),
        "T": ("Tijd","Time"),
        "U": ("Uur","Hour"),
        "KH": ("kiloWatt uur","kiloWatt hour"),
        "KWH": ("kWh","kWh"),
        "W": ("Watt","Watts"),
        "WH": ("Watt uur","Watts hour"),
        "KM": ("Kubieke Meter","Cubic meters"),
        "M3": ("m3","m3"),
        "L": ("Liter","Liter"),
    }

    ## SQL dictionary
    __sql = {
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
            "s_dayhours2":
            """
                SELECT * FROM %s WHERE year = %s AND month = %s AND day IN (%s, %s)
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
 
    @staticmethod
    def youless_locale():
        """
            returns the locale setting
        """
        locale.setlocale(locale.LC_ALL, Youless.web("LOCALE"))
    
    @staticmethod
    def lang(text):
        """
            returns item from language dictionary
            usage:
            Youless.lang("keyname") returns the contents of the key
            return value is either english or dutch based on the setting in the __web dictionary under LANG.
        """
        if Youless.__web["LANG"] == "NL":
            return Youless.__lang[text][0]
        elif Youless.__web["LANG"] == "EN":
            return Youless.__lang[text][1]   

    @staticmethod
    def sql(name): # return items from config dictionary
        """
            returns item from the conf dictionary
            usage:
            Youless.conf("keyname") returns contents of the key
            For nested dictionaries use as followed:
            Youless.conf("keyname")["2nd_keyname"]["etc"]
        """
        return Youless.__sql[name]

    @staticmethod
    def web(name, *args): 
        """
            returns item from web dictionary, add second argument to return dictionary from key
            can be used either as Youless.web("keyname") and return its contents
            or as Youless.web("keyname", "secondkeyname") and returns the dictionary within the dictionary
            This will also work: Youless.web("keyname")["second_keyname"]["etc"]        
        """        
        if (args == ()):
            return Youless.__web[name]
        else:
            return Youless.__web[name].get(args[0]) # only the first extra argument will be processed, others will be ignored

if __name__ == '__main__':
        sys.exit()