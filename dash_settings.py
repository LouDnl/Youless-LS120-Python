"""
    File name: dash_settings.py
    Author: LouDFPV
    Date created: 15/07/2021
    Date last modified: 28/07/2021
    Python Version: 3+
    Tested on Version: 3.9

    Description:
    This file is for dash related settings.
"""
# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("dash_settings.py loaded")

# TODO - random todo for testing

class Dash_Settings:
    """dash default debug, ip and port settings"""

    DASHDEBUG = True  # enable/disable serving of dash webservices on local_ip
    RELOADER = True  # enable/disable the use_reloader feature of dash when editing files (always True if debug is True)

    local_ip = '127.0.0.1'  # static home ip for testing the webpage. default ip if DASHDEBUG == True
    external_ip = '192.168.0.5'  # external webpage ip when hosting
    port = '80'  # connection port


class ip_validation(object):
    """class to validate if supplied IP address is a valid IP address.

    credits: https://www.tutorialspoint.com/validate-ip-address-in-python
    """
    def valid_ip_address(self, IP):
        """
        :type IP: str
        :rtype: str
        """
        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except Exception:
                return False

        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != '-'
            except Exception:
                return False
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return "IPv4"
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return "IPv6"
        return "Neither"
