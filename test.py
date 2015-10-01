import json
import urllib2

import datetime
import pytz
import tzlocal

#
# getSun
# coords: { 'lat': lat_string, 'lng' : long_string }
# returns { 'sunrise': datetime1, 'sunset': datetime2 } for given coords.
# Datetimes are 'aware' and UTC.
#
def getSun(coord) :
    response = urllib2.urlopen('http://api.sunrise-sunset.org/json?lat=' + coord['lat'] + '&lng=' + coord['lng'] + '&formatted=0')
    html = response.read()
    j = json.loads(html)
    return { 'sunrise' :  pytz.utc.localize(datetime.datetime.strptime(j['results']['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')),
             'sunset' :   pytz.utc.localize(datetime.datetime.strptime(j['results']['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')) }

def nkpCoord() :
    return { 'lat' : '58.45', 'lng' : '17.04' }

def printNkpSun() :
    sun = getSun( nkpCoord() )
    tz = tzlocal.get_localzone()
    sunrise = sun['sunrise'].astimezone(tz)
    sunset = sun['sunset'].astimezone(tz)
    print("Sunrise: " + sunrise.ctime())
    print("Sunset: " + sunset.ctime())
