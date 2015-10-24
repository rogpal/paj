
import pytz
import datetime
import tzlocal
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import SunsetTimepoint
from interval import AbsoluteTimepoint
from interval import DarkAndAfter
from interval import LightOrAfter

def murklanScheme(place) :
    tz = tzlocal.get_localzone()
               # TV corner
    scheme = { 1 : [ TimeInterval(DarkAndAfter(datetime.time(6, 15, 0, 0, tz), place),      # on at 6.15 and if it is dark,
                                  AbsoluteTimepoint(datetime.time(7, 30, 0, 0, tz))),       # off at 07:30
                     TimeInterval(DarkAndAfter(datetime.time(17, 0, 0, 0, tz),  place),     # on if it is dark and after 17,
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],    # off at 22:30

               # Front left
               2 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place), # on 15 mins after sunset
                     AbsoluteTimepoint(datetime.time(22, 35, 0, 0, tz))) ],                 # off at 22:35

               # Front right
               3 : [ TimeInterval(AbsoluteTimepoint(datetime.time(6, 15, 0, 0, tz)),           # on at 6.15
                                  LightOrAfter(datetime.time(7, 30, 0, 0, tz), place)),        # of at 7:30 or sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 1), place),     # on 1 minute after sunset
                                  AbsoluteTimepoint(datetime.time(23, 0, 0, 0, tz))) ],        # off at 23:00

               # outside corner
               4 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place),    # on 30 mins after sunset
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],       # off at 22:30

               # akvarium
               5 : [ TimeInterval(AbsoluteTimepoint(datetime.time(7, 0, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(23, 0, 0, 0, tz))) ]
             }
    return scheme
