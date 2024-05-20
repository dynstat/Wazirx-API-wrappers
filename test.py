from wazirxapi import * #required for wzx_api and environment variables to be loaded
from wazirxapi.funcs import show_my_funds, show_open_orders,cancel_order, place_order, cancel_all_open_orders


if __name__ == "__main__":
    show_my_funds(wzx_api, funds_type="non_zero")
    show_open_orders(wzx_api, symbol="xrpinr")
    cancel_order(wzx_api, symbol="xrpinr", order_id="4482351439")
    place_order(wzx_api, symbol="xrpinr", side="buy", order_type="limit", price=30, quantity=4)
    cancel_all_open_orders(wzx_api, symbol="xrpinr")

