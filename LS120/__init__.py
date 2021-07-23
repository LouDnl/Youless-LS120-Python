#!/usr/bin/env python3
# __init__.py

# import methods from all package files
# from .logger import logger
from .settings import Settings
from .constants import Runtime, Youless
from .read_data import read_data
from .read_live import read_live_data
from .read_custom_data import read_custom_data
# note: create_database and import_data are run outside of any predefined code.
# example:
# python -m LS120.create_database
# python -m LS120.import_data

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
        logger.debug("__init__.py loaded")
    except yaml.YAMLError as e:
        print("Error, could not open logger config.\nUnable to start.")
        print(e)
        sys.exit()
