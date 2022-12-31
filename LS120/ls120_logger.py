
"""
    File name: ls120_logger.py
    Author: LouDFPV
    Date created: 24/07/2021
    Python Version: 3+
    Tested on Version: 3.10

    Description:
    This file starts and sets logging parameters.
"""
# initialize logging

import logging
import logging.config
import os
import sys

import yaml

# from LS120 import Settings

filename = 'ls120_logger_config.yaml'
path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides
logfilepath = os.path.dirname(".") + './'  # path is the full path of where ever the LS120 module folder resides


# open logging config
with open(path + filename, 'r') as f:
    try:
        # load logpath from environment
        logpath = os.environ.get('YOULESS_LOGPATH')
        if not (logpath):
            logpath = logfilepath  # if not present set a default logpath

        # load config file
        logger_config = yaml.safe_load(f.read())
        # update path variable in yaml with logpath (credits: https://stackoverflow.com/questions/32145688/using-program-variables-in-python-logging-configuration-file)
        logger_config["handlers"]["debug_file_handler"]["filename"] = logger_config["handlers"]["debug_file_handler"]["filename"].format(path = logpath)
        logging.config.dictConfig(logger_config)
        logger = logging.getLogger(__name__)
        logger.debug("LS120 logging enabled")
    except yaml.YAMLError as e:
        print("Error, could not open logger config.\nUnable to start.")
        print(e)
        sys.exit()
