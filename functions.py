import os.path
import requests
from clickhouse_driver import Client
import pickle
import os

DUMP_FILE = 'data/data.dump'

client = Client(host='localhost', port=9002)

def load_state():
    if not os.path.isfile(DUMP_FILE):
        return {}
    
    with open(DUMP_FILE, 'rb') as handle:
        return pickle.load(handle) 

def persist_state(state):
    with open(DUMP_FILE, 'wb') as handle:
        pickle.dump(state, handle, protocol=pickle.HIGHEST_PROTOCOL)

def request_current_auctions():
    params = {
        'base_uri': 'https://eu.api.blizzard.com/data/wow/connected-realm', 
        'realm': os.environ['WOW_REALM'], 
        'auction_id': os.environ['WOW_AUCTION_ID'],
        'namespace': os.environ['WOW_NAMESPACE'],
        'token': os.environ['WOW_TOKEN'],
    }
    uri = '{base_uri}/{realm}/auctions/{auction_id}?namespace={namespace}&locale=en_US&access_token={token}'.format(params)
    response = requests.get(uri)

    return response.json()['auctions']

def persist_sold_auctions(update_list):
    client.execute(
        'INSERT INTO wow.auction (id, item_id, bid, buyout, quantity, found_at, sold_at, time_left) VALUES',
        update_list
    )