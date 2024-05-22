from wazirxapi import *  # required for wzx_api and environment variables to be loaded
from wazirxapi.funcs import (
    get_ticker_24hr,
    show_my_funds,
    show_open_orders,
    cancel_order,
    place_order,
    cancel_all_open_orders,
)
from wazirxapi.helpers import remove_unwanted_keys
from time import sleep
import threading

live_market_data = {}
last_placed_orders = {}


# Thread handler
def update_market_data(symbols):
    while True:
        for symbol in symbols:
            ticker_data = get_ticker_24hr(wzx_api, symbol=symbol)
            # print(f"ticker_data ({symbol})----->>> : {ticker_data}\n\n")
            if ticker_data['symbol']:
                live_market_data.update({
                    ticker_data['symbol']: {
                        'lastPrice': ticker_data['lastPrice'],
                        'bidPrice': ticker_data['bidPrice'],
                        'askPrice': ticker_data['askPrice']
                    }
                })
            else:
                pass
            sleep(3) # to avoid rate limiting
            print(f"Updated live_market_data for {symbol}: {live_market_data[ticker_data['symbol']]}")
        sleep(5)

if __name__ == "__main__":
    symbols = ["xrpinr", "btcinr"]  # List of symbols to track
    # Start the market data tracking in a separate thread
    market_thread = threading.Thread(target=update_market_data, args=(symbols,))
    market_thread.start()
    # sleep(3)
    
    # Main thread continues with other tasks
    # show_my_funds(wzx_api, funds_type="non_zero")
    # show_open_orders(wzx_api, symbol="xrpinr")
    # # cancel_order(wzx_api, symbol="xrpinr", order_id="4482351439")
    # order_details = place_order(
    #     wzx_api, symbol="xrpinr", side="buy", order_type="limit", price=30, quantity=4
    # )
    # placed_order_item = remove_unwanted_keys(order_details)
    # last_placed_orders.update({placed_order_item["symbol"]: placed_order_item})

    # cancel_all_open_orders(wzx_api, symbol="xrpinr")

    # Optionally, join the thread if you need to wait for it to finish
    # Wait for the thread to finish
    market_thread.join()