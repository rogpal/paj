import os
import lamp
import scheme
import place

nkp = place.Place(place.nkpCoord())
nkp.findSunTimes()
myscheme = scheme.murklanScheme(nkp)
lamp.update(myscheme)

