#!/usr/bin/env python3
"""
    File name: settings.py
    Author: LouDFPV
    Date created: 09/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file is contains ip, device, path and language related settings.
"""
import os

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("settings.py loaded")


class Settings:
    """static language, locale, path, dbname and youless ip settings"""

    language = "NL"  # or EN
    locale = "nl_NL.utf8"  # or en_US.utf8

    path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides
    dbname = "youless.db"  # database name of file in path

    youless_ip = "192.168.0.40"  # the Youless LS120 IP address
