#!/usr/bin/env python3
"""
    File name: db_auto_import.py
    Author: LouDFPV
    Date created: 9/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file automatically reads all data from the youless and stores them in the database
"""
import sys
from LS120 import Youless, db_connect, read_youless, parse_data

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("db_auto_import.py started")


def main():
    """LS120.db_auto_import -> imports year, month, day, hour and ten minute data into database"""
    try:
        conn = db_connect().connect_and_return_readwrite()
        conn.close()
    except Exception as e:
        logger.error(f"{e}, connection not possible")
        sys.exit(1)  # exiting with a non zero value is better for returning from an error
    else:
        for type in Youless.sql("dbtables").keys():
            parse_data().parse_tenminutes(type, read_youless().read_ten_minutes(type))
            parse_data().parse_days(type, read_youless().read_days(type))
            parse_data().parse_months(type, read_youless().read_months(type))


if __name__ == '__main__':
    main()
