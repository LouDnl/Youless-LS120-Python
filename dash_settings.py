"""
    dash_settings.py

    This file is for dash related settings.
"""
import sys

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.debug("dash_settings.py loaded")


class Dash_Settings:

    DASHDEBUG = True  # enable/disable serving of dash webservices on local_ip

    local_ip = '127.0.0.1'  # static home ip for testing the webpage. default ip if DASHDEBUG == True
    external_ip = '192.168.0.5'  # external webpage ip when hosting
    port = '80'  # connection port


class ip_validation(object):
    """
    Credits: https://www.tutorialspoint.com/validate-ip-address-in-python
    """
    def valid_ip_address(self, IP):
        """
        :type IP: str
        :rtype: str
        """
        def isIPv4(s):
            try: return str(int(s)) == s and 0 <= int(s) <= 255
            except: return False

        def isIPv6(s):
            if len(s) > 4:
                return False
            try: return int(s, 16) >= 0 and s[0] != '-'
            except:
                return False
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return "IPv4"
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return "IPv6"
        return "Neither"


if __name__ == '__main__':
    sys.exit()
