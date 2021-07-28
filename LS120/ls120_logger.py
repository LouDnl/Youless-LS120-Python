
"""
    File name: ls120_logger.py
    Author: LouDFPV
    Date created: 24/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file starts and sets logging parameters.
"""
# initialize logging
import sys
import os
import yaml
import logging
import logging.config
filename = 'ls120_logger_config.yaml'

path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides

# open logging config
with open(path + filename, 'r') as f:
    try:
        # load config file
        logger_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logger_config)
        logger = logging.getLogger(__name__)
        logger.debug("LS120 logging enabled")
    except yaml.YAMLError as e:
        print("Error, could not open logger config.\nUnable to start.")
        print(e)
        sys.exit()
