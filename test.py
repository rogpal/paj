import json

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
from enum import Enum

import os.path

class LampMode(Enum) :
    unknown = 1
    on = 2
    off = 3    


class Lamp :
    def __init__(self, index) :
        self.index = index
        self.mode = LampMode.unknown

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
            if self.mode != LampMode.on:
                self.mode = LampMode.on
                self.on()
        else :
            if self.mode != LampMode.off:
                self.mode = LampMode.off
                self.off()

    def serialize(self) :
        return 'lamp:' + json.dumps(self.__dict__) + '\n'

    @staticmethod
    def deserialize(s) :
        if s[:5] == 'lamp:':
            lamp = Lamp(0)
            lamp.__dict__ = json.loads(s[5:])
            return lamp
        else:
            return None


def murklanScheme(place) :
    tz = tzlocal.get_localzone()
               # TV corner
    scheme = { 1 : [ TimeInterval(SunriseTimepoint(datetime.timedelta(hours = -1), place),  # on 1 hour before sunrise,
                                  AbsoluteTimepoint(datetime.time(9, 0, 0, 0, tz))),        # off at 09:00
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 30), place), # on 1/2 hour after sunset,
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],    # off at 22:30

               # Front left
               2 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(hours = 1), place),    # on 1 hour after sunset
                     AbsoluteTimepoint(datetime.time(22, 35, 0, 0, tz))) ],                 # off at 22:35

               # Front right
               3 : [ TimeInterval(SunriseTimepoint(datetime.timedelta(hours = -1), place),     # on 1 hour before sunrise
                                  SunriseTimepoint(datetime.timedelta(minutes = 15), place)),  # off 15 minutes after sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 1), place),     # on 1 minute after sunset
                                  AbsoluteTimepoint(datetime.time(23, 0, 0, 0, tz))) ],        # off at 23:00

               # outside corner
               4 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place),
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ]
             }
    return scheme
                                                                                             

def update_lamps() :
    tz = tzlocal.get_localzone()
    place = Place(nkpCoord())
    place.findSunTimes()
    present = datetime.datetime.now().timetz()

    scheme = murklanScheme(place)

    # if there is a file, use it
    filename = 'lamp.db'
    if os.path.isfile(filename):
        lamps = []
        with open(filename, 'r') as file :
            eof = False
            while not eof:
                lamp = Lamp.deserialize(file.readline())
                if lamp is None:
                    eof = True
                else:
                    lamps.append(lamp)
    else:
        # no file, so create default list
        lamps = [ Lamp(1), Lamp(2), Lamp(3), Lamp(4) ]

    for lamp in lamps :
        lamp.update(present, scheme[lamp.index])

    # persist the updated state
    with open(filename, 'w') as file:
        for lamp in lamps:
            file.write(lamp.serialize())




def test_serialize() :
    print 'Hello'[:3]

    lamp1 = Lamp(1)
    lamp2 = Lamp(2)
    lamp1.mode = LampMode.on
    lamp2.mode = LampMode.off

    #lamps = [lamp1, lamp2]

    with open('lamps.db', 'w') as file :
        file.write(lamp1.serialize())
        file.write(lamp2.serialize())
        #json.dump(lamps, file)

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
    
    

