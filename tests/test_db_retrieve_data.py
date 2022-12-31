#!/usr/bin/env python3
"""
    File name: test_db_retrieve_data.py
    Author: LouDFPV
    Date created: 25/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file tests the LS120.retrieve_dbdata functions
"""
# initialize logging
import logging
import unittest

from LS120.db_retrieve_data import retrieve_data

# logger = logging.getLogger(__name__)
logger = logging.getLogger('root')  # get root logger to override settings for testing
logger.setLevel(20)  # 20 INF0 10 DEBUG (only for this file)
logger.debug("test_retrieve_dbdata.py started")


class retrieve_data_unittest(unittest.TestCase):
    """class to test the returns of the retrieve_data methods"""

    def test_retrieve_hours(self):
        self.test_result = retrieve_data().retrieve_hours('dayhours_g', 2021, 5, 2, 3, 3, 6)
        logger.info(f'dayhours_g, 6 args: {self.test_result}')

        self.test_result = retrieve_data().retrieve_hours('dayhours_e', 2021, 3, 1, 12)
        logger.info(f'dayhours_e, 4 args: {self.test_result}')

        self.test_result = retrieve_data().retrieve_hours('dayhours_e', 2021, 6, 2, 11, 18)
        logger.info(f'dayhours_e, 5 args: {self.test_result}')

    def test_retrieve_day(self):
        self.test_result = retrieve_data().retrieve_day(2021, 5, 19, 'dayhours_e')
        logger.info(f'dayhours_e, 2021, 1, 19: {self.test_result}')

        self.test_result = retrieve_data().retrieve_day(2021, 6, 25, 'dayhours_g')
        logger.info(f'dayhours_e, 2021, 1, 19: {self.test_result}')

    def test_retrieve_month(self):
        self.test_result = retrieve_data().retrieve_month(2021, 5, 'yeardays_g')
        logger.info(f'yeardays_g, 2021, 5: {self.test_result}')

        self.test_result = retrieve_data().retrieve_month(2021, 3, 'yeardays_e')
        logger.info(f'yeardays_e, 2021, 3: {self.test_result}')

    def test_retrieve_year(self):
        self.test_result = retrieve_data().retrieve_year(2021, 2, 'yeardays_g')
        logger.info(f'yeardays_g, 2021, 2: {self.test_result}')

        self.test_result = retrieve_data().retrieve_year(2021, 1, 'yeardays_e')
        logger.info(f'yeardays_e, 2021, 1: {self.test_result}')


if __name__ == '__main__':
    unittest.main()
