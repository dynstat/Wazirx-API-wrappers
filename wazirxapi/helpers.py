def add_query_params(api_endpoint: str, query_params: dict) -> str:
    """
    Constructs a complete URL by appending query parameters to the base API endpoint.

    Args:
    api_endpoint (str): The base URL of the API endpoint.
    query_params (dict): A dictionary containing query parameter keys and values.

    Returns:
    str: The complete URL with query parameters.
    """
    # Start with the base API endpoint
    full_url = api_endpoint

    # Check if there are query parameters to append
    if query_params:
        # Append the '?' symbol to start the query string
        full_url += '?'

        # Join each key-value pair in the dictionary into a string formatted as "key=value"
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])

        # Append the query string to the base URL
        full_url += query_string

    return full_url