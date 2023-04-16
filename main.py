import json
import logging
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

FACILITY_IDS = (10, 11, 12, 13)  # All badminton facility IDs
URL = 'https://www.mesrc.net/efacility/{id}/reserve'

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load from configuration file
with open('config.json', 'r') as fp:
    CONFIG = json.load(fp)

logging.info(f'Initializing configuration. Please check that all variables are correct.')
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

def timeit(msg: str):
    """
    Utility function to measure the time a function took to run
    :param msg: Formatted message to print
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            logging.info(msg.format(time=elapsed_time))
            return result
        return wrapper
    return decorator


@timeit('Retrieving form token took {time} seconds')
def get_form_token():
    """
    Retrieve the form token which is required for sending post requests
    It is a constant that changes each session (I think)
    :return:
    """

    content = requests.get(URL.format(id=10), cookies=REQUEST_COOKIES).content
    soup = BeautifulSoup(content, 'html.parser')
    element = soup.find('input', {'data-drupal-selector': 'edit-efacility-reserve-form-form-token'})
    return element.get('value')


def main():
    execute_time = datetime.strptime(CONFIG['execute'], '%d/%m/%Y %H:%M:%S')
    now = datetime.now()
    delta = execute_time - now

    if delta.total_seconds() > 0:
        logging.info(f'{delta.total_seconds()} total seconds until execution time. Sleeping program...')
        time.sleep(delta.total_seconds())
    else:
        logging.warning(f'Execution time has already passed. Starting program immediately...')

    payload = {
        'form_token': get_form_token(),
        'form_id': 'efacility_reserve_form',
        'reserve_date': CONFIG['date'].replace('/', '-'),
        'reserve_start_time': CONFIG['time_start'] * 3600,
        'reserve_end_time': CONFIG['time_end'] * 3600,
        'purpose': CONFIG['purpose'],
        'pax': CONFIG['pax'],
        'op': 'Submit',
        'efacility_id': None,  # To be set when sending the post request
    }

    for facility_id in FACILITY_IDS:
        start_time = time.perf_counter()
        payload['efacility_id'] = facility_id
        response = requests.post(URL.format(id=facility_id), cookies=REQUEST_COOKIES, data=payload)
        print(response.status_code)
        # print(response.headers)
        end_time = time.perf_counter()
        logging.info(f'Sending post request to Court {facility_id - 9} took {end_time - start_time} seconds')


if __name__ == '__main__':
    main()
