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
    url = f"https://api.wazirx.com/sapi/v1/funds?recvWindow1=5000&timestamp={current_timestamp}&signature={signature}"


    funds_params = {
    'recvWindow1': 5000,
    'timestamp': current_timestamp,
    'signature': signature,
    }
    funds_url = add_query_params(wzx_api.funds, funds_params)

    headers = {
        'X-Api-Key': APIKEY
    }

    response = requests.request("GET", url, headers=headers)

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

    
