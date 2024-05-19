import time
import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
import base64
import json

load_dotenv()

SIGNATURE = os.getenv("SIGNATURE")
APIKEY = os.getenv("APIKEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PRIVATE_KEY = os.getenv("RSA_PRIVATE_KEY")

# Set Current Time
current_timestamp = int(time.time() * 1000)

# Generate Request Payload
query_params = {
    'recvWindow1': '5000',
    'timestamp': current_timestamp
}

# Create the query string
query_string_array = [f"{key}={value}" for key, value in query_params.items()]
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

headers = {
    'X-Api-Key': APIKEY
}

response = requests.request("GET", url, headers=headers)

# response = [{'asset': 'lpt', 'free': '0.00', 'locked': '0.00'}, {'asset': 'jto', 'free': '0.00', 'locked': '0.00'}, {'asset': 'omni', 'free': '0.00', 'locked': '0.00'}, {'asset': 'dgb', 'free': '0.00', 'locked': '0.00'}, {'asset': 'audio', 'free': '0.00', 'locked': '0.00'}, {'asset': 'dego', 'free': '0.00', 'locked': '0.00'}, {'asset': 'nmr', 'free': '0.00', 'locked': '0.00'}, {'asset': 'gmt', 'free': '0.00', 'locked': '0.00'}, {'asset': 'floki', 'free': '0.00', 'locked': '0.00'}, {'asset': 'beamx', 'free': '0.00', 'locked': '0.00'}, {'asset': 'ankr', 'free': '0.00', 'locked': '0.00'}, {'asset': 'mkr', 'free': '0.00', 'locked': '0.00'}, {'asset': 'tlm', 'free': '0.00', 'locked': '0.00'}, {'asset': 'waxp', 'free': '0.00', 'locked': '0.00'}, ...]

# json.loads(response.content)[i]["asset"] == "xrp"

for coin_data in response.json():
    coin_name = coin_data["asset"]
    # if coin_name == "xrp" or coin_name == "inr":
    #     print(f"{coin_name}: free {coin_data['free']}, locked {coin_data['locked']}")
    if float(coin_data["free"]) > 0:
        print(f"{coin_name}: free {coin_data['free']}, locked {coin_data['locked']}")
# print(response.text)

