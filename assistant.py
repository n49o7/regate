"""
Assistant for manual sailing.
"""

import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns

perf_speed = pd.read_csv('data/perf_speed_interpol.csv')

sns.heatmap(perf_speed, cmap="coolwarm")

def speed(w_ang, w_spd):
    """ Interpolated speed. """
    return perf_speed.iloc[w_spd, w_ang]

perf_sails = pd.read_csv('data/perf_sails_interpol.csv', index_col=0)

# perf_sails_long = perf_sails.stack().reset_index()
# perf_sails_long.columns = ['w_spd', 'w_ang', 'sail']
# perf_sails_long['w_ang'] = perf_sails_long['w_ang'].astype('int64')

# url = 'data/perf_sails_long.json'
# perf_sails_long.to_json(url, orient='records')
#
# url = 'data/perf_sails_long.csv'
# perf_sails_long.to_csv(url)

# alt.data_transformers.enable('default')
# alt.limit_rows(perf_sails_long, 8000)
# alt.data_transformers.disable_max_rows()

url = "file://D:/Work/Code/regate/data/perf_sails_long.json"

alt.Chart(url).mark_rect().encode(
    x = 'w_ang:O',
    y = 'w_spd:O',
    color = 'sail:N',
    # x = alt.X('w_ang'),
    # y = alt.Y('w_spd'),
    # color = alt.Color('sail'),
).properties(
    background='#FFF',
    width=600,
    height=300,
)

def sails(w_ang, w_spd):
    """ Sail to use for best interpolated speed. """
    return perf_sails.iloc[w_spd, w_ang].replace(' ','-')

def time(distance, w_spd, w_ang):
    """ Predicted travel time according to deviation from route. """
    s = speed(w_ang, w_spd)
    t = np.round(distance/(2*s), 2)
    return [s, t]

# f = []

def wind(w_azi, cap):
    """ Wind angle, between 0 and 180. """
    return (w_azi-cap)

def ang_360(a):
    """ Return the absolute value of the wind angle, between 0 and 360. """
    return int( np.round( a % 360 ))

def simulate(route, distance, w_spd, w_azi):
    w_ang = wind(w_azi, route)
    print('Route:', route, '°')
    print('Wind:', w_azi, '°')
    print('Wind angle:', w_ang, '°')
    print('Best performance:', speed(w_ang, w_spd),'kn')
    # print("Sail to use:", sails(w_ang,w_spd))
    global f
    l = []
    for deviation in range(89):
        d_rad = np.radians(deviation)
        detour = (distance/np.cos(d_rad))
        d_rel = +deviation if w_ang > 0 else -deviation
        w_ang_l = wind(w_azi+d_rel, route)
        w_ang_p = wind(w_azi-d_rel, route)
        t_l = time(detour, w_spd, w_ang_l)
        t_p = time(detour, w_spd, w_ang_p)
        sail_l = sails(w_ang_l, w_spd)
        sail_p = sails(w_ang_p, w_spd)
        l.append( [deviation] + [route-d_rel] + [w_ang_l] + t_l + [sail_l] + [route+d_rel] + [w_ang_p] + t_p + [sail_p] + [t_l[1]+t_p[1]] )
    # f = pd.DataFrame(l, columns=['dev', 'speed_L','time_L','speed_P','time_P','time_sum']).set_index(['dev'])
    f = pd.DataFrame(l, columns=['dev','cap_L','w_ang_L','speed_L','time_L','sail_L','cap_P','w_ang_P','speed_P','time_P','sail_P','time_sum'])
    # print(l)

simulate(90, 10, 6, 90)

f.loc[ f['time_sum'].idxmin() ]

alt.Chart(f).mark_area(clip=True).encode(
    alt.Y( 'time_sum:Q', scale=alt.Scale( domain=(0,f['time_sum'].min()*10) ) ),
    x='dev:Q'
    ).properties(background='#FFF')


# chart.save('assistant.png', scale_factor=2.0)
