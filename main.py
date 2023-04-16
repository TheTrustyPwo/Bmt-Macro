import concurrent.futures
import json
import logging
import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = 'https://www.mesrc.net/efacility/{id}/reserve'
FACILITY_IDS = [10, 11, 12, 13]  # All badminton facility IDs
random.shuffle(FACILITY_IDS)  # Shuffle IDs because why not

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

# Create new requests session to improve performance
SESSION = requests.Session()

# Load cookie file
with open('cookies.json', 'r') as fp:
    COOKIES = json.load(fp)
    for cookie in COOKIES:
        # Setting cookie for requests session
        SESSION.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])


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
    response = SESSION.get(URL.format(id=10))
    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.find('input', {'data-drupal-selector': 'edit-efacility-reserve-form-form-token'})
    return element.get('value')


def send_post_request(url, payload):
    """
    Wrapper to send post requests with cookies
    :param url: URL to post to
    :param payload: Payload json data
    :return: HTTP Response
    """
    logging.info(f'Sending post request to Court {payload["efacility_id"] - 9}')
    response = SESSION.post(url, data=payload)
    return response


def main():
    form_token = get_form_token()
    execute_time = datetime.strptime(CONFIG['execute'], '%d/%m/%Y %H:%M:%S')
    delta = execute_time - datetime.now()

    if delta.total_seconds() > 0:  # Not yet execution time so sleep program
        logging.info(f'{delta.total_seconds()} total seconds until execution time. Sleeping program...')
        time.sleep(delta.total_seconds())
        logging.info('Program starting...')
    else:
        logging.warning(f'Execution time has already passed. Starting program immediately...')

    payload = {
        'form_token': form_token,
        'form_id': 'efacility_reserve_form',
        'reserve_date': CONFIG['date'].replace('/', '-'),
        'reserve_start_time': CONFIG['time_start'] * 3600,
        'reserve_end_time': CONFIG['time_end'] * 3600,
        'purpose': CONFIG['purpose'],
        'pax': CONFIG['pax'],
        'op': 'Submit',
        'efacility_id': None,  # To be set when sending the post request
    }

    start_time = time.perf_counter()

    # Create a thread pool executor with 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the POST requests to the executor
        futures = [executor.submit(send_post_request, URL.format(id=fid), dict(payload, efacility_id=fid)) for fid in FACILITY_IDS]

        # wait for all the futures to complete and get their results
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    end_time = time.perf_counter()
    logging.info(f'Sending all post requests took {end_time - start_time}')

    for fid, res in zip(FACILITY_IDS, results):
        logging.info(f'Court {fid - 9} response: {res.status_code}')

    logging.info(f'Visit https://www.mesrc.net/user/0/efacility to check if the court has been booked')
    logging.info('Program Stopping...')


if __name__ == '__main__':
    main()
