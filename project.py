
import time
from datetime import datetime
from functions import load_state, persist_state, request_current_auctions, persist_sold_auctions 

prev_state = load_state()

while True:
    now = datetime.now()
    
    current_state = {}
    update_list = []

    for auction in request_current_auctions():
        if auction['id'] not in prev_state:
            current_state[auction['id']] = {'id': auction['id'], 'item_id': auction['item']['id'], 'bid': auction['bid'], 'buyout': auction['buyout'], 'quantity': auction['quantity'], 'found_at': now, 'sold_at': '', 'time_left': ''}
        else:
            current_state[auction['id']] = prev_state[auction['id']]
            current_state[auction['id']]['bid'] = auction['bid']

        current_state[auction['id']]['time_left'] = auction['time_left']
    
    persist_state(current_state)

    update_list = []
    for id in prev_state:
        auction = prev_state[id]
        if id not in current_state:
            auction['sold_at'] = now
            update_list.append(auction)

    print("{date} - rows updated: {count}".format(date=now.strftime("%Y-%m-%d %H:%i:%s"), count=len(update_list)))
    persist_sold_auctions(update_list)

    prev_state = current_state
    if update_list.length > 0:
        time.sleep(60 * 30)
    else:
        time.sleep(60 * 3)

