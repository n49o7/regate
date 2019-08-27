""" Module to steer the boat. """

from selenium.webdriver.common.keys import Keys
import browser
# import logging

def rte(route):
    """ Set a course. """
    rte = browser.browser.find_element_by_id('boat.cap')
    rte.send_keys(Keys.CONTROL + "a")
    rte.send_keys(route)
    rte.send_keys(Keys.RETURN)
    # logging.info('Setting course %r°.', rte)

def ang(angle):
    """ Set a wind angle. """
    ang = browser.browser.find_element_by_id('boat.capReg')
    ang.send_keys(Keys.CONTROL + "a")
    ang.send_keys(angle)
    ang.send_keys(Keys.RETURN)
    # logging.info('Setting wind angle %a°.', ang)

def rig(arg=False):
    """ Set a sail configuration. Use its number (0 to 4) or name (ex:'GV Genois'). """
    sails = browser.browser.find_elements_by_css_selector('[damo-trigger="changeSail(this)"]')
    for s in sails:
        if arg == s.get_attribute('title') or arg == sails.index(s):
            s.click()
            # logging.info('Selecting sail %s: %s', sails.index(s), s.get_attribute('title'))
