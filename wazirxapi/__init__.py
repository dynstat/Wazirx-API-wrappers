try:
    import logging
    from logging.handlers import RotatingFileHandler
    import time
    import requests
    from dotenv import load_dotenv
    import os
    import hmac
    import hashlib
    import base64
    import json
    import pydantic
    from pydantic import BaseModel
    from .symbols import assets_set, base_currency_set
    import threading
except ImportError:
    print("Please install the required modules, try running 'pip install -r requirements.txt'")

load_dotenv()

# Configure logging with RotatingFileHandler
log_handler = RotatingFileHandler(
    filename='api.log',
    mode='a',  # Append mode
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=2,  # Keep 2 backup files
    encoding=None,
    delay=0
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s - [Function: %(funcName)s] - [Time: %(asctime)s]'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


# # Configure logging
# logging.basicConfig(
#     filename='api.log',
#     filemode='w',  # 'a' mode appends to the file instead of clearing it
#     level=logging.INFO,
#     format='%(levelname)s - %(message)s - [Function: %(funcName)s] - [Time: %(asctime)s]',
# )

SIGNATURE = os.getenv("SIGNATURE")
APIKEY = os.getenv("APIKEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PRIVATE_KEY = os.getenv("RSA_PRIVATE_KEY")


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

    test_new_order: str
    account_info: str
    funds: str
    open_orders: str
    order: str
    
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
 
    test_new_order=f"{wazirx_api_domain}/sapi/v1/order/test",
    account_info=f"{wazirx_api_domain}/sapi/v1/account",
    
    funds=f"{wazirx_api_domain}/sapi/v1/funds", #Tested
    open_orders=f"{wazirx_api_domain}/sapi/v1/openOrders", #Tested
    order=f"{wazirx_api_domain}/sapi/v1/order", #Tested
    
    create_auth_token=f"{wazirx_api_domain}/sapi/v1/create_auth_token"
)

