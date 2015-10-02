import datetime
import pytz
import tzlocal

from enum import Enum

class TimepointMode(Enum) :
    sunrise = 1
    sunset = 2
    absolute = 3


class SunriseTimepoint :

    # offset: datetime.timedelta
    # place: Place
    def __init__(self, offset, place) :
        self.offset = offset
        self.place = place

    # time: datetime.time
    def after(self, time) :        
        return time > (self.place.sunrise + self.offset).timetz()

    # time: datetime.time
    def before(self, time) :
        return time < (self.sunrise - self.offset).timetz()

    
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


class TimeInterval :
    def __init__(self, start, end) :
        self.start = start
        self.end = end

    def within(self, time) :
        return self.start.after(time) and self.end.before(time)



