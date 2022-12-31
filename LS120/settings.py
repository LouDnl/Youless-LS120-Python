#!/usr/bin/env python3
"""
    File name: settings.py
    Author: LouDFPV
    Date created: 09/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file is contains ip, device, path and language related settings.
"""
# initialize logging
import logging
import os

logger = logging.getLogger(__name__)
logger.debug("settings.py loaded")


class Settings:
    """static language, locale, path, dbname and youless ip settings"""
    # first we check if the environment variables are set and if so use those settings
    _youless = os.environ.get('YOULESS_IP')
    _lang    = os.environ.get('YOULESS_LANG')
    _locale  = os.environ.get('YOULESS_LOCALE')
    _dbname  = os.environ.get('YOULESS_DBNAME')
    _dbpath  = os.environ.get('YOULESS_DBPATH')

    if (_youless and _lang and _locale and _dbname and _dbpath):
        language = _lang
        locale = _locale
        path = _dbpath
        dbname = _dbname
        youless_ip = _youless
    else:
        language = "NL"  # or EN
        locale = "nl_NL.utf8"  # or en_US.utf8
        # path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides
        path = os.path.dirname(".") + './'  # path is the full path of where ever the LS120 module folder resides
        dbname = "youless.db"  # database name of file in path
        youless_ip = "192.168.0.40"  # the Youless LS120 IP address
