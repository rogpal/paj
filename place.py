import json
import urllib2

import datetime
import pytz
import tzlocal

class Coord :
    def __init__(self, lat, lng):
        self.lat, self.lng = lat, lng
        

class Place :
    def __init__(self, coord) :
        self.coord = coord
        self.tz = tzlocal.get_localzone()

    # findSunTimes
    # sets internal sun times from external service
    # times will be based on todays date
    def findSunTimes(self, date = None) :
        url = 'http://api.sunrise-sunset.org/json?lat=' + \
              self.coord.lat + '&lng=' + self.coord.lng + \
              '&formatted=0'
        if not (date is None):
            url += '&date=' + date.ctime()
        response = urllib2.urlopen(url)
        html = response.read()
        j = json.loads(html)
        self.sunrise = pytz.utc.localize(datetime.datetime.strptime(j['results']['sunrise'],
                                         '%Y-%m-%dT%H:%M:%S+00:00'))
        self.sunset = pytz.utc.localize(datetime.datetime.strptime(j['results']['sunset'],
                                        '%Y-%m-%dT%H:%M:%S+00:00'))
        self.sunrise_local = self.sunrise.astimezone(self.tz)
        self.sunset_local = self.sunset.astimezone(self.tz)

    # isSunUp   
    # Returns True if according to local system time, sun is presently up
    #              at this Place. findSunTimes must have been called prior to this method.
    def isSunUp(self) :
        present = datetime.datetime.now(pytz.utc)
        return( present > self.sunrise and present < self.sunset )


def nkpCoord() :
    return Coord('58.45', '17.04')

def printNkpSun() :
    nkp = Place(nkpCoord())
    nkp.findSunTimes()
    print("Sunrise: " + nkp.sunrise_local.ctime())
    print("Sunset: " + nkp.sunset_local.ctime())


def isSunUp() :
    place = Place(nkpCoord())
    place.findSunTimes()
    return place.isSunUp()

