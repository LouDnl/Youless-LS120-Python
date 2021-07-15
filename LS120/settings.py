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

    language = "NL"  # or EN
    locale = "nl_NL.utf8"  # or en_US.utf8

    path = os.path.dirname(os.path.realpath(__file__)) + '/'  # path is the full path of where ever this file resides
    dbname = "youless.db"  # database name

    youless_ip = "192.168.0.40"


if __name__ == '__main__':
    sys.exit()
