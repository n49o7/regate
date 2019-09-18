"""
Useful functions.
"""

def wind(w_azi, cap):
    """ Wind angle, between 0 and 180. """
    return (w_azi-cap)

def ang_180(a):
    """ Return the absolute value of an angle (eg. the wind angle), between 0 and 180. """
    return int( np.degrees(np.arccos(np.cos(np.radians( int(a) % 360 )))) )

def ang_360(a):
    """ Return the absolute value of an angle, between 0 and 360. """
    return int( np.round( a % 360 ))

def dm_to_dd(dms):
    """ Convert degrees-minutes to decimal degrees. """
    d = float( dms.split('°')[0] )
    m = float( dms.split('°')[1][:-1] )
    return round( d + m/60, 6 )

def dd_to_dm(dd):
    """ Convert decimal degrees to degrees-minutes. """
    d = dd // 1
    m = dd % 1*60
    return str(d)+'° '+str(round(m,3))+"'"

def tf(time):
    """ Format a potentially decimal number of hours. """
    if '.' in str(time):
        return str(int(time-time%1)) + 'h ' + str(int(60*(time%1))) + 'm'
    else:
        return str(time) + 'h'

def df(date):
    """ Format a date from YYYYMMDD. """
    date = str(date)
    return date[:4]+'.'+date[4:6]+'.'+date[6:]
