"""
Steer the boat.
"""

from selenium.webdriver.common.keys import Keys
import browser
import logging

logging.basicConfig(filename='pilot.log',level=logging.DEBUG)

def rte(route):
    """ Set a course. """
    rte = browser.browser.find_element_by_id('boat.cap')
    rte.send_keys(Keys.CONTROL + "a")
    rte.send_keys(route)
    rte.send_keys(Keys.RETURN)
    logging.info('Set course %r°.', rte)

def ang(angle):
    """ Set a wind angle. """
    ang = browser.browser.find_element_by_id('boat.capReg')
    ang.send_keys(Keys.CONTROL + "a")
    ang.send_keys(angle)
    ang.send_keys(Keys.RETURN)
    logging.info('Set wind angle %a°.', ang)

def rig(arg=False):
    """ Set a sail configuration. Use its number (0 to 4) or name (ex:'GV Genois'). """
    sails = browser.browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]')
    for s in sails:
        if arg == s.get_attribute('title') or arg == sails.index(s):
            s.click()
            logging.info('Selected sail %s: %s', sails.index(s), s.get_attribute('title'))

#

def circle(sails=[0,1,2,3,4]):
    """ Sail in circles, trying specified configurations and recording data. """
    logging.info('Started circling with sails %s at %s', sails, datetime.datetime.now())
    browser.params()
    out_r = browser.data[2]
    out_s = browser.data[4]
    for s in sails:
        rig(s)
        for a in range(-179,180,2):
            ang(a)
            d = random.randint(1,300)/1000
            time.sleep(2+d)
            browser.params()
            browser.export()
    # ang(0)
    rte(out_r)
    rig(out_s)
    logging.info('Ended circling %s', datetime.datetime.now())

# def best_sail():
# """   Try all sails and set the best one. """
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
