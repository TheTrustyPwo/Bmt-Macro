import json
import logging
import os
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

FACILITY_IDS = (10, 11, 12, 13)  # All badminton facility IDs
URL = 'https://www.mesrc.net/efacility/{id}/reserve'

os.environ['WDM_LOG'] = '0'  # Silence webdriver log messages
logging.getLogger(requests.packages.urllib3.__package__).setLevel(logging.ERROR)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load from configuration file
with open('config.json', 'r') as fp:
    CONFIG = json.load(fp)

logging.info(f'Initializing configuration. Please check that all variables are correct.')
logging.info(f'HEADLESS: {CONFIG["headless"]}')
logging.info(f'EXECUTION TIME: {CONFIG["execute"]}')
logging.info(f'DATE: {CONFIG["date"]}')
logging.info(f'TIME START: {CONFIG["time_start"]}')
logging.info(f'TIME END: {CONFIG["time_end"]}')
logging.info(f'PURPOSE: {CONFIG["purpose"]}')
logging.info(f'PAX: {CONFIG["pax"]}')

# Load cookie file
REQUEST_COOKIES = {}
with open('cookies.json', 'r') as fp:
    COOKIES = json.load(fp)
    for cookie in COOKIES:
        cookie["sameSite"] = "None"  # Overrides null value when exported from CookieEditor
        REQUEST_COOKIES[cookie['name']] = cookie['value']  # Setting cookie dict for requests library

SERVICE = Service(ChromeDriverManager().install())
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

if CONFIG['headless']:
    OPTIONS.add_argument('--headless')

driver = webdriver.Chrome(service=SERVICE, options=OPTIONS)

# Initialize cookies
# Enables network tracking to use the Network.setCookie method
driver.execute_cdp_cmd('Network.enable', {})

for cookie in COOKIES:
    driver.execute_cdp_cmd('Network.setCookie', cookie)

# Disable network tracking to not affect performance
driver.execute_cdp_cmd('Network.disable', {})


def select_date(date: str) -> None:
    """
    Parses the date string and selects the date
    from the datepicker calendar
    :param date: Date string in the format DD/MM/YYYY
    :return:
    """
    date = datetime.strptime(date, '%d/%m/%Y')
    driver.find_element(By.ID, 'edit-reserve-date').click()
    Select(driver.find_element(By.CLASS_NAME, 'ui-datepicker-month')).select_by_value(str(date.month - 1))
    Select(driver.find_element(By.CLASS_NAME, 'ui-datepicker-year')).select_by_value(str(date.year))
    driver.find_elements(By.CLASS_NAME, 'ui-state-default')[date.day - 1].click()


def get_availability(date: str) -> list[int]:
    """
    Get the availability of a certain date
    :param date: Date string in the format DD/MM/YYYY
    :return: Returns the list of available timings in a list
    """
    available = []
    select_date(date)
    time.sleep(0.1)

    # Iterates through the reservations table to find available timings
    data = driver.find_element(By.ID, 'reservations').find_elements(By.XPATH, "//table/tbody/tr")
    for t, entry in enumerate(data[1:], 7):
        state = entry.find_elements(By.TAG_NAME, 'td')[1].get_attribute('class')
        if state != 'available':
            continue
        available.append(t)

    return available


def book(date: str, start: int, end: int, purpose: str = "Recreational", pax: int = 4) -> None:
    """
    Book the current facility with the specified parameters
    :param date: Date to book the facility on
    :param start: Starting timing, in 24-hour format
    :param end: Ending timing, in 24-hour format
    :param purpose: Purpose, as required by the booking form
    :param pax: Pax, as required by the booking form
    :return:
    """
    select_date(date)
    Select(driver.find_element(By.ID, 'edit-reserve-start-time')).select_by_value(str(start * 3600))
    Select(driver.find_element(By.ID, 'edit-reserve-end-time')).select_by_value(str(end * 3600))
    driver.find_element(By.ID, 'edit-purpose').send_keys(purpose)
    driver.find_element(By.ID, 'edit-pax').send_keys(str(pax))
    driver.find_element(By.XPATH, '//input[@id="edit-submit" and @value="Submit"]').click()


def check_and_book(facility_id: int) -> bool:
    """
    Integrates both checking of availability and booking the facility
    if it's available into this function
    :param facility_id: Facility ID to check and book
    :return: Return True if booking is successful
    """
    driver.get(URL.format(id=facility_id))
    logging.info(f'Checking availability of Badminton Court {fid - 9}...')
    available = get_availability(CONFIG['date'])
    if CONFIG['time_start'] not in available or (CONFIG['time_end'] - 1) not in available:
        logging.warning(f'Badminton Court {fid - 9} not available... Skipping...')
        return False
    logging.info(f'Badminton Court {fid - 9} available! Booking now...')
    book(CONFIG['date'], CONFIG['time_start'], CONFIG['time_end'], CONFIG['purpose'], CONFIG['pax'])
    logging.info(f'Successfully booked Badminton Court {fid - 9} for {CONFIG["time_start"]} to {CONFIG["time_end"]} on {CONFIG["date"]}!')
    return True


if __name__ == '__main__':
    execute_time = datetime.strptime(CONFIG['execute'], '%d/%m/%Y %H:%M:%S')
    now = datetime.now()
    delta = execute_time - now

    if delta.total_seconds() > 0:
        driver.get('https://www.mesrc.net/')  # Loads the webpage first to prevent some bugs
        logging.info(f'{delta.total_seconds()} total seconds until execution time. Sleeping program...')
        time.sleep(delta.total_seconds())

    for fid in FACILITY_IDS:
        res = check_and_book(fid)
        if not res:
            continue
        logging.info(f'Available court was found and booked.')
        logging.info(f'Visit https://www.mesrc.net/user/0/efacility to check your booking')
        break

    logging.info('Program Stopping...')
