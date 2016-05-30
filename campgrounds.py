'''
This script is designed to check availability of campgrounds for a range of dates.
It writes available campgrounds and dates to a file or/and sounds alarm if something is found.
If site's interface is changed, script needs to be adjusted for a new page layout.

Mikhail Rogozhin 2016
license: http://unlicense.org/
Python 3.4
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re
import argparse
import time
from datetime import date
from datetime import datetime
from calendar import monthrange
import sys

# reservable campgrounds can be found by searching for national park name here
# http://www.recreation.gov/
# mark important campground or park's name with * for an audio alert

Glacier = {
    'many glacier': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=136190',
    'st. mary': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70973'
    }

Yosemite = {
    'lower-pines': 'http://www.recreation.gov/camping/lower-pines/r/campgroundDetails.do?contractCode=NRSO&parkId=70928',
    'upper-pines': 'http://www.recreation.gov/camping/upper-pines/r/campgroundDetails.do?contractCode=NRSO&parkId=70925',
    'north-pines': 'http://www.recreation.gov/camping/north-pines/r/campgroundDetails.do?contractCode=NRSO&parkId=70927',
    'tuolomne meadows': 'http://www.recreation.gov/camping/tuolumne-meadows/r/campgroundDetails.do?contractCode=NRSO&parkId=70926',
    'bridalveil creek': 'http://www.recreation.gov/camping/bridalveil-creek-group-and-horse-camp/r/campgroundDetails.do?contractCode=NRSO&parkId=70931',
    'wawona': 'http://www.recreation.gov/camping/wawona/r/campgroundDetails.do?contractCode=NRSO&parkId=70924',
    'crane flat': 'http://www.recreation.gov/camping/crane-flat/r/campgroundDetails.do?contractCode=NRSO&parkId=70930',
    # 'crystal springs(south)':
    # 'http://www.recreation.gov/camping/crystal-springs-campground-midsized-group-sites/r/campgroundDetails.do?contractCode=NRSO&parkId=72486',
    # 'limestone(outside)':
    # 'http://www.recreation.gov/camping/limestone-campground/r/campgroundDetails.do?contractCode=NRSO&parkId=123440'
    'hodgdon meadow': 'http://www.recreation.gov/camping/hodgdon-meadow/r/campgroundDetails.do?contractCode=NRSO&parkId=70929'
    }

Sequoia = {
    'lodgepole': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70941',
    'dorst creek': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70940',
    'canyon view groupsite': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=110284',
    'potwisha': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=72461',
    'buckeye flat': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=72462',
    'sunset': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=110283',
    'crystal springs': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=72486',
    'stony creek': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=71554',
    'fairview (south of park)': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=71678',
    'goldledge (south)': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=71679'
    }

GrandCanyon = {
    'north rim': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70970',
    'demotte': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=108033',
    'jacob': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75417',
    'big springs cabin': 'http://www.recreation.gov/camping/big-springs-cabin-site/r/campgroundDetails.do?contractCode=NRSO&parkId=121740',
    'jumpup cabin': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=134090',
    }

Zion = {
    'watchman': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70923'
    }

Bryce = {
    'sunset': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=74088',
    'kings and creek': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=70101',
    'podunk guard station(south)': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75419',
    }
CapitolReef = {
    'aquarius ranger station': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75464',
    'sunglow': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75169',
    'capitol reef group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=72456'
    }

Canyonlands = {
    'campground': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=72489',
    'windwhistle': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75831'
    }

Arches = {
    'devils garden': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=74066',
    'goose island group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75835',
    # 'oak grove':
    # 'http://www.recreation.gov/unifSearchInterface.do?interface=%2FrecreationalAreaDetails.do&contractCode=NRSO&parkId=202159&facilityId=202159&agencyCode=70901\'
    'the ledge group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75832',
    'kens lake group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75838',
    'horsethief group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75837',
    'lone mesa group': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75839',
    'big bend': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75836',
    'onion creek': 'http://www.recreation.gov/unifSearchInterface.do?interface=camping&contractCode=NRSO&parkId=75834'
    }

# marking with * triggers bell when campsite is found
parks = {
    'Yosemite*': Yosemite,
    'Sequoia*': Sequoia,
    'Grand Canyon*': GrandCanyon,
  #  'Zion': Zion,
  #  'Bryce': Bryce,
  #  'CapitolReef': CapitolReef,
  #  'Canyonlands': Canyonlands,
  #  'Arches': Arches,
  #  'Glacier': Glacier
    }

def click(browser, element):
    actions = webdriver.ActionChains(browser)
    actions.click(element).perform()

def click_element_by_id(browser, id):
    element = browser.find_element_by_id(id)
    click(browser, element)

def spots_available(browser):
    campsites = browser.find_element_by_class_name("matchSummary")
    found = re.search('[0-9]+', campsites.text)
    return found.group()

def process_args():
    parser = argparse.ArgumentParser(description="Check campgrounds' availability")
    parser.add_argument('--start_month', type = int, choices=range(1, 13), help='month, i.e. [5] for May', required = True) 
    parser.add_argument('--start_day', type = int, choices=range(1, 32), help='day from which to look for campsites', required = True) 
    parser.add_argument('--flexibility_weeks', type = int, choices = [0, 2, 4], help='look for camping within this range in weeks. [0] exact date, [2] 2 weeks', default = 2)
    parser.add_argument('--filename', type = str, default = 'available_camps', help='file to output results')
    parser.add_argument('--silent', type = bool, default = False, choices = [True, False], help='ring a bell if found campground marked *')
    args = parser.parse_args()   
    return vars(args)

def sound_alarm(N):
    times = 0
    while(times < N):
        print('\a', end = '')
        times += 1

def really_want_this_one(name):
    return name.find('*') != -1

def print_dates(dates):
    i = 1
    for date in dates:
        print(date.rjust(10), end = " ")
        if (i % 7 == 0):
            print()
        i += 1
    print('\n')

def mark_all_parks():
    for park in list(parks):
        if (not really_want_this_one(park)):
            parks[park + "*"] = parks.pop(park)

def find_dates_available(browser, flexibility):
    available_dates = set()
    if (flexibility != 0):
        date_elements = browser.find_elements_by_link_text("A")
        for element in date_elements:
            link = element.get_attribute("href")
            found = re.search('[0-9]+/[0-9]+/[0-9]+', link)
            if (found):
                available = found.group()
                available_dates.add(available)
    list = sorted(available_dates, key = lambda x: datetime.strptime(x, "%m/%d/%Y"))
    if (flexibility == 4): # check next 2 weeks
        next = browser.find_element_by_link_text("Next 2 weeks >")
        click(browser, next)
        list += find_dates_available(browser, 2)
    return list
    
if __name__ == "__main__":
    mark_all_parks()

    args_dict = process_args()
    start_day = args_dict['start_day']
    start_month = args_dict['start_month']

    today = date.today()
    today_day = int(today.strftime('%d'))
    today_month = int(today.strftime('%m'))
    today_year = int(today.strftime('%y'))

    days_in_month = monthrange(today_year, start_month)[1]
    if (start_day > days_in_month):
        start_day = days_in_month
    if (start_month - today_month < 0):
        raise ValueError("start_month shouldn't be in the past") # winter camping is never packed anyways, ignoring January booking

    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(1)
    i = 0
    while True:
        filename = args_dict['filename'] + '_' + str(start_month) + '_' + str(start_day) + '.txt'
        f = open(filename, "w")
        for park, campgrounds in parks.items():
            print(park, file = f, flush = True)
            for campground, url in campgrounds.items():
                try:
                    browser.get(url)
                    # each element's id/name/xpath can be found by looking at
                    # page's source
                    sel = Select(browser.find_element_by_id('flexDates'))
                    # flexibility: [1] = flexible within 2 weeks; [2] = 4 weeks
                    flexibility = args_dict['flexibility_weeks']
                    if (flexibility == 4):
                        sel.select_by_index(2)
                    elif (flexibility == 2):
                        sel.select_by_index(1)
                    else:
                        sel.select_by_index(0)

                    # pick a date
                    click_element_by_id(browser, 'arrivalDate')
                    calendar = browser.find_element_by_id('popupCalendar')
                    browser.switch_to.frame(calendar)
                    today_month_cpy = today_month
                    while(start_month - today_month_cpy > 0):
                        click_element_by_id(browser, 'nextmonth')
                        today_month_cpy += 1
                    dates = browser.find_elements_by_link_text(str(start_day)) # could have one extra from previous month, like 30th
                    click(browser, dates[1]) # pick arrival date.
                    browser.switch_to.default_content()

                    # search
                    click_element_by_id(browser, 'filter')
                    spots = spots_available(browser)
                    if (spots != '0'):
                        # find dates available
                        dates_available = find_dates_available(browser, flexibility)                                              
                        print("\t" + campground + ": " + spots, file = f, flush = True)
                        if ((really_want_this_one(campground) or really_want_this_one(park)) and not args_dict['silent']):
                            sound_alarm(3)
                            print("found {0} campground: {1}({2})".format(park, campground, spots), flush = True)
                            print(url, flush = True)
                            print_dates(dates_available)
                except KeyboardInterrupt: # Ctrl + C to stop
                    print("Exiting")
                    browser.quit()
                    sys.exit()
                except Exception as problem:
                    print(type(problem), file = f)
                    print("for " + park + " " + campground + ": " + url, file = f)
                    print(problem, file = f)
                    print(problem, flush = True)
        print("finished check #"+str(i), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        i += 1
        time.sleep(60) # wait 60 sec after each run
    