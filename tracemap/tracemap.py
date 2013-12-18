#!/usr/bin/env python

# This file is part of Tracemap
#
# Tracemap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tracemap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tracemap.  If not, see <http://www.gnu.org/licenses/>.


import re
import sys
from sh import traceroute
import GeoIP


def lookup(target):
    """
    Runs a traceroute and attempts to geoip lookup all of the
    intelligable stops.
    """

    cmd = traceroute(target)
    cmd.wait()
    result = "\n".join(cmd.stdout.split("\n")[1:])
    ips = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)

    db = "/usr/share/GeoIP/GeoLiteCity.dat"
    gi = GeoIP.open(db, GeoIP.GEOIP_STANDARD)
    stops = map(gi.record_by_addr, ips)

    path = []
    for stop in stops:
        city = None
        region = None
        country = None
        coord = None
        if stop:
            city = stop["city"]
            region = stop["region_name"] or stop["region"]
            country = stop["country_name"] or stop["country_code"]
            coord = (round(stop["latitude"],2), round(stop["longitude"],2))
        location = []
        for datum in [city, region, country, coord]:
            if datum and len(datum):
                location.append(datum)
        path.append(location)
    return path


def mains():
    """
    Nice command form for the lookup function.
    """
    try:
        target = sys.argv[1]
    except IndexError:
        print "Pass a url or ip address as an argument."

    print "Running traceroute, please wait..."
    route = lookup(target)

    for i, location in zip(range(len(route)), route):
        msg = " - {0}: ".format(i+1)
        if location:
            msg += " ".join(map(str, location))
        else:
            msg += "Unknown"
        print msg
