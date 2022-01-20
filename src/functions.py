import os.path
import requests
from clickhouse_driver import Client
import pickle
import os
import time


DUMP_FILE = '/app/data/data.dump'

client = Client(host='clickhouse', user=os.environ['CLICKHOUSE_USER'], password=os.environ['CLICKHOUSE_PASSWORD'])

def load_state():
    if not os.path.isfile(DUMP_FILE):
        return {}
    
    with open(DUMP_FILE, 'rb') as handle:
        return pickle.load(handle) 

def persist_state(state):
    with open(DUMP_FILE, 'wb') as handle:
        pickle.dump(state, handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_token():
    response = requests.post('https://eu.battle.net/oauth/token', data={'grant_type': 'client_credentials'}, auth=(os.environ['WOW_CLIENT'], os.environ['WOW_SECRET']))

    print(response.status_code)
    print(response.content)

    return response.json()['access_token']

def request_current_auctions():
    params = {
        'base_uri': 'https://eu.api.blizzard.com/data/wow/connected-realm', 
        'realm': os.environ['WOW_REALM'], 
        'auction_id': os.environ['WOW_AUCTION_ID'],
        'namespace': os.environ['WOW_NAMESPACE']
        # 'token': get_token()
    }

    uri = '{base_uri}/{realm}/auctions/{auction_id}?namespace={namespace}&locale=en_US'.format(**params)
    
    try:
        response = requests.get(uri, headers={'Authorization': 'Bearer {}'.format(get_token())})

        return response.json()['auctions']

    except requests.exceptions.JSONDecodeError as e:
        print(response.status_code)
        print(response.content)
        time.sleep(60 * 3)
        

    # return []

def persist_sold_auctions(update_list):
    client.execute(
        'INSERT INTO wow.auction (id, item_id, bid, buyout, quantity, found_at, sold_at, time_left) VALUES',
        update_list
    )