
import datetime
import pytz
import tzlocal

from subprocess import call

from place import Place
from place import nkpCoord
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import AbsoluteTimepoint
from interval import SunsetTimepoint



class Lamp :
    def __init__(self, index) :
        self.index = index

    def on(self) :
        call(['tdtool', '--on', str(self.index)])

    def off(self) :
        call(['tdtool', '--off', str(self.index)])

    def update(self, time, lampscheme) :
        on = False
        for interval in lampscheme :
            if( interval.within(time) ) :
                on = True
                
        if( on ) :
            self.on()
        else :
            self.off()


def murklanScheme(place) :
    tz = tzlocal.get_localzone()
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
    

# assumes sunrise at 07:00 and sunset at 18:22
# should really have a test that is independent from which day it is run...
def test_lamp() :
    tz = tzlocal.get_localzone()
    place = Place(nkpCoord())
    place.findSunTimes()

    scheme = murklanScheme(place)
    lamp = Lamp(1)

    lamp.update(datetime.time(12, 10, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be OFF. Press enter to continue.")
    
    lamp.update(datetime.time(5, 50, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be OFF. Press enter to continue.")
    
    lamp.update(datetime.time(6, 30, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be ON. Press enter to continue.")
    
    lamp.update(datetime.time(8, 30, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be ON. Press enter to continue.")
    
    lamp.update(datetime.time(9, 10, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be OFF. Press enter to continue.")
    
    lamp.update(datetime.time(18, 40, 5, 0, tz), scheme[1])         # after sunset but within offset
    test_wait("Lamp expected to be OFF. Press enter to continue.")
    
    lamp.update(datetime.time(18, 59, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be ON. Press enter to continue.")
    
    lamp.update(datetime.time(22, 29, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be ON. Press enter to continue.")
    
    lamp.update(datetime.time(22, 30, 5, 0, tz), scheme[1])
    test_wait("Lamp expected to be OFF. Press enter to continue.")


def test_wait(s) :
    raw_input(s)
    
    
