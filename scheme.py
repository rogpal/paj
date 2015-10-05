
import pytz
import datetime
import tzlocal
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import SunsetTimepoint
from interval import AbsoluteTimepoint

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
