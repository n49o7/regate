import pandas as pd
import numpy as np
import altair as alt
import datetime
import time
import logging
import random
import requests
import csv

class Captain:


class Pilot:
    """ Control the boat. """
    # def __init__(self):
    #     self.is_active = False
    def detect_wind():
        """ If the current wind speed is of interest, sail in circles. """
    def make_circles():
        """ Sail in circles, trying specified configurations and recording data. """
    def rte(route):
        """ Set a course. """
        rte = co.browser.find_element_by_id('boat.cap')
        rte.send_keys(Keys.CONTROL + "a")
        rte.send_keys(route)
        rte.send_keys(Keys.RETURN)
        logging.info('Setting route %s°.', route)
    def ang(angle):
        """ Set a wind angle. """
        ang = co.browser.find_element_by_id('boat.capReg')
        ang.send_keys(Keys.CONTROL + "a", angle)
        ang.send_keys(angle)
        ang.send_keys(Keys.RETURN)
        logging.info('Setting wind angle %s°.')
    def rig(arg):
        """ Set a sail configuration. Use its number (0 to 4) or name (ex:'GV Genois'). """
        sails = co.browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]')
        for s in sails:
            if arg == s.get_attribute('title') or arg == sails.index(s):
                s.click()
                logging.info('Selecting sail %s: %s.', sails.index(s), s.get_attribute('title'))
    def max_dev(range=10):
        """ Determine the maximum offset from route, both left and right.
         Specify the range over which to test in nautical miles. """
        for a in range(-45,46):
            w_spd = Book.data['w_spd']
            t = range / Book.speed_at(a, w_spd)
            na = Book.data['w_ang'] - a
            nt = range / (np.cos(a) * Book.speed_at(na, w_spd))
            print(t, nt)

class Book:
    """ Hold data about sailing performance. """
    # w_azi = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.wind.cap"]').text
    # w_spd = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.wind.force"]').text
    # b_rte = Browser.webdriver.find_element_by_id('boat.cap').get_attribute("value")
    # w_ang = Browser.webdriver.find_element_by_id('boat.capReg').get_attribute("value")
    # b_sails = current_sail()
    # b_spd = current_b_spd()
    # chrono = Browser.webdriver.find_element_by_css_selector('[damo-id="chrono.current.chrono"]').text
    # b_lon = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.pos.lon"]').text
    # b_lat = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.pos.lat"]').text
    def __init__(self):
        segments = pd.read_csv('geo/segments.csv').set_index('sid').sort_index()
        waypoints = pd.read_csv('geo/waypoints.csv').set_index('pid').sort_index()
        perf_speed = pd.read_csv('perfs_speed_interpol.csv')
        perf_sail = pd.read_csv('perfs_sail_interpol.csv')
        data = {}
    def sailing_params():
        """ Get the current sailing parameters. """
        data['w_azi'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.wind.cap"]').text
        data['w_spd'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.wind.force"]').text
        data['b_rte'] = Browser.webdriver.find_element_by_id('boat.cap').get_attribute("value")
        data['w_ang'] = Browser.webdriver.find_element_by_id('boat.capReg').get_attribute("value")
        data['b_sails'] = current_sail()
        data['b_spd'] = current_b_spd()
        data['chrono'] = Browser.webdriver.find_element_by_css_selector('[damo-id="chrono.current.chrono"]').text
        data['b_lon'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.pos.lon"]').text
        data['b_lat'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.pos.lat"]').text
        # ['time'] = Browser.webdriver.find_element_by_css_selector('[damo-id="chrono.current.date"]').text
        # ['dist'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.distance"]').text
        # ['nwp'] = Browser.webdriver.find_element_by_css_selector('[damo-id="boat.nextWp"]').text
        # return data
    def speed_at(w_ang, w_spd):
        """ Best recorded speed. """
        return perf_speed.iloc[w_spd, w_ang]
    def sail_at(w_ang, w_spd):
        """ Sail used for best recorded speed. """
        return perf_sail.iloc[w_spd, w_ang]

class Forecast:
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

class Browser:
    def __init__(self):
        self.webdriver = webdriver.Firefox()
        webdriver.get("https://excess-catamarans.com/challenge")
        webdriver.find_element_by_id('accept-cookies').click()
        webdriver.switch_to.frame("login-iframe")
    def login(u, p):
        """ Attempt to login automatically. """
        webdriver.find_element_by_css_selector('[for="name"]').click()
        webdriver.find_element_by_id('name').send_keys(u)
        webdriver.find_element_by_css_selector('[for="pass"]').click()
        webdriver.find_element_by_id('pass').send_keys(p)
        webdriver.send_keys(Keys.DOWN)
        webdriver.find_element_by_css_selector('[onclick="javascript:goLogin()"]').click()

# class Utils:
def wind_angle(rte, w_azi):
    """ Wind angle from route and wind azimuth. """
    return rte - w_azi
def ang_abs(a):
    """ Absolute value of an angle (eg. the wind angle), between 0 and 180. """
    return int( np.degrees(np.arccos(np.cos(np.radians( int(a) % 360 )))) )
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
def closest(df, param, target):
    """
        Find the closest point for which there is data.
        "closest(closest(x))" only makes sense in planar space!
    """
    x = df.iloc[df.eval(param+'-'+str(target)).abs().argsort()]
    return x[x[param]==x.iloc[0][param]]
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
