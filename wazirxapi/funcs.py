from wazirxapi import * #required
from wazirxapi.helpers import add_query_params





def show_my_funds(wzx_api: WazirxAPIModel,funds_type : str = "all") -> str:
    """
    Retrieves and displays the funds in a user's WazirX account based on the specified funds type.

    This function constructs a request to the WazirX API to fetch the user's funds. It handles the generation of the necessary signature for API authentication, constructs the request URL, and sends the request. The response is then parsed, and the funds information is printed out.

    Parameters:
        wzx_api (WazirxAPIModel): The API model instance containing API endpoint configurations.
        funds_type (str): Specifies the type of funds to display. 
                          "non_zero" displays only funds with a non-zero balance.
                          "all" displays all funds regardless of balance.

    The function first generates a current timestamp and constructs a dictionary of parameters needed for the API request. It then generates a signature using HMAC (SHA256) if a secret key is available, or RSA signing is assumed to be handled if needed.

    The final API URL is constructed with the necessary parameters and signature. A GET request is sent to the WazirX API with the appropriate headers. Depending on the 'funds_type' parameter, it either prints all funds or only those with a non-zero balance.

    Returns:
       str: Returns and prints the response from the WazirX API.
    """
    
    # Set Current Time
    current_timestamp = int(time.time() * 1000)
    
    # Generate Request Payload
    funds_params_no_signature = {
        'recvWindow1': '5000',
        'timestamp': current_timestamp
    }

    # Create the query string
    query_string_array = [f"{key}={value}" for key, value in funds_params_no_signature.items()]
    payload = "&".join(query_string_array)
    print("Request Payload =", payload)

    # Generate Signature
    if SECRET_KEY:
        signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        print("Signature =", signature)
    else:
        # RSA signing (assuming you have a method to handle this)
        # from Crypto.PublicKey import RSA
        # from Crypto.Signature import pkcs1_15
        # from Crypto.Hash import SHA256

        # key = RSA.import_key(PRIVATE_KEY)
        # h = SHA256.new(payload.encode())
        # signature = pkcs1_15.new(key).sign(h)
        # signature = base64.b64encode(signature).decode()
        # print("Signature =", signature)
        pass

    # Update URL with signature
    # url = f"https://api.wazirx.com/sapi/v1/funds?recvWindow1=5000&timestamp={current_timestamp}&signature={signature}"


    funds_params = {
    'recvWindow1': 5000,
    'timestamp': current_timestamp,
    'signature': signature,
    }
    funds_url = add_query_params(wzx_api.funds, funds_params)

    headers = {
        'X-Api-Key': APIKEY
    }

    response = requests.request("GET", funds_url, headers=headers)

    if funds_type == "non_zero":
        for coin_data in response.json():
            coin_name = coin_data["asset"]
            if float(coin_data["free"]) > 0:
                response = f"{coin_name}: free {coin_data['free']}, locked {coin_data['locked']}"
                print(response)
    else:
        for coin_data in response.json():
            coin_name = coin_data["asset"]
            response = f"{coin_name}: free {coin_data['free']}, locked {coin_data['locked']}"
            print(response)
            
    return response

    
