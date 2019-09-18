"""
Make weather and time-to-travel predictions.
"""

import pandas as pd
import numpy as np
import requests

segments = pd.read_csv('geo/segments.csv').set_index('sid').sort_index()
# segments[:3]

waypoints = pd.read_csv('geo/waypoints.csv').set_index('pid').sort_index()
# waypoints[:3]

perf_speed = pd.read_csv('data/perfs_speed_interpol.csv')
# perf_sail = pd.read_csv('perfs_sail_raw.csv')
perf_sail = pd.read_csv('data/perfs_sail_interpol.csv')

# test_data = pd.read_csv('data_clean.csv')[40:140]
# test_data[:3]

def route_map(stop, date, time):
    """ List of segments until <stop>. """
    chrono = 0
    hops = pd.DataFrame(columns=['segment','time_to_complete','date_completed','time_completed','rte','w_azi','w_ang','w_spd','b_spd','b_sail']).set_index('segment')
    for seg in range(1, stop+1):
        dur = seg_duration(seg, date, time)
        chrono += dur
        edt = est_datetime(date, time, chrono)
        row = {'time_to_complete':tf(dur),'date_completed':df(edt[0]),'time_completed':tf(edt[1])}
        det = seg_detail(seg, date, time)
        row.update(det)
        hops.loc[int(seg),:] = row
    return hops

# bbox1 = 35.836731781015466+-3.0637545883655557+47.4943612826354+15.459194630384449
# bbox2 = 39.351290+1.933594+43.834527+10.788574

# bbox1, wm=0.2
route_map(18, 20190608, 0)

def cache_forecast(date,time):
    """ Wind forecast at YYYMMDD <date> and UTC <time>. """
    # global forecast
    # url = "https://vps614770.ovh.net:8197/getMapWind?action=getMapWind&day=" + str(date) + "&hour=" + str(time) + "&bbox=35.836731781015466+-3.0637545883655557+47.4943612826354+15.459194630384449&wm=0.2"
    url = "https://vps614770.ovh.net:8197/getMapWind?action=getMapWind&day=" + str(date) + "&hour=" + str(time) + "&bbox=39.351290+1.933594+43.834527+10.788574&wm=0.05"
    r = requests.get(url)
    columns = ['lat','lon','w_spd','w_azi','_1','_2','color']
    forecast = pd.DataFrame(r.json(), columns=columns)
    for c in columns[:-1]:
        forecast[c] = pd.to_numeric(forecast[c])
    return forecast

def wpts_map(stop, date, time):
    """ List of waypoints until <stop>. """
    chrono = 0
    hops = pd.DataFrame(columns=['waypoint', 'chrono', 'date_reached', 'time_reached']).set_index('waypoint')
    hops.loc[0,:] = [tf(0), df(date), tf(time)]
    for wpt in range(1, stop+1):
        seg = segments.index[segments['end'] == wpt][0]
        chrono += seg_duration(seg, date, time)
        edt = est_datetime(date, time, chrono)
        row = [tf(chrono), df(edt[0]), tf(edt[1])]
        hops.loc[int(wpt),:] = row
    return hops

wpts_map(18, 20190608, 0)

def time_sum(stop, date, time):
    """ Time taken until <stop>. """
    chrono = 0
    for seg in range(1, stop+1):
        edt = est_datetime(date, time, chrono)
        chrono += seg_duration(seg, edt[0], edt[1])
    return chrono

def est_datetime(date, time, chrono):
    """ Sum date and duration. """
    date += chrono // 24
    time = (time + chrono) % 24
    return (int(date), round(time,2))

def closest(df, param, target):
    """
        Find the closest point for which there is data.
        "closest(closest(x))" only makes sense in an isometric space!
    """
    x = df.iloc[df.eval(param+'-'+str(target)).abs().argsort()]
    return x[x[param]==x.iloc[0][param]]

def w_at(date, time, lat, lon):
    """ Wind speed and azimuth. """
    forecast = cache_forecast(date, time)
    return closest( closest(forecast, 'lon', lon), 'lat', lat )

def seg_detail(seg, date, time):
    """ Sailing parameters for segment <seg>. """
    start = segments.loc[seg,'start']
    coord = (waypoints.loc[start,'lat'], waypoints.loc[start,'lon'])
    wind = w_at(date, time, coord[0], coord[1])
    rte = segments.loc[seg,'bearing']
    w_azi = int(round(wind['w_azi']))
    w_ang = int(wind_angle(w_azi, rte))
    w_spd = int(round(wind['w_spd']))
    w_ang_a = ang_abs(w_ang)
    b_spd = speed_at(w_ang_a, w_spd)
    b_sail = sail_at(w_ang_a, w_spd)
    dist = segments.loc[seg,'dist']
    time = round(dist/b_spd, 2)
    return {"rte":rte,"w_azi":w_azi,"w_ang":w_ang,"w_spd":w_spd, "b_spd":b_spd, "b_sail":b_sail}

def seg_duration(seg, date, time):
    """ Time taken to complete segment <seg>. """
    start = segments.loc[seg,'start']
    coord = (waypoints.loc[start,'lat'], waypoints.loc[start,'lon'])
    wind = w_at(date, time, coord[0], coord[1])
    rte = segments.loc[seg,'bearing']
    w_ang = ang_abs( wind_angle(round(wind['w_azi']), rte) )
    b_spd = speed_at(w_ang, round(wind['w_spd']))
    dist = segments.loc[seg,'dist']
    duration = round(dist/b_spd, 2)
    return float(duration)

def speed_at(w_ang, w_spd):
    """ Best recorded speed. """
    return perf_speed.iloc[w_spd, w_ang]

def sail_at(w_ang, w_spd):
    """ Sail used for best recorded speed. """
    return perf_sail.iloc[w_spd, w_ang]

def sails(w_ang, w_spd):
    """ Sail to use for best interpolated speed. """
    return perf_sails.iloc[w_spd, w_ang].replace(' ','-')

def time(distance, w_spd, w_ang):
    """ Predicted travel time according to deviation from route. """
    s = speed(w_ang, w_spd)
    t = np.round(distance/(2*s), 2)
    return [s, t]

# def simulate(route, distance, w_spd, w_azi):
#     w_ang = wind(w_azi, route)
#     print('Route:', route, '°')
#     print('Wind:', w_azi, '°')
#     print('Wind angle:', w_ang, '°')
#     print('Best performance:', speed(w_ang, w_spd),'kn')
#     # print("Sail to use:", sails(w_ang,w_spd))
#     global f
#     l = []
#     for deviation in range(89):
#         d_rad = np.radians(deviation)
#         detour = (distance/np.cos(d_rad))
#         d_rel = +deviation if w_ang > 0 else -deviation
#         w_ang_l = wind(w_azi+d_rel, route)
#         w_ang_p = wind(w_azi-d_rel, route)
#         t_l = time(detour, w_spd, w_ang_l)
#         t_p = time(detour, w_spd, w_ang_p)
#         sail_l = sails(w_ang_l, w_spd)
#         sail_p = sails(w_ang_p, w_spd)
#         l.append( [deviation] + [route-d_rel] + [w_ang_l] + t_l + [sail_l] + [route+d_rel] + [w_ang_p] + t_p + [sail_p] + [t_l[1]+t_p[1]] )
#     # f = pd.DataFrame(l, columns=['dev', 'speed_L','time_L','speed_P','time_P','time_sum']).set_index(['dev'])
#     f = pd.DataFrame(l, columns=['dev','cap_L','w_ang_L','speed_L','time_L','sail_L','cap_P','w_ang_P','speed_P','time_P','sail_P','time_sum'])
#     # print(l)
