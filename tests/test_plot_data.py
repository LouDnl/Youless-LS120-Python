#!/usr/bin/env python3
"""
    File name: test_plot_data.py
    Author: LouDFPV
    Date created: 26/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file tests the LS120.plot_data functions
"""
import datetime
# initialize logging
import logging
import unittest

from LS120.plotly_graphs.plot_data import plot_dbdata, plot_live

# logger = logging.getLogger(__name__)
logger = logging.getLogger('root')  # get root logger to override settings for testing
logger.setLevel(20)  # 20 INF0 10 DEBUG (only for this file)
logger.debug("plot_data_youless.py started")


class plot_dbdata_unittest(unittest.TestCase):
    """class to test the returns of the plot_dbdata methods"""

    def test_plot_hours(self):
        self.test_result = plot_dbdata().plot_hours("E", 2021, 3, 2, 12, 3, 11)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12, 3, 11): {self.test_result}')

        self.test_result = plot_dbdata().plot_hours("E", 2021, 3, 2, 12, 11)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12, 11): {self.test_result}')

        self.test_result = plot_dbdata().plot_hours("E", 2021, 3, 2, 12)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12): {self.test_result}')

        self.test_result = plot_dbdata().plot_hours("G", 2021, 5, 2, 12, 3, 11)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12, 3, 11): {self.test_result}')

        self.test_result = plot_dbdata().plot_hours("G", 2021, 5, 2, 12, 11)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12, 11): {self.test_result}')

        self.test_result = plot_dbdata().plot_hours("G", 2021, 5, 2, 12)
        logger.info(f'plot_hours("E", 2021, 3, 2, 12): {self.test_result}')

    def test_plot_day_hour(self):
        self.test_result = plot_dbdata().plot_day_hour(2021, 3, 19, 'E')
        logger.info(f"plot_day_hour(2021, 3, 19, 'E'): {self.test_result}")

        self.test_result = plot_dbdata().plot_day_hour(2021, 3, 26, 'G')
        logger.info(f"plot_day_hour(2021, 3, 26, 'G'): {self.test_result}")

    def test_plot_month_day(self):
        self.test_result = plot_dbdata().plot_month_day(2021, 3, 'E')
        logger.info(f"plot_month_day(2021, 3, 'E')): {self.test_result}")

        self.test_result = plot_dbdata().plot_month_day(2021, 'April', 'G')
        logger.info(f"plot_month_day(2021, 'April', 'G'): {self.test_result}")

    def test_plot_year_day(self):
        self.test_result = plot_dbdata().plot_year_day(2020, 'E')
        logger.info(f'plot_year_day(2020, "E"): {self.test_result}')

        self.test_result = plot_dbdata().plot_year_day(2021, 'G')
        logger.info(f'plot_year_day(2021, "G"): {self.test_result}')

    def test_plot_year_month(self):
        self.test_result = plot_dbdata().plot_year_month(2020, 'E')
        logger.info(f'plot_year_month(2020, "E"): {self.test_result}')

        self.test_result = plot_dbdata().plot_year_month(2021, 'G')
        logger.info(f'plot_year_month(2021, "G"): {self.test_result}')


class plot_live_unittest(unittest.TestCase):
    """class to test the returns of the plot_live methods"""

    def test_plot_live(self):
        self.test_result = plot_live().plot_live()
        logger.info(f'plot_live: {self.test_result}')

    def test_plot_live_minutes(self):
        self.test_result = plot_live().plot_live_minutes()
        logger.info(f'plot_live_minutes: {self.test_result}')

    def test_plot_live_ten_minutes_E(self):
        self.test_result = plot_live().plot_live_ten_minutes(etype='E')
        logger.info(f'plot_live_ten_minutes_E type: {type(self.test_result)}')
        logger.info(f'plot_live_ten_minutes_E: {self.test_result}')

    def test_plot_live_ten_minutes_G(self):
        d_obj = datetime.datetime(2021, 7, 20)  # fixed history start date
        self.test_result = plot_live().plot_live_ten_minutes(etype='G', start=d_obj)
        logger.info(f'plot_live_ten_minutes_G type: {type(self.test_result)}')
        logger.info(f'plot_live_ten_minutes_G: {self.test_result}')

        d_obj = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=2)  # 2 days back from today
        self.test_result = plot_live().plot_live_ten_minutes(etype='G', start=d_obj)
        logger.info(f'plot_live_ten_minutes_G type: {type(self.test_result)}')
        logger.info(f'plot_live_ten_minutes_G: {self.test_result}')

        self.test_result = plot_live().plot_live_ten_minutes(etype='G', start=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=4))  # 4 days back from today
        logger.info(f'plot_live_ten_minutes_G type: {type(self.test_result)}')
        logger.info(f'plot_live_ten_minutes_G: {self.test_result}')


if __name__ == '__main__':
    unittest.main()
