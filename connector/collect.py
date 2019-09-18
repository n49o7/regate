"""
Check and organize data.
"""

import csv
import time
import datetime
import logging

logging.basicConfig(filename='collect.log',level=logging.INFO)

def current_sail():
    """ Get the current sail """
    for i in browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]'):
        if '_on' in i.get_attribute('class'):
            return i.get_attribute("title")

def current_b_spd():
    """ Get the current boat speed """
    return browser.find_element_by_css_selector('[damo-id="boat.speed"]').text

def params():
    """ Get the current sailing parameters and store them in the global scope """
    global data
    b_sails = current_sail()
    # for i in browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]'):
    #     if '_on' in i.get_attribute('class'):
    #         b_sails = i.get_attribute("title")
    b_rte = browser.find_element_by_id('boat.cap').get_attribute("value")
    w_ang = browser.find_element_by_id('boat.capReg').get_attribute("value")
    w_azi = browser.find_element_by_css_selector('[damo-id="boat.wind.cap"]').text
    w_spd = browser.find_element_by_css_selector('[damo-id="boat.wind.force"]').text
    b_spd = current_b_spd()
    chrono = browser.find_element_by_css_selector('[damo-id="chrono.current.chrono"]').text
    b_lon = browser.find_element_by_css_selector('[damo-id="boat.pos.lon"]').text
    b_lat = browser.find_element_by_css_selector('[damo-id="boat.pos.lat"]').text
    # time = browser.find_element_by_css_selector('[damo-id="chrono.current.date"]').text
    # dist = browser.find_element_by_css_selector('[damo-id="boat.distance"]').text
    # nwp = browser.find_element_by_css_selector('[damo-id="boat.nextWp"]').text
    data = [w_azi, w_spd, b_rte, w_ang, b_sails, b_spd, chrono, b_lon, b_lat]

def export():
    """ Write the latest data to a file """
    global last
    with open(f, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|')
        diff = data[:6]
        if diff != last:
            writer.writerow(data)
            # logging.info('Wrote one row to %s', f)
            last = diff

def record(limit=30, i=4):
    """
    Record all the data.
    "limit" is roughly the number of minutes to run this for.
    "i" is the interval in seconds.
    """
    logging.info('Started recording %s', datetime.datetime.now())
    t = 0
    while t <= limit*60:
        export()
        t += i
        time.sleep(i)
    logging.info('Ended recording %s', datetime.datetime.now())

def detect(limit=30):
    """ If the latest wind speed is of interest, sail in circles. """
    # "limit" is (very) roughly the number of minutes to run this for
    global w_spd_todo
    logging.info('Started detecting %s', datetime.datetime.now())
    t = 0
    while 0 <= t <= limit*1.5:
        browser.params()
        s = round(float(browser.data[1]))
        if s in w_spd_todo:
            logging.info('Wind found: %s. Sails found: %s.', s, w_spd_todo[s])
            limit -= len(w_spd_todo[s]) * 6
            circle(sails=w_spd_todo[s])
            del w_spd_todo[s]
        t += 1
        time.sleep(40)
    logging.info('Ended detecting %s', datetime.datetime.now())
