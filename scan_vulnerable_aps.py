#!/usr/bin/env python

import errno
import sys
import types
from mac2defaults import default_key, default_ssid

import pythonwifi.flags
from pythonwifi.iwlibs import Wireless, Iwrange, getNICnames

def print_probable_keys(wifi):
    """ Print the probable keys
    """
    # "Check if the interface could support scanning"
    try:
        iwrange = Iwrange(wifi.ifname)
    except IOError, (error_number, error_string):
        sys.stderr.write("%-8.16s  Interface doesn't support scanning.\n\n" % (
                            wifi.ifname))
    else:
        try:
            results = wifi.scan()
        except IOError, (error_number, error_string):
            sys.stderr.write("error %i vs %i\n" % (error_number, errno.EPERM))
            if error_number == errno.EPERM
                sys.stderr.write("Permission denied. Did you run the program as root?")
            else:
                sys.stderr.write(
                    "%-8.16s  Interface doesn't support scanning : %s\n\n" %
                    (wifi.ifname, error_string))
        print("%i results" % len(results))
        for ap in results:
            print ap.mode
            if "Master" == ap.mode:
                defaultkey = default_key(ap.bssid)
                defaultessid = default_ssid(ap.bssid)
                print("- %s: try %s" % (ap.essid, defaultkey))
                if substr(ap.essid, -4) == defaultessid:
                    print "Probable key for %s: %s" % (ap.essid, defaultkey)


def main():
    # if only program name is given, print usage info
    if len(sys.argv) == 1:
        ifname = "wlan0"
    else:
        ifname = sys.argv[1]
    wifi = Wireless(ifname)
    print_probable_keys(wifi)

if __name__ == "__main__":
    main()
