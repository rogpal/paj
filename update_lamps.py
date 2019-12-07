import os
import lamp
import scheme
import place

nkp = place.Place(place.nkpCoord())
nkp.updateSunTimes()
myscheme = scheme.murklanScheme(nkp)
lamp.update(myscheme)

