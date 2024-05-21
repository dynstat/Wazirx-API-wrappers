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

live_market_data = {}
last_placed_orders = {}

if __name__ == "__main__":

    while True:
        ticker_data = get_ticker_24hr(wzx_api, symbol="xrpinr")
        print(ticker_data)
        sleep(5)

    show_my_funds(wzx_api, funds_type="non_zero")
    show_open_orders(wzx_api, symbol="xrpinr")
    # cancel_order(wzx_api, symbol="xrpinr", order_id="4482351439")
    order_details = place_order(
        wzx_api, symbol="xrpinr", side="buy", order_type="limit", price=30, quantity=4
    )
    placed_order_item = remove_unwanted_keys(order_details)
    last_placed_orders.update({placed_order_item["symbol"]: placed_order_item})

    cancel_all_open_orders(wzx_api, symbol="xrpinr")
