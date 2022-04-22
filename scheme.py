
import pytz
import datetime
import tzlocal
from interval import TimeInterval
from interval import SunriseTimepoint
from interval import SunsetTimepoint
from interval import AbsoluteTimepoint
from interval import DarkAndAfter
from interval import LightOrAfter
from enum import Enum

class Weekday(Enum):
    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6


#
# Scheme structure:
#
# [ ([ list of days ], scheme_for_days), .... ]
#
# where
#
# scheme_for_days is
# { <lamp_no> : [ list of intervals ] }
#
#
#
#


def murklanScheme(place) :
    tz = tzlocal.get_localzone()

                # TV corner
    weekend = { 1 : [ TimeInterval(DarkAndAfter(datetime.time(8, 0, 0, 0, tz), place),      # on at 8:00 and if it is dark,
                                   LightOrAfter(datetime.time(9, 30, 0, 0, tz), place)),    # off at 09:30 or light
                     TimeInterval(DarkAndAfter(datetime.time(16, 0, 0, 0, tz),  place),     # on if it is dark and after 16,
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],    # off at 22:30

               # Front left
               2 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place), # on 15 mins after sunset
                     AbsoluteTimepoint(datetime.time(22, 35, 0, 0, tz))) ],                 # off at 22:35

               # Front right
               3 : [ TimeInterval(DarkAndAfter(datetime.time(7, 30, 0, 0, tz), place),         # on at 7:30 and dark
                                  LightOrAfter(datetime.time(9, 0, 0, 0, tz), place)),         # of at 9:00 or sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = -15), place),     # on 1 minute after sunset
                                  AbsoluteTimepoint(datetime.time(23, 0, 0, 0, tz))) ],        # off at 23:00

               # outside corner
               4 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place),    # on 30 mins after sunset
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],       # off at 22:30

               # akvarium
               5 : [ TimeInterval(AbsoluteTimepoint(datetime.time(8, 0, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],

	       # christmas stuff
               6 : [ TimeInterval(AbsoluteTimepoint(datetime.time(7, 30, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(11, 0, 0, 0, tz))),
                     TimeInterval(AbsoluteTimepoint(datetime.time(15, 0, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(23, 56, 0, 0, tz))) ],


               7 : [ TimeInterval(AbsoluteTimepoint(datetime.time(7, 40, 0, 0, tz)),
                                  SunriseTimepoint(datetime.timedelta(minutes = 20), place)),    # off 20 min after sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(-30), place),                      # on 30 minutes before sunset
                                  AbsoluteTimepoint(datetime.time(23, 56, 0, 0, tz))) ],

	       # Julia
               8 : [ TimeInterval(DarkAndAfter(datetime.time(8, 0, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(10, 0, 0, 0, tz))),
                     TimeInterval(DarkAndAfter(datetime.time(15, 0, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(22, 0, 0, 0, tz))) ],

	       # Ludvig
               9 : [ TimeInterval(DarkAndAfter(datetime.time(16, 5, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],

               # Dragon foot
               10 : [ TimeInterval(DarkAndAfter(datetime.time(18, 0, 0, 0, tz), place),          # on at 18:00 and dark
                                   AbsoluteTimepoint(datetime.time(21, 30, 0, 0, tz))) ],         # off at 21:30

               # Outside
               11 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 0), place),       # on at sunset
                                   AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],          # off at 22:30

               # Star
               12 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 0), place),       # on at sunset
                                   AbsoluteTimepoint(datetime.time(22, 00, 0, 0, tz))) ],          # off at 22:00


               # Outside back
               13 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = -30), place),       # on half hour before sunset
                                   AbsoluteTimepoint(datetime.time(23, 00, 0, 0, tz))) ],           # off at 23:00

               # Hallway
               14 : [ TimeInterval(AbsoluteTimepoint(datetime.time(8, 0, 0, 0, tz)),                # on at 08:00
                                   AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ]            # off at 22:30

                
             }




               # TV corner
    workday = { 1 : [ TimeInterval(DarkAndAfter(datetime.time(6, 15, 0, 0, tz), place),      # on at 6.15 and if it is dark,
                                  AbsoluteTimepoint(datetime.time(7, 30, 0, 0, tz))),       # off at 07:30
                     TimeInterval(DarkAndAfter(datetime.time(17, 0, 0, 0, tz),  place),     # on if it is dark and after 17,
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],    # off at 22:30


               # Front left
               2 : [ TimeInterval(AbsoluteTimepoint(datetime.time(6, 10, 0, 0, tz)),           # on at 6.15
                                  LightOrAfter(datetime.time(7, 30, 0, 0, tz), place)),        # of at 7:30 or sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = -15), place),     # on 1 minute after sunset
                                  AbsoluteTimepoint(datetime.time(23, 15, 0, 0, tz))) ],        # off at 23:00


               # Front right
               3 : [ TimeInterval(AbsoluteTimepoint(datetime.time(6, 15, 0, 0, tz)),           # on at 6.15
                                  LightOrAfter(datetime.time(7, 30, 0, 0, tz), place)),        # of at 7:30 or sunrise
                     TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = -15), place),     # on 1 minute after sunset
                                  AbsoluteTimepoint(datetime.time(23, 0, 0, 0, tz))) ],        # off at 23:00

               # outside corner
               4 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 15), place),    # on 30 mins after sunset
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],       # off at 22:30

               # akvarium
               5 : [ TimeInterval(AbsoluteTimepoint(datetime.time(7, 0, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ],

	       # christmas stuff
               6 : [ TimeInterval(AbsoluteTimepoint(datetime.time(6, 10, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(10, 50, 0, 0, tz))),
                     TimeInterval(AbsoluteTimepoint(datetime.time(15, 30, 0, 0, tz)),
                                  AbsoluteTimepoint(datetime.time(22, 10, 0, 0, tz))) ],
                
               7 : [ TimeInterval(AbsoluteTimepoint(datetime.time(6, 20, 0, 0, tz)),
                                  SunriseTimepoint(datetime.timedelta(minutes = 20), place)),    # off 20 min after sunrise                                  
                     TimeInterval(SunsetTimepoint(datetime.timedelta(-30), place),               # on 30 minutes before sunset
                                  AbsoluteTimepoint(datetime.time(22, 20, 0, 0, tz))) ],

	       # Julia
               8 : [ TimeInterval(DarkAndAfter(datetime.time(6, 0, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(7, 30, 0, 0, tz))),
                     TimeInterval(DarkAndAfter(datetime.time(15, 0, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(21, 30, 0, 0, tz))) ],

	       # Ludvig
               9 : [ TimeInterval(DarkAndAfter(datetime.time(16, 10, 0, 0, tz), place),
                                  AbsoluteTimepoint(datetime.time(22, 0, 0, 0, tz))) ],

               # Dragon foot
               10 : [ TimeInterval(DarkAndAfter(datetime.time(18, 00, 0, 0, tz), place),     # on at 18:00 and dark
                                   AbsoluteTimepoint(datetime.time(21, 30, 0, 0, tz))) ],    # off at 21:30

               # Outside
               11 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 0), place),  # on at sunset
                                   AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))),      # off at 22:30
                      TimeInterval(DarkAndAfter(datetime.time(6, 15, 0, 0, tz), place),
                                   AbsoluteTimepoint(datetime.time(7, 15, 0, 0, tz))) ],
               # Star
               12 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = 0), place),       # on at sunset
                                   AbsoluteTimepoint(datetime.time(22, 00, 0, 0, tz))) ],         # off at 22:00

               # Outside back
               13 : [ TimeInterval(SunsetTimepoint(datetime.timedelta(minutes = -30), place),       # on half hour before sunset
                                   AbsoluteTimepoint(datetime.time(23, 00, 0, 0, tz))) ],            # off at 23:00

               # Hallway
               14 : [ TimeInterval(AbsoluteTimepoint(datetime.time(16, 0, 0, 0, tz)),          # on 16:00
                                   AbsoluteTimepoint(datetime.time(22, 30, 0, 0, tz))) ]       # off at 22:30
                
                

             }


    scheme = [ ([Weekday.sun, Weekday.sat], weekend),
               ([Weekday.mon, Weekday.tue, Weekday.wed, Weekday.thu, Weekday.fri], workday) ]
    return scheme
