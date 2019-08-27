"""
Scrape data from the web interface.
"""


import csv
import time
import datetime
import logging
logging.basicConfig(filename='regate.log',level=logging.INFO)



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

# def minimalize():
# """ Manipulate the CSS for a cleaner virtual sailing experience """
#     title
#         0000000000000
#     header, footer, .banner
#         visibility: collapse
#
#         display: flex /
#     .site_content
#         max-width: none
#     iframe
#         .video-wrapper, .banner
#             visibility: collapse
#         body
#             background: none / repeat
#         .mapBlock
#             position: inherit
#         #windMenu
#             left: none
#             top: none
#             margin:10px 0 0 10px
#
#         video-wrapper
#             visibility: collapse
#
#             display: inherit
#             border: none
#             top: none
#             left: none
#         #mapContainer, .containerUp
#             box-shadow: none
#             border: 1px solid #AAA
