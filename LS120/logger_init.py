#!/bin/sh
"""
    logger_init.py
    
    global logging initialization
"""
import os
path = os.path.dirname(os.path.realpath(__file__)) + '/' # path is the full path of where ever this file resides

# import modules for logging
import yaml
import logging
import logging.config
filename = 'logger_config.yaml'

# open logging config
with open(path + filename, 'r') as f:
    try:
        # load config file
        logger_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logger_config)
    except yaml.YAMLError as e:
        print("Error, could not open logger config")
        pass


