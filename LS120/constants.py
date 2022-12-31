#!/usr/bin/env python3
"""
    File name: constants.py
    Author: LouDFPV
    Date created: 11/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    Constants used by the package

    Runtime class: provides datetime
    YouLess class: provides configuration constants
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import locale
# initialize logging
import logging

# get ip, language and path settings
from LS120 import Settings

logger = logging.getLogger(__name__)
logger.debug("constants loaded")


class Runtime:
    """class to provide datetime to the package."""

    @staticmethod
    def td(request):
        dt = datetime.datetime.today()

        if (request == 'dt'):
            return dt
        elif (request == 'current_date'):
            return ("{:4d}-{:02d}-{:02d}".format(dt.year, dt.month, dt.day))
        elif (request == 'current_time'):
            return ("{:02d}:{:02d}:{:02d}".format(dt.hour, dt.minute, dt.second))
        elif (request == 'today'):
            return ("{:4d},{:02d},{:02d}".format(dt.year, dt.month, dt.day))
        elif (request == 'yesterday'):
            return ("{:4d},{:02d},{:02d}".format(dt.year, dt.month, dt.day-1))
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
            return dt.year  # last two digits == %100
        elif (request == 'last_year'):
            return dt.year-1  # last year
        elif (request == 'date_live'):
            return dt.strftime("%A %d %B %Y")
        elif (request == 'time_live'):
            return dt.strftime("%H:%M")
        elif (request == 'secs_live'):
            return dt.strftime("%H:%M:%S")
        else:
            pass


class Youless:
    """libraries and constants for the package."""

    # dictionary for temporary storage of live values
    live_dict = {
            'timelst': [],
            'wattlst': []
            }

    # Youless webpage links, locale, naming and css settings
    __web = {
        "LANG": Settings.language,  # NL or EN only for now
        "LOCALE": Settings.locale,  # Need to set this to nl_NL er en_US aswell
        "ENCODING": "utf-8",
        "HEADERS": {"Accept-Language": "en-US, en;q=0.5"},
        "URL": "http://" + Settings.youless_ip,  # base url
        "ELE": "/V?",  # url for electricity
        "GAS": "/W?",   # url for gas
        "S0": "/Z?",  # url for S0 bus
        "STATS": "/a?",  # url for live statistics
        "JSON": "f=j&",  # json link
        "M": "m=",  # url represented in months (number) 1 to 12 and goes back 1 year, kWh for E and m3 for G
        "W": "d=",  # url represented per day, history goes back 70 days, Watt for E and ltr for G
        "D": "h=",  # url represented in 20 parts of half an hour (10 hours total) with usage per minute, counting back from the current moment (last entry of page 1). Watt for E and ltr for G
        "H": "w=",  # url represented in 30 parts of 8 hours (10 days total) per part in 47 representations (10 minutes), counting back from the current moment -10mins (last entry of page 1). Watt for E and ltr for G
        "maxDayPage": 70,  # max for d=
        "minDayPage": 1,  # min for d=
        "maxMonthPage": 12,  # max for m=
        "minMonthPage": 1,  # min for m=
        "maxMinutePage": 20,  # max for h=
        "minMinutePage": 1,  # min for h=
        "max_tenminutepage": 30,  # max for w=
        "min_tenminutepage": 1,  # min for w=
        "maxHour": 24,  # max hour in a day -1
        "minHour": 0,  # min hour in a day
        "maxMinute": 29,  # max minutes per part for h=
        "minMinute": 0,  # min minutes per part for h=
        "min_ten": 0,  # min entry for w=
        "max_ten": 47,  # max entry for w=
    }

    # SQL dictionary
    __sql = {
        "valuenaming": ('kWh', 'm3', 'watt', 'ltr'),  # Tuple with fixed value naming 0, 1, 2, 3
        "energytypes": {
            "list": ("E", "G", "W"),  # 0, 1, 2
            "E": "Electricity in watts or kilowatts (per hour)",
            "G": "Gas usage in liters or cubic meters",
            "W": "Water usage in liters or cubic meters"
        },
        "dbtables": {  # Database table naming
            "E": ('yeardays_e', 'dayhours_e', 'daytenminutes_e'),  # tuple 0, 1, 2 #, 'dayminutes_e'),
            "G": ('yeardays_g', 'dayhours_g', 'daytenminutes_g')  # tuple 0, 1, 2 #, 'dayminutes_g'),
            # "S": ('yeardays_s', 'dayhours_s'),  # tuple 0, 1
        },
        "av_select": {  # select yearday watt or liter for average calculation from dayhours_X
            "E": 'yearday,watt',
            "G": 'yearday,ltr'
        },
        "queries": {  # All used SQL queries
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
            "daytenminutes_e":
            """
                CREATE TABLE daytenminutes_e (
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
            "daytenminutes_g":
            """
                CREATE TABLE daytenminutes_g (
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
            # INSERT OR IGNORE WORKS ONLY IF VALUES DO NOT GET UPDATED
            # INSERT OR REPLACE WILL OVERWRITE EXISTING VALUES
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
            "i_daytenminutes":
            """
                INSERT OR REPLACE INTO %s (date,year,week,month,monthname,day,yearday,%s)
                VALUES(?,?,?,?,?,?,?,?)
            """,
            "s_table":
            """
                SELECT * FROM %s WHERE date=?
            """,
            "table_exist":  # query credits: https://stackoverflow.com/posts/8827554/revisions
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
            """,
            "select_one":
            """
                SELECT %s FROM %s WHERE %s IS %s
            """,
            "select_one_and":
            """
                SELECT %s FROM %s WHERE %s IS %s AND %s = %s
            """,
            "if_exists":  # test reformat of query style for better reading
            """
                SELECT EXISTS(SELECT 1 FROM {} WHERE {} = {})
            """,
        }
    }

    # Languages. Tuple within a dictionary item. 0 == NL, 1 == EN
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
            "Verbruik per tien minuten: {} {}, {} {} uur",
            "Usage per ten minutes: {} {}, {} {} hour",
        ),
        "customhourtitle": (
            "%d t/m %d %s %d %s per uur, totaal verbruik: %g %s",
            "%d - %d %s %d %s per hour, total usage: %g %s",
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
        "LIVE_TEN_E":
        (
            "Live Informatie Elektriciteit per 10 Minuten ",
            "Live Electricity Information per 10 Minutes",
        ),
        "LIVE_TEN_G":
        (
            "Live Informatie Gas per 10 Minuten ",
            "Live Gas Information per 10 Minutes",
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
        "D": ("Dag", "Day",),
        "DT": ("Datum", "Date",),
        "M": ("maand", "month"),
        "T": ("Tijd", "Time"),
        "U": ("Uur", "Hour"),
        "KH": ("kiloWatt uur", "kiloWatt hour"),
        "KWH": ("kWh", "kWh"),
        "W": ("Watt", "Watts"),
        "WH": ("Watt uur", "Watts hour"),
        "KM": ("Kubieke Meter", "Cubic meters"),
        "M3": ("m3", "m3"),
        "L": ("Liter", "Liter"),
    }

    @staticmethod
    def youless_locale():
        """youless_locale() -> returns the locale setting from settings.py"""
        locale.setlocale(locale.LC_ALL, Settings.locale)

    @staticmethod
    def lang(text):
        """returns item from language dictionary.

        return value is either english or dutch based on the language setting in settings.py

        example:
            :Youless.lang("keyname") -> returns the contents of the key
        """
        if Youless.__web["LANG"] == "NL":
            return Youless.__lang[text][0]
        elif Youless.__web["LANG"] == "EN":
            return Youless.__lang[text][1]

    @staticmethod
    def sql(name):  # return items from sql dictionary
        """returns item from the sql dictionary.

        examples:
            :Youless.sql("keyname") -> returns contents of the key
            :Youless.sql("keyname")["2nd_keyname"]["etc"] -> returns nested dictionaries
        """
        return Youless.__sql[name]

    @staticmethod
    def web(name, *args):  # the else: does not really add anything only a test case for me
        """returns item from web dictionary.

        examples:
            :Youless.web("keyname") -> returns contents of the key
            :Youless.web("keyname")["second_keyname"]["etc"] -> returns contents of the key within the key
            :Youless.web("keyname", "secondkeyname") -> same as above
        """
        if (args == ()):
            return Youless.__web[name]
        else:
            return Youless.__web[name].get(args[0])  # only the first extra argument will be processed, others will be ignored
