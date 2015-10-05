
import datetime
import pytz
import tzlocal

from lamp import Lamp
from lamp import LampMode
from place import Place
from place import nkpCoord
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import AbsoluteTimepoint
from interval import SunsetTimepoint

from scheme import murklanScheme
                                                                                             

def test_serialize() :
    lamp1 = Lamp(1)
    lamp2 = Lamp(2)
    lamp1.mode = LampMode.on
    lamp2.mode = LampMode.off

    with open('lamps.db', 'w') as file :
        file.write(lamp1.serialize())
        file.write(lamp2.serialize())

    lamps = []
    with open('lamps.db', 'r') as file :
        eof = False
        while not eof:
            lamp = Lamp.deserialize(file.readline())
            if lamp is None:
                eof = True
            else:
                lamps.append(lamp)

    lamp1b = lamps[0]
    lamp2b = lamps[1]

    print str(lamp1b.mode) + " supposed to be on."
    print str(lamp2b.mode) + " supposed to be off."



def test_interval() :
    tz = tzlocal.get_localzone()
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
    
    

