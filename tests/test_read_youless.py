#!/usr/bin/env python3
"""
    File name: test_read_youless.py
    Author: LouDFPV
    Date created: 26/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file tests the LS120.read_youless functions
"""
import unittest
from LS120.read_youless import read_youless

# initialize logging
import logging
# logger = logging.getLogger(__name__)
logger = logging.getLogger('root')  # get root logger to override settings for testing
logger.setLevel(20)  # 20 INF0 10 DEBUG (only for this file)
logger.debug("test_read_youless.py started")


class read_youless_unittest(unittest.TestCase):
    """class to test the returns of the read_custom_data methods"""

    def test_read_live(self):
        self.test_result = read_youless().read_live()
        logger.info(f'read_live: {self.test_result}')

    def test_read_minutes(self):
        self.test_result = read_youless().read_minutes()
        logger.info(f'read_minutes: {self.test_result}')

    def test_read_ten_minutes_E(self):
        self.test_result = read_youless().read_ten_minutes('E')
        logger.info(f'read_ten_minutes E: {self.test_result}')
        return self.test_result

    def test_read_ten_minutes_G(self):
        self.test_result = read_youless().read_ten_minutes('G')
        logger.info(f'read_ten_minutes G: {self.test_result}')
        return self.test_result

    def test_read_days_E(self):
        self.test_result = read_youless().read_days('E')
        logger.info(f'read_days E: {self.test_result}')
        return self.test_result

    def test_read_days_G(self):
        self.test_result = read_youless().read_days('G')
        logger.info(f'read_days G: {self.test_result}')
        return self.test_result

    def test_read_months_E(self):
        self.test_result = read_youless().read_months('E')
        logger.info(f'read_months E: {self.test_result}')
        return self.test_result

    def test_read_months_G(self):
        self.test_result = read_youless().read_months('G')
        logger.info(f'read_months G: {self.test_result}')
        return self.test_result


if __name__ == '__main__':
    unittest.main()
