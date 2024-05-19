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

from pydantic import BaseModel

wazirx_api_domain = "https://api.wazirx.com"

class WazirxAPIModel(BaseModel):
    ping: str
    server_time: str
    system_status: str
    exchange_info: str
    tickers_24hr: str
    ticker_24hr: str
    order_book_depth: str
    historical_trades: str
    new_order: str
    test_new_order: str
    account_info: str
    funds: str
    create_auth_token: str
    
wzx_api = WazirxAPIModel(
    ping=f"{wazirx_api_domain}/sapi/v1/ping",
    server_time=f"{wazirx_api_domain}/sapi/v1/time",
    system_status=f"{wazirx_api_domain}/sapi/v1/systemStatus",
    exchange_info=f"{wazirx_api_domain}/sapi/v1/exchangeInfo",
    tickers_24hr=f"{wazirx_api_domain}/sapi/v1/tickers/24hr",
    ticker_24hr=f"{wazirx_api_domain}/sapi/v1/ticker/24hr", # ?symbol={symbol}",
    order_book_depth=f"{wazirx_api_domain}/sapi/v1/depth", # ?symbol={symbol}&limit={limit}",
    historical_trades=f"{wazirx_api_domain}/sapi/v1/historicalTrades", # ?symbol={symbol}",
    new_order=f"{wazirx_api_domain}/sapi/v1/order",
    test_new_order=f"{wazirx_api_domain}/sapi/v1/order/test",
    account_info=f"{wazirx_api_domain}/sapi/v1/account",
    funds=f"{wazirx_api_domain}/sapi/v1/funds",
    create_auth_token=f"{wazirx_api_domain}/sapi/v1/create_auth_token"
)