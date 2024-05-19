try:
    import time
    import requests
    from dotenv import load_dotenv
    import os
    import hmac
    import hashlib
    import base64
    import json
    import pydantic
except ImportError:
    print("Please install the required modules, try running 'pip install -r requirements.txt'")

load_dotenv()

from pydantic import BaseModel

class APIEndpoints(BaseModel):
    ping: str
    system_status: str
    server_time: str
    exchange_info: str
    order_book: str
    recent_trades: str
    historical_trades: str
    agg_trades: str
    klines: str
    ticker_24hr: str
    ticker_price: str
    book_ticker: str
    new_order: str
    test_new_order: str
    query_order: str
    cancel_order: str
    current_open_orders: str
    all_orders: str
    account_information: str
    account_trade_list: str
    all_coins_information: str
    daily_account_snapshot: str
    disable_fast_withdraw_switch: str
    enable_fast_withdraw_switch: str
    withdraw: str
    deposit_history: str
    withdraw_history: str
    create_listen_key: str
    keepalive_listen_key: str
    close_listen_key: str

wzx_api = APIEndpoints(
    ping="https://api.wazirx.com/sapi/v1/ping",
    system_status="https://api.wazirx.com/sapi/v1/systemStatus",
    server_time="https://api.wazirx.com/sapi/v1/time",
    exchange_info="https://api.wazirx.com/sapi/v1/exchangeInfo",
    order_book="https://api.wazirx.com/sapi/v1/depth?symbol={symbol}&limit={limit}",
    recent_trades="https://api.wazirx.com/sapi/v1/trades?symbol={symbol}&limit={limit}",
    historical_trades="https://api.wazirx.com/sapi/v1/historicalTrades?symbol={symbol}&limit={limit}&fromId={fromId}",
    agg_trades="https://api.wazirx.com/sapi/v1/aggTrades?symbol={symbol}&fromId={fromId}&startTime={startTime}&endTime={endTime}&limit={limit}",
    klines="https://api.wazirx.com/sapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}&startTime={startTime}&endTime={endTime}",
    ticker_24hr="https://api.wazirx.com/sapi/v1/ticker/24hr?symbol={symbol}",
    ticker_price="https://api.wazirx.com/sapi/v1/ticker/price?symbol={symbol}",
    book_ticker="https://api.wazirx.com/sapi/v1/ticker/bookTicker?symbol={symbol}",
    new_order="https://api.wazirx.com/sapi/v1/order",
    test_new_order="https://api.wazirx.com/sapi/v1/order/test",
    query_order="https://api.wazirx.com/sapi/v1/order?symbol={symbol}&orderId={orderId}&origClientOrderId={origClientOrderId}",
    cancel_order="https://api.wazirx.com/sapi/v1/order?symbol={symbol}&orderId={orderId}&origClientOrderId={origClientOrderId}&newClientOrderId={newClientOrderId}",
    current_open_orders="https://api.wazirx.com/sapi/v1/openOrders?symbol={symbol}",
    all_orders="https://api.wazirx.com/sapi/v1/allOrders?symbol={symbol}&orderId={orderId}&startTime={startTime}&endTime={endTime}&limit={limit}",
    account_information="https://api.wazirx.com/sapi/v1/account",
    account_trade_list="https://api.wazirx.com/sapi/v1/myTrades?symbol={symbol}&startTime={startTime}&endTime={endTime}&fromId={fromId}&limit={limit}",
    all_coins_information="https://api.wazirx.com/sapi/v1/capital/config/getall",
    daily_account_snapshot="https://api.wazirx.com/sapi/v1/accountSnapshot?type={type}&startTime={startTime}&endTime={endTime}&limit={limit}",
    disable_fast_withdraw_switch="https://api.wazirx.com/sapi/v1/account/disableFastWithdrawSwitch",
    enable_fast_withdraw_switch="https://api.wazirx.com/sapi/v1/account/enableFastWithdrawSwitch",
    withdraw = "https://api.wazirx.com/sapi/v1/capital/withdraw/apply",
    deposit_history = "https://api.wazirx.com/sapi/v1/capital/deposit/hisrec?coin={coin}&status={status}&startTime={startTime}&endTime={endTime}&limit={limit}",
    withdraw_history = "https://api.wazirx.com/sapi/v1/capital/withdraw/history?coin={coin}&status={status}&startTime={startTime}&endTime={endTime}&limit={limit}",
    create_listen_key = "https://api.wazirx.com/sapi/v1/userDataStream",
    keepalive_listen_key = "https://api.wazirx.com/sapi/v1/userDataStream?listenKey={listenKey}",
    close_listen_key = "https://api.wazirx.com/sapi/v1/userDataStream?listenKey={listenKey}")