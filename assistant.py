import pandas as pd
import numpy as np
import altair as alt

def wind(w_azi, cap):
    """ Wind angle, between 0 and 180. """
    return (w_azi-cap) % 180

def ang_360(a):
    # Return the absolute value of the wind angle, between 0 and 360.
    return int( np.round( a % 360 ))

perf_speed = pd.read_csv('data/perfs_speed_interpol.csv')

def speed(w_ang, w_spd):
    """ Interpolated speed. """
    return perf_speed.iloc[w_spd, w_ang]

perf_sails = pd.read_csv('data/perfs_sail_interpol.csv', index_col=0)

def sails(w_ang, w_spd):
    """ Sail to use for best interpolated speed. """
    return perf_sails.iloc[w_spd, w_ang].replace(' ','-')

def time(distance, w_spd, w_ang):
    """ Predicted travel time according to deviation from route. """
    s = speed(w_ang, w_spd)
    t = np.round(distance/(2*s), 1)
    return [s, t]

# f = []

def simulate(route, distance, w_spd, w_azi):
    w_ang = wind(w_azi, route)
    print('Wind angle:', w_ang, '°')
    print('Best performance:', speed(w_ang, w_spd),'kn')
    # print("Sail to use:", sails(w_ang,w_spd))
    global f
    l = []
    for deviation in range(86):
        d_rad = np.radians(deviation)
        detour = (distance/np.cos(d_rad))
        d_rel = +deviation if w_ang > 0 else -deviation
        w_ang_l = wind(ang_360(w_azi+d_rel), route)
        w_ang_p = wind(ang_360(w_azi-d_rel), route)
        t_l = time(detour, w_spd, w_ang_l)
        t_p = time(detour, w_spd, w_ang_p)
        sail_l = sails(w_ang_l, w_spd)
        sail_p = sails(w_ang_p, w_spd)
        l.append( [deviation] + [route+d_rel] + [w_ang_l] + t_l + [sail_l] + [route-d_rel] + [w_ang_p] + t_p + [sail_p] + [t_l[1]+t_p[1]] )
    # f = pd.DataFrame(l, columns=['dev', 'speed_L','time_L','speed_P','time_P','time_sum']).set_index(['dev'])
    f = pd.DataFrame(l, columns=['dev','cap_L','w_ang_L','speed_L','time_L','sail_L','cap_P','w_ang_P','speed_P','time_P','sail_P','time_sum'])
    # print(l)

simulate(149, 99, 7, 158)
f

alt.Chart(f).mark_area().encode(x='dev:Q', y='time_sum:Q').properties(background='#FFF')


# chart.save('assistant.png', scale_factor=2.0)
