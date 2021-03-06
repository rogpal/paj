
from place import Place
from scheme import Weekday

from enum import Enum
from subprocess import call
import interval
import datetime
import pytz
import tzlocal
import os.path
import json
import time

class LampMode(str, Enum) :
    unknown = "unknown"
    on = "on"
    off = "off"


class Lamp :
    def __init__(self, index, tries = 1) :
        self.index = index
        self.mode = LampMode.unknown
        self.tries = tries

    def on(self) :
        for x in range(self.tries):
            call(['/usr/local/bin/tdtool', '--on', str(self.index)])
            if x < self.tries - 1:
                time.sleep(2)

    def off(self) :
        for x in range(self.tries):
            call(['/usr/local/bin/tdtool', '--off', str(self.index)])
            if x < self.tries - 1:
                time.sleep(2)

    def update(self, time, lampscheme) :
        on = False
        for interval in lampscheme :
            if(interval.within(time) ) :
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


def update(scheme) :
    present = datetime.datetime.now().timetz()
    weekday = Weekday(datetime.datetime.today().weekday())

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
        lamps = [ Lamp(1), Lamp(2), Lamp(3), Lamp(4), Lamp(5), Lamp(6,3), Lamp(7,3), Lamp(8), Lamp(9), Lamp(10), Lamp(11), Lamp(12), Lamp(13) ]

    # select scheme based on weekday
    for weekscheme in scheme:
        if weekday in weekscheme[0]:
            dayscheme = weekscheme[1]

    for lamp in lamps :
        lamp.update(present, dayscheme[lamp.index])

    # persist the updated state
    with open(filename, 'w') as file:
        for lamp in lamps:
            file.write(lamp.serialize())
