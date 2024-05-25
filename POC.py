from wazirxapi import *  # required for wzx_api and environment variables to be loaded
from wazirxapi.funcs import (
    get_ticker_24hr,
    show_my_funds,
    show_open_orders,
    cancel_order,
    place_order,
    cancel_all_open_orders,
    query_order,
)
from wazirxapi.helpers import remove_unwanted_keys
import threading
import time

# Constants
INR_FOR_XRP = 150  # Maximum INR amount to use for XRP
XRP_AMOUNT = 0
STOP_LOSS_THRESHOLD = 0.05  # 5% stop loss
PROFIT_THRESHOLD = 0.02  # 2% profit to re-enter
Y = 0.95  # Multiplier for subsequent buy points

# Global variables
live_market_data = {}
last_placed_orders = {}
latest_top_price = 0
latest_bottom_price = float("inf")
buy_points = []
buy_count = 0


def update_market_data(symbols):
    while True:
        for symbol in symbols:
            ticker_data = get_ticker_24hr(wzx_api, symbol=symbol)
            if ticker_data["symbol"]:
                live_market_data[ticker_data["symbol"]] = {
                    "lastPrice": float(ticker_data["lastPrice"]),
                    "bidPrice": float(ticker_data["bidPrice"]),
                    "askPrice": float(ticker_data["askPrice"]),
                }
            time.sleep(3)  # Avoid rate limiting
        time.sleep(5)
        print(f"Updated live_market_data for {symbol}: {live_market_data[symbol]}")


def trading_bot():
    global XRP_AMOUNT, INR_FOR_XRP, latest_top_price, latest_bottom_price, buy_points, buy_count
    
    while True:
        # Fetch open orders for the symbol "xrpinr"
        open_orders = show_open_orders(wzx_api, symbol="xrpinr")
        if open_orders:
            for order in open_orders:
                # Remove unwanted keys and update the last placed orders dictionary
                last_placed_orders[order["symbol"]] = remove_unwanted_keys(order)

        # Get the current price of XRP in INR from the live market data
        current_price = live_market_data.get("xrpinr", {}).get("lastPrice", 0)

        # If we currently own XRP, check for selling conditions
        if XRP_AMOUNT > 0:
            # Update the latest top price if the current price is higher
            if current_price > latest_top_price:
                latest_top_price = current_price  # Update the latest top price
            # Check if the current price has fallen below the stop loss threshold
            elif current_price <= latest_top_price * (1 - STOP_LOSS_THRESHOLD):
                # Example: latest_top_price = 100, STOP_LOSS_THRESHOLD = 0.05, current_price = 94
                # Place a market sell order at the current bid price
                order_response = place_order(
                    wzx_api,
                    symbol="xrpinr",
                    side="sell",
                    order_type="market",
                    price=live_market_data["xrpinr"]["bidPrice"],
                    quantity=XRP_AMOUNT,
                )
                order_id = order_response.get(
                    "id"
                )  # Extract order ID from the response

                # Check the status of the placed order
                while True:
                    time.sleep(1)
                    order_status = query_order(wzx_api, order_id=order_id)
                    if order_status["status"] == "done":
                        XRP_AMOUNT = 0  # Reset XRP amount after selling
                        latest_bottom_price = current_price  # Update the latest bottom price after selling
                        buy_points = []  # Reset buy points after selling
                        buy_count = 0
                        print("Stop loss triggered, sold XRP")
                        break
                    else:
                        # If the order is not done, cancel it and place a new sell order with the remaining quantity
                        remaining_quantity = float(order_status["origQty"]) - float(
                            order_status["executedQty"]
                        )
                        cancel_order(wzx_api, symbol="xrpinr", order_id=order_id)
                        order_response = place_order(
                            wzx_api,
                            symbol="xrpinr",
                            side="sell",
                            order_type="market",
                            price=live_market_data["xrpinr"]["bidPrice"],
                            quantity=remaining_quantity,
                        )
                        order_id = order_response.get(
                            "id"
                        )  # Update order ID with the new order's ID

        # If we do not own XRP and have INR to spend, check for buying conditions
        if XRP_AMOUNT == 0 and INR_FOR_XRP > 0:
            # Limit the number of buy points to 3
            if buy_count < 3:
                if not buy_points:
                    buy_points.append(current_price)
                else:
                    # Calculate the next buy point using the multiplier Y
                    next_buy_point = buy_points[-1] * Y
                    # Check if the current price is less than or equal to the next buy point
                    if current_price <= next_buy_point:
                        buy_points.append(next_buy_point)
                        # Example: INR_FOR_XRP = 150, current_price = 95, next_buy_point = 90.25
                        # Determine the amount of INR to spend based on the buy order number
                        if buy_count == 0:
                            inr_to_spend = int(0.3 * INR_FOR_XRP)  # 30% for the first order
                        elif buy_count == 1:
                            inr_to_spend = int(0.6 * INR_FOR_XRP)  # 60% for the second order
                        else:
                            inr_to_spend = int(INR_FOR_XRP)  # 100% for the third order

                        # Calculate the quantity to buy based on the determined INR to spend and the current ask price
                        quantity_to_buy = inr_to_spend / live_market_data["xrpinr"]["askPrice"]
                        quantity_to_buy = int(quantity_to_buy)  # Take only the integer part

                        # Place a limit buy order at the current ask price
                        order_details = place_order(
                            wzx_api,
                            symbol="xrpinr",
                            side="buy",
                            order_type="limit",
                            price=live_market_data["xrpinr"]["askPrice"],
                            quantity=quantity_to_buy,
                        )
                        # Remove unwanted keys and update the last placed orders dictionary
                        placed_order_item = remove_unwanted_keys(order_details)
                        last_placed_orders.update(
                            {placed_order_item["symbol"]: placed_order_item}
                        )
                        XRP_AMOUNT += quantity_to_buy  # Update the XRP amount after buying
                        INR_FOR_XRP -= quantity_to_buy * live_market_data["xrpinr"]["askPrice"]  # Deduct the spent INR
                        latest_top_price = (
                            current_price  # Reset the latest top price after buying
                        )
                        buy_count += 1
                        print(
                            f"Bought {quantity_to_buy} XRP at {live_market_data['xrpinr']['askPrice']} INR"
                        )

        # If we own XRP and the current price has risen above the profit threshold, sell the XRP
        if XRP_AMOUNT > 0 and current_price >= latest_bottom_price * (
            1 + PROFIT_THRESHOLD
        ):
            # Example: latest_bottom_price = 90, PROFIT_THRESHOLD = 0.03, current_price = 92.7
            # Place a market sell order at the current bid price
            place_order(
                wzx_api,
                symbol="xrpinr",
                side="sell",
                order_type="market",
                price=live_market_data["xrpinr"]["bidPrice"],
                quantity=XRP_AMOUNT,
            )
            XRP_AMOUNT = 0  # Reset XRP amount after selling
            latest_bottom_price = (
                current_price  # Update the latest bottom price after selling
            )
            buy_points = []  # Reset buy points after selling
            buy_count = 0
            print("Sold XRP at profit")

        time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    symbols = ["xrpinr", "btcinr"]
    market_thread = threading.Thread(
        target=update_market_data, args=(symbols,), name="market_thread"
    )
    market_thread.start()

    bot_thread = threading.Thread(target=trading_bot, name="bot_thread")
    bot_thread.start()

    market_thread.join()
    bot_thread.join()
