import json
import requests

import datetime
import pytz
import tzlocal
import os.path

class Coord :
    def __init__(self, lat, lng):
        self.lat, self.lng = lat, lng
        

class Place :
    def __init__(self, coord) :
        self.coord = coord
        self.tz = tzlocal.get_localzone()

    # updateSunTimes
    # sets internal sun times
    # times will be based on todays date
    def updateSunTimes(self, date = None) :
        
        filename = 'suntimes.cache'
        if os.path.isfile(filename) :
            with open(filename, 'r') as file :
                timeTuple = Place.deserializeSunTimes(file.readline())
        else :
            timeTuple = Place.fetchSunTimes(self.coord, date)

        today = datetime.datetime.now(pytz.utc).date() if (date is None) else date.date()
        sunTimes = (timeTuple[1], timeTuple[2]) if today == timeTuple[0] else Place.fetchSunTimes(self.coord, date)
        self.sunrise = sunTimes[0]
        self.sunset = sunTimes[1]
        self.sunrise_local = self.sunrise.astimezone(self.tz)
        self.sunset_local = self.sunset.astimezone(self.tz)

        with open(filename, 'w') as file :
            file.write(Place.serializeSunTimes(sunTimes, date))
        
    # fetchSunTimes
    # fetch sunrise and sunset from service and return
    @staticmethod
    def fetchSunTimes(coord, date = None) :
        print("Fetching")
        
        url = 'https://api.sunrise-sunset.org/json?lat=' + \
              coord.lat + '&lng=' + coord.lng + \
              '&formatted=0'
        if not (date is None):
            url += '&date=' + date.ctime()

        response = requests.get(url)
        html = response.text
        j = json.loads(html)
        return (pytz.utc.localize(datetime.datetime.strptime(j['results']['sunrise'],
                                                             '%Y-%m-%dT%H:%M:%S+00:00')),
                pytz.utc.localize(datetime.datetime.strptime(j['results']['sunset'],
                                                             '%Y-%m-%dT%H:%M:%S+00:00')))
    
    @staticmethod
    def serializeSunTimes(sunTimes, date = None) :
        usedDate = datetime.datetime.now(pytz.utc) if (date is None) else date
        return usedDate.date().ctime() + "," + sunTimes[0].ctime() + "," + sunTimes[1].ctime()
        

    @staticmethod
    def deserializeSunTimes(str) :
        timeList = str.split(",")
        return (datetime.datetime.strptime(timeList[0], Place.getTimeFormat()).date(),
                pytz.utc.localize(datetime.datetime.strptime(timeList[1], Place.getTimeFormat())),
                pytz.utc.localize(datetime.datetime.strptime(timeList[2], Place.getTimeFormat())))

    @staticmethod
    def getTimeFormat() :
        return "%a %b %d %H:%M:%S %Y"
    
    
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
    nkp.updateSunTimes()
    print("Sunrise: " + nkp.sunrise_local.ctime())
    print("Sunset: " + nkp.sunset_local.ctime())

def printSerializedTime() :
    times = Place.fetchSunTimes(nkpCoord())
    print(Place.deserializeSunTimes(Place.serializeSunTimes(times)))

def isSunUp() :
    place = Place(nkpCoord())
    place.findSunTimes()
    return place.isSunUp()

