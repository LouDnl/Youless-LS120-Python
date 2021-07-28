#!/usr/bin/env python3
"""
    File name: test_db_write_data.py
    Author: LouDFPV
    Date created: 26/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file tests the LS120.db_write_data functions
"""
import unittest
from LS120.db_write_data import parse_data
# from test.test_read_youless import read_youless_unittest
from .test_read_youless import read_youless_unittest

# initialize logging
import logging
# logger = logging.getLogger(__name__)
logger = logging.getLogger('root')  # get root logger to override settings for testing
logger.setLevel(20)  # 20 INF0 10 DEBUG (only for this file)
logger.debug("test_read_youless.py started")


class db_write_data_unittest(unittest.TestCase):
    """class to test the parse and write data functions"""

    def test_parsewrite_ten_minutes_E(self):
        self.test_result = parse_data().parse_tenminutes('E', read_youless_unittest().test_read_ten_minutes_E())
        logger.info(f'parse_tenminutes_E: {self.test_result}')

    def test_parsewrite_ten_minutes_G(self):
        self.test_result = parse_data().parse_tenminutes('G', read_youless_unittest().test_read_ten_minutes_G())
        logger.info(f'parse_tenminutes_G: {self.test_result}')

    def test_parsewrite_days_E(self):
        self.test_result = parse_data().parse_days('E', read_youless_unittest().test_read_days_E())
        logger.info(f'parse_days_E: {self.test_result}')

    def test_parsewrite_days_G(self):
        self.test_result = parse_data().parse_days('G', read_youless_unittest().test_read_days_G())
        logger.info(f'parse_days_G: {self.test_result}')

    def test_parsewrite_months_E(self):
        self.test_result = parse_data().parse_months('E', read_youless_unittest().test_read_months_E())
        logger.info(f'parse_months_E: {self.test_result}')

    def test_parsewrite_months_G(self):
        self.test_result = parse_data().parse_months('G', read_youless_unittest().test_read_months_G())
        logger.info(f'parse_months_G: {self.test_result}')


if __name__ == '__main__':
    unittest.main()
