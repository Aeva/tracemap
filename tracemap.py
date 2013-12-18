#!/usr/bin/env python

import re
import sys
from sh import traceroute
import GeoIP

if __name__ == "__main__":
    target = sys.argv[1]
    db = "/usr/share/GeoIP/GeoLiteCity.dat"
    gi = GeoIP.open(db, GeoIP.GEOIP_STANDARD)
    
    print "Running traceroute, please wait..."
    cmd = traceroute(target)
    cmd.wait()
    result = "\n".join(cmd.stdout.split("\n")[1:])
    ips = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', result)
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

    for i, location in zip(range(len(path)), path):
        msg = " - {0}: ".format(i+1)
        if location:
            msg += " ".join(map(str, location))
        else:
            msg += "Unknown"
        print msg

