**NOTE:** *Still under development. not recommended to be used if you don't understand what you are doing.*

# WazirX API Client Library

This Python library provides a simple interface to interact with the WazirX API, allowing users to perform various operations such as retrieving account funds, checking market data, and executing trades.

## Setup

### Requirements

- Python 3.x
- Requests: `pip install -r requirements.txt`

### Installation

Clone the repository to your local machine and `cd` into it.

### Configuration

Create a `.env` file in the root directory of the project and populate it with your Wazirx API credentials and other necessary environment variables. Here's an example of what the contents might look like:

```
SIGNATURE=your_signature_here
APIKEY=your_api_key_here
SECRET_KEY=your_secret_key_here
RSA_PRIVATE_KEY=your_rsa_private_key_here
```

These keys are used for authenticating requests to the WazirX API.

## Usage

### Importing the Libraries

Start by importing the necessary modules from the library:

```python
from wazirxapi import wzx_api
from wazirxapi.funcs import show_my_funds
```

### Making API Calls

You can make API calls using the functions provided. For example, to retrieve and display your funds, you can use the `show_my_funds` function:

```python
response = show_my_funds(wzx_api, funds_type='all')
print(response)
```

The `funds_type` parameter can be either `'all'` to show all funds or `'non_zero'` to show only funds with a non-zero balance.

## Documentation

to be posted soon...