def show_open_orders(wzx_api: WazirxAPIModel, symbol: str) -> list:
    """
    Retrieves and displays the open orders for a specified symbol in a user's WazirX account.

    This function constructs a request to the WazirX API to fetch the user's open orders. It handles the generation of the necessary signature for API authentication, constructs the request URL, and sends the request. The response is then parsed, and the open orders information is printed out.

    Parameters:
        wzx_api (WazirxAPIModel): The API model instance containing API endpoint configurations.
        symbol (str): The trading pair symbol (e.g., 'xrpinr') for which to fetch open orders.

    Returns:
       list: List of open orders for the specified symbol.
    """
    if symbol[:3] not in assets_set and symbol[3:] not in base_currency_set:
        print("Invalid symbol")
        return "Invalid symbol"
    # Set Current Time
    current_timestamp = int(time.time() * 1000)
    
    # Generate Request Payload
    open_orders_params_no_signature = {
        'symbol': symbol,
        'recvWindow': '20000',
        'timestamp': current_timestamp
    }

    # Create the query string
    query_string_array = [f"{key}={value}" for key, value in open_orders_params_no_signature.items()]
    payload = "&".join(query_string_array)
    print("Request Payload =", payload)

    # Generate Signature
    if SECRET_KEY:
        signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        print("Signature =", signature)
   
    # Update URL with signature
    # url = f"https://api.wazirx.com/sapi/v1/openOrders?{payload}&signature={signature}"
    
    open_orders_params = {
       'symbol': symbol,
       'recvWindow': 20000,
       'timestamp': current_timestamp,
       'signature': signature,
    }

    open_orders_url = add_query_params(wzx_api.open_orders, open_orders_params)
    headers = {
        'X-Api-Key': APIKEY
    }

    response = requests.request("GET", open_orders_url, headers=headers)

    # Print and return the response
    print(response.text)
    return json.loads(response.text)



