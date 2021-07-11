"""
    settings.py

    This file is for ip, device, path and language related settings.
"""
import os
import sys

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("settings.py loaded")


class Settings:
    DASHDEBUG = True  # enable/disable serving of dash webservices on local_ip
    local_ip = '127.0.0.1'  # static home ip for testing the webpage
    external_ip = '192.168.0.5'  # external webpage ip when hosting
    port = '80'  # connection port
    # path = "./"  # static path, assumes db is in same folder as script
    # path = os.getcwd()  # path is current working directory
    path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides
    dbname = "youless.db"  # database name

    youless_ip = "192.168.0.40"
    language = "NL"  # or EN
    locale = "nl_NL.utf8"  # or en_US.utf8


if __name__ == '__main__':
    sys.exit()
