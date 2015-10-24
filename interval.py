import datetime
import pytz
import tzlocal

from enum import Enum

class TimepointMode(Enum) :
    sunrise = 1
    sunset = 2
    absolute = 3


class SunTimepoint :
    def __init__(self, offset, suntime) :
        self.offset = offset
        self.suntime = suntime

    # time: datetime.time
    def after(self, time) :
        return time > (self.suntime + self.offset).timetz()

    # time: datetime.time
    def before(self, time) :
        return time < (self.suntime - self.offset).timetz()


class SunriseTimepoint(SunTimepoint) :

    # offset: datetime.timedelta
    # place: Place
    def __init__(self, offset, place) :
        SunTimepoint.__init__(self, offset, place.sunrise_local)


class SunsetTimepoint(SunTimepoint) :

    # offset: datetime.timedelta
    # place: Place
    def __init__(self, offset, place) :
        SunTimepoint.__init__(self, offset, place.sunset_local)


    
class AbsoluteTimepoint :

    # time: datetime:time
    def __init__(self, time) :
        self.time = time

    # time: datetime:time
    def after(self, time) :
        return time > self.time

    # time: datetime:time
    def before(self, time) :
        return time < self.time


class DarkAndAfter:
    def __init__(self, time, place):
        self.time = time
        self.place = place

    def after(self, time):
        return time > self.time and not self.place.isSunUp()

    def before(self, time):
        return not self.after(time)


class LightOrAfter:
    def __init__(self, time, place):
        self.time = time
        self.place = place

    def after(self, time):
        return time > self.time or self.place.isSunUp()

    def before(self, time):
        return not self.after(time)


class TimeInterval :
    def __init__(self, start, end) :
        self.start = start
        self.end = end

    def within(self, time) :
        return self.start.after(time) and self.end.before(time)




