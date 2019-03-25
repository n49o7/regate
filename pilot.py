# Steering the boat.
from selenium.webdriver.common.keys import Keys
import collect as co
import datetime
import time
import logging
import random

def rte(route):
    # Set a course.
    rte = co.browser.find_element_by_id('boat.cap')
    rte.send_keys(Keys.CONTROL + "a")
    rte.send_keys(route)
    rte.send_keys(Keys.RETURN)

def ang(angle):
    # Set a wind angle.
    ang = co.browser.find_element_by_id('boat.capReg')
    ang.send_keys(Keys.CONTROL + "a")
    ang.send_keys(angle)
    ang.send_keys(Keys.RETURN)

def rig(arg=False):
    # Set a sail configuration. Use its number (0 to 4) or name (ex:'GV Genois').
    sails = co.browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]')
    # success = False
    for s in sails:
        if arg == s.get_attribute('title') or arg == sails.index(s):
            s.click()
            logging.info('Selecting sail %s: %s', sails.index(s), s.get_attribute('title'))

def circle(sails=[0,1,2,3,4]):
    # Sail in circles, trying specified configurations and recording data.
    logging.info('Started circling with sails %s at %s', sails, datetime.datetime.now())
    co.params()
    out_r = co.data[2]
    out_s = co.data[4]
    for s in sails:
        rig(s)
        for a in range(-179,180,2):
            ang(a)
            d = random.randint(1,300)/1000
            time.sleep(2+d)
            co.params()
            co.export()
    # ang(0)
    rte(out_r)
    rig(out_s)
    logging.info('Ended circling %s', datetime.datetime.now())

def detect(limit=30):
    # If the latest wind speed is of interest, sail in circles.
    # "limit" is (very) roughly the number of minutes to run this for
    global w_spd_todo
    logging.info('Started detecting %s', datetime.datetime.now())
    t = 0
    while 0 <= t <= limit*1.5:
        co.params()
        s = round(float(co.data[1]))
        if s in w_spd_todo:
            logging.info('Wind found: %s. Sails found: %s.', s, w_spd_todo[s])
            limit -= len(w_spd_todo[s]) * 6
            circle(sails=w_spd_todo[s])
            del w_spd_todo[s]
        t += 1
        time.sleep(40)
    logging.info('Ended detecting %s', datetime.datetime.now())

def detect_old(limit=30):
    # If the latest wind speed is of interest, sail in circles.
    # "limit" is (very) roughly the number of minutes to run this for
    global w_spd_todo
    logging.info('Started detecting %s', datetime.datetime.now())
    t = 0
    while len(w_spd_todo) > 0 and 0 <= t <= limit*1.5:
    # while len(w_spd_todo) > 15:
        # best_sail()
        co.params()
        s = round(float(co.data[1]))
        if s in w_spd_todo:
            if s in w_spd_todo:
                logging.info('Wind found: %s. Sails found: %s.', s, w_spd_todo[s])
                limit -= len(w_spd_todo[s]) * 6
                circle(sails=w_spd_todo[s])
                del w_spd_todo[s]
            else:
                logging.info('Wind found: %s.', s)
                limit -= 30
                circle()
                w_spd_todo.remove(s)
        t += 1
        time.sleep(40)
    logging.info('Ended detecting %s', datetime.datetime.now())

def best_sail():
    pass

# def best_sail():
#     # Try all sails and set the best one.
#     sails = browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]')
#     initial_speed = data[5]
#     best = current_sail()
#     logging.info('Trying to find the best sail by beating %s with %s', initial_speed, best)
#     for s in sails:
#         s.click()
#         time.sleep(1.5)
#         name = s.get_attribute('title')
#         speed = current_b_spd()
#         logging.info('Sail %s shows speed %s', name, speed)
#         if speed > initial_speed:
#             best = name
#     logging.info('Found the best sail: %s', name)
#     rig(best)
#     # return best