def cancel_order(wzx_api: WazirxAPIModel, symbol: str, order_id: str) -> dict:
    """
    Cancels an order for a specified symbol in a user's WazirX account.

    This function constructs a request to the WazirX API to cancel an order. It handles the generation of the necessary signature for API authentication, constructs the request URL, and sends the request. The response is then parsed, and the cancellation status is printed out.

    Parameters:
        wzx_api (WazirxAPIModel): The API model instance containing API endpoint configurations.
        symbol (str): The trading pair symbol (e.g., 'xrpinr') for which to cancel the order.
        order_id (str): The ID of the order to be canceled.

    Returns:
       str: Returns and prints the response from the WazirX API.
    """
    
    if symbol[:3] not in assets_set and symbol[3:] not in base_currency_set:
        print("Invalid symbol")
        return "Invalid symbol"
    
    # Set Current Time
    current_timestamp = int(time.time() * 1000)
    
    # Generate Request Payload
    cancel_order_params_no_signature = {
        'symbol': symbol,
        'orderId': order_id,
        'recvWindow': '20000',
        'timestamp': current_timestamp
    }

    # Create the query string
    query_string_array = [f"{key}={value}" for key, value in cancel_order_params_no_signature.items()]
    payload = "&".join(query_string_array)
    print("Request Payload =", payload)

    # Generate Signature
    if SECRET_KEY:
        signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        print("Signature =", signature)
   
    # Update URL with signature
    # url = f"https://api.wazirx.com/sapi/v1/order?{payload}&signature={signature}"
    
    cancel_order_params = {
       'symbol': symbol,
       'orderId': order_id,
       'recvWindow': 20000,
       'timestamp': current_timestamp,
       'signature': signature,
    }

    cancel_order_url = add_query_params(wzx_api.order, cancel_order_params)
    headers = {
        'X-Api-Key': APIKEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("DELETE", cancel_order_url, headers=headers, data=payload)

    # Print and return the response
    print(response.text)
    return json.loads(response.text)


def cancel_all_open_orders(wzx_api: WazirxAPIModel, symbol: str) -> list:
    """
    Cancels all open orders for a specified symbol in a user's WazirX account.

    This function constructs a request to the WazirX API to cancel all open orders for a given symbol. It handles the generation of the necessary signature for API authentication, constructs the request URL, and sends the request. The response is then parsed, and the cancellation status is printed out.

    Parameters:
        wzx_api (WazirxAPIModel): The API model instance containing API endpoint configurations.
        symbol (str): The trading pair symbol (e.g., 'xrpinr') for which to cancel all open orders.

    Returns:
       str: Returns and prints the response from the WazirX API.
    """
    
    if symbol[:3] not in assets_set and symbol[3:] not in base_currency_set:
        print("Invalid symbol")
        return "Invalid symbol"
    
    # Set Current Time
    current_timestamp = int(time.time() * 1000)
    
    # Generate Request Payload
    cancel_all_orders_params_no_signature = {
        'symbol': symbol,
        'recvWindow': '20000',
        'timestamp': current_timestamp
    }

    # Create the query string
    query_string_array = [f"{key}={value}" for key, value in cancel_all_orders_params_no_signature.items()]
    payload = "&".join(query_string_array)
    print("Request Payload =", payload)

    # Generate Signature
    if SECRET_KEY:
        signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        print("Signature =", signature)
   
    # Update URL with signature
    # url = f"https://api.wazirx.com/sapi/v1/openOrders?{payload}&signature={signature}"
    
    cancel_all_orders_params = {
       'symbol': symbol,
       'recvWindow': 20000,
       'timestamp': current_timestamp,
       'signature': signature,
    }

    cancel_all_orders_url = add_query_params(wzx_api.open_orders, cancel_all_orders_params)
    headers = {
        'X-Api-Key': APIKEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("DELETE", cancel_all_orders_url, headers=headers, data=payload)

    # Print and return the response
    print(response.text)
    return response.text



def place_order(wzx_api: WazirxAPIModel, symbol: str, side: str, order_type: str, price: float, quantity: float) -> str:
    """
    Places a new order for a specified symbol in a user's WazirX account.

    This function constructs a request to the WazirX API to place a new order. It handles the generation of the necessary signature for API authentication, constructs the request URL, and sends the request. The response is then parsed, and the order status is printed out.

    Parameters:
        wzx_api (WazirxAPIModel): The API model instance containing API endpoint configurations.
        symbol (str): The trading pair symbol (e.g., 'xrpinr') for which to place the order.
        side (str): The side of the order ('buy' or 'sell').
        order_type (str): The type of the order ('limit', 'market', etc.).
        price (float): The price at which to place the order.
        quantity (float): The quantity of the asset to buy or sell.

    Returns:
       str: Returns and prints the response from the WazirX API.
   
    Sample Success Response:
    {
        "id": 4486665821,                  # Unique identifier for the order
        "symbol": "xrpinr",                # Trading pair symbol
        "type": "limit",                   # Type of the order (e.g., limit, market)
        "side": "buy",                     # Side of the order (buy or sell)
        "status": "wait",                  # Current status of the order
        "price": "30",                     # Price at which the order is placed
        "origQty": "4",                    # Original quantity of the order
        "executedQty": "0",                # Quantity of the order that has been executed
        "avgPrice": "0",                   # Average price at which the order has been executed
        "createdTime": 1716228241000,      # Timestamp when the order was created
        "updatedTime": 1716228241000,      # Timestamp when the order was last updated
        "clientOrderId": "706a3a5a-dcde-44b5-be13-a396efffdef7"  # Client-provided unique identifier for the order
    }
    """
    
    # Set Current Time
    current_timestamp = int(time.time() * 1000)
    
    # Generate Request Payload
    order_params_no_signature = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'price': price,
        'quantity': quantity,
        'recvWindow': '10000',
        'timestamp': current_timestamp
    }

    # Create the query string
    query_string_array = [f"{key}={value}" for key, value in order_params_no_signature.items()]
    payload = "&".join(query_string_array)
    print("Request Payload =", payload)

    # Generate Signature
    if SECRET_KEY:
        signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        print("Signature =", signature)
   
    # Update URL with signature
    # url = f"https://api.wazirx.com/sapi/v1/order?{payload}&signature={signature}"
    
    order_params = {
       'symbol': symbol,
       'side': side,
       'type': order_type,
       'price': price,
       'quantity': quantity,
       'recvWindow': 5000,
       'timestamp': current_timestamp,
       'signature': signature,
    }

    order_url = add_query_params(wzx_api.order, order_params)
    headers = {
        'X-Api-Key': APIKEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", order_url, headers=headers, data=payload)

    # Print and return the response
    print(response.text)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None
    

