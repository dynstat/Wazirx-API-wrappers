from wazirxapi import * #required for wzx_api and environment variables to be loaded
from wazirxapi.funcs import show_my_funds


if __name__ == "__main__":
    show_my_funds(wzx_api, funds_type="non_zero")

