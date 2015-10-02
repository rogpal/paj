
import datetime
import pytz
import tzlocal

from subprocess import call

from place import Place
from place import nkpCoord
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import AbsoluteTimepoint



class Lamp :
    def __init__(self, index, place) :
        self.index = index
        self.place = place

    def on(self) :
        call(['tdtool', '--on', str(self.index)])

    def off(self) :
        call(['tdtool', '--off', str(self.index)])

    def update(self, time, lampscheme) :
        for interval in lampscheme :            
            if( interval.within(datetime.datetime.now(pytz.utc)) ) :
                on(self)
            else :
                off(self)



def murklanScheme()
    tz = tzlocal.get_localzone()
    place = Place(nkpCoord())
    place.findSunTimes()
    scheme = { 1 : [ TimeInterval(SunriseTimepoint(datetime.timedelta(hours = -1), place),  # on 1 hour before sunrise,
                                  AbsoluteTimepoint(datetime.time(9, 0, 0, 0, tz))),        # off at 09:00
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 30), place), # on 1/2 hour after sunset,
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ]     # off at 22:30
             }
    return scheme
                                                                                             

def test_interval() :
    tz = pytz.utc
    place = Place(nkpCoord())
    place.findSunTimes()
    interval = TimeInterval(SunriseTimepoint(datetime.timedelta(hours = 1), place),
                            AbsoluteTimepoint(datetime.time(13, 10, 5, 0, tz)))
    print str(interval.within(datetime.time(12, 10, 5, 0, tz))) + ' expected true.'
    print str(interval.within(datetime.time(13, 10, 6, 0, tz))) + ' expected false.'
    print str(interval.within(datetime.time(5, 10, 5, 0, tz))) + ' expected false.'
    print str(interval.within(datetime.time(8, 10, 5, 0, tz))) + ' expected true.'
    

