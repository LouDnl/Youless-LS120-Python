#!/usr/bin/env python3
"""
    File name: test_db_retrieve_custom_data.py
    Author: LouDFPV
    Date created: 24/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file tests the LS120.db_retrieve_custom_data functions
"""
from datetime import datetime
import unittest
from LS120.db_retrieve_data import retrieve_custom_data

# initialize logging
import logging
# logger = logging.getLogger(__name__)
logger = logging.getLogger('root')  # get root logger to override settings for testing
logger.setLevel(20)  # 20 INF0 10 DEBUG (only for this file)
logger.debug("ls120_unit_test.py started")


class retrieve_custom_unittest(unittest.TestCase):
    """class to test the returns of the retrieve_custom_data methods"""

    def test_get_item(self):
        self.test_result = retrieve_custom_data().get_item(query='select_one_and',
                                                           select=('*'),
                                                           table='dayhours_e',
                                                           id='year',
                                                           item='2021',
                                                           id2='yearday',
                                                           item2='44')
        logger.info(f'get_item result1: {self.test_result}')

        #  SELECT %s FROM %s WHERE %s IS %s
        self.test_result = retrieve_custom_data().get_item(query='select_one',
                                                           select='*',
                                                           table='yeardays_e',
                                                           id='month',
                                                           item='3')
        logger.info(f'get_item result2: {self.test_result}')

        self.test_result = retrieve_custom_data().get_item(query='select_one',
                                                           select='yearday,watt',
                                                           table='dayhours_e',
                                                           id='year',
                                                           item='2021')
        logger.info(f'get_item result3: {self.test_result}')

    def test_get_yeardays(self):
        self.test_result = retrieve_custom_data().get_yeardays(start=datetime(2021, 1, 1), end=datetime(2021, 12, 31), day='wednesday')
        logger.info(f'get_yeardays result: {self.test_result}')

        self.test_result = retrieve_custom_data().get_yeardays(start=datetime(2021, 3, 1), end=datetime(2021, 3, 31))
        logger.info(f'get_yeardays result2: {self.test_result}')

    def test_exist(self):
        self.test_result = retrieve_custom_data().check_existence(table='dayhours_e', column='yearday', item=140)
        logger.info(f'existence result1: {self.test_result}')

        self.test_result = retrieve_custom_data().check_existence(table='dayhours_e', column='yearday', item='141')
        logger.info(f'existence result2: {self.test_result}')

    def test_get_date_range_from_week(self):
        self.test_result = retrieve_custom_data().get_date_range_from_week(year=2020, week=24)
        logger.info(f'week dates result: {self.test_result}')

        self.test_result = retrieve_custom_data().get_date_range_from_week(year=2021, week=1)
        logger.info(f'week dates result: {self.test_result}')

        self.test_result = retrieve_custom_data().get_date_range_from_week(year=2021, week=1)[2:]
        logger.info(f'week dates result: {self.test_result}')

    def test_get_average(self):
        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, day='friday', etype='E')
        logger.info(f'average result1: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, month='march', day='tuesday', etype='E')
        logger.info(f'average result2: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, month='february', etype='E')
        logger.info(f'average result3: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, week=6, etype='E')
        logger.info(f'average result4: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, day='friday', etype='G')
        logger.info(f'average result1: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, month='march', day='tuesday', etype='G')
        logger.info(f'average result2: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, month='june', etype='G')
        logger.info(f'average result3: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, week=8, etype='G')
        logger.info(f'average result4: {self.test_result}')

        self.test_result = retrieve_custom_data().get_dayhours_average(year=2021, week=6, etype='G')
        logger.info(f'average result4: {self.test_result}')


if __name__ == '__main__':
    unittest.main()
