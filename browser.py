""" Connect to the  game. """

from selenium import webdriver
import time

def initialize():
    """ Launch a browser """
    global browser
    browser = webdriver.Firefox()
    browser.get("https://excess-catamarans.com/challenge")
    browser.find_element_by_id('accept-cookies').click()
    browser.switch_to.frame("login-iframe")

def login(u, p):
    """ Attempt to login automatically """
    browser.find_element_by_css_selector('[for="name"]').click()
    browser.find_element_by_id('name').send_keys(u)
    browser.find_element_by_css_selector('[for="pass"]').click()
    browser.find_element_by_id('pass').send_keys(p)
    # time.sleep(2)
    # browser.sendKeys(Keys.PAGE_DOWN)
    # .scrollIntoView()
    b = browser.find_element_by_css_selector('[onclick="javascript:goLogin()"]')
    # browser.execute_script("arguments[0].scrollIntoView();", b)
    b.click()

def quit(delay):
    time.sleep(delay)
    browser.close()
