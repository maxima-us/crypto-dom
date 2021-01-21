import time
from urllib.parse import urlencode
import hashlib
import hmac
import os

from dotenv import load_dotenv
load_dotenv()


class EmptyEnv(Exception):
    pass


def get_keys():
    
    environ = {k: v for k, v in dict(os.environ).items()}
    creds = {k: v for k, v in environ.items() if any(i in k for i in ["API_KEY", "API_SECRET"])}
    print("Env Creds", creds)

    if not creds:
        raise EmptyEnv("Missing credentiels in .env file")

    # we need to match each api-key to its api-secret
    key_pairs = set()
    
    for k, v in creds.items():
        if "KEY" in k:
            # TODO length for api-key is always the same, same for api-secret
            # TODO we should test for the length to make sure the user has pasted the full key
            # print("Length of key/secret", v, len(v))
            pair = (v, creds[k.replace("API_KEY", "API_SECRET")])
            key_pairs.add(pair)

    # print('Returned set', key_pairs)
    
    # returns a set of tuples (key, secret)
    return key_pairs


# see: https://binance-docs.github.io/apidocs/spot/en/#signed-trade-user_data-and-margin-endpoint-security
def auth_signature(url:str, data:dict, *, secret:str):

    sorted_data= sorted([(k, v) for k, v in data.items()], reverse=False)
    print(sorted_data)
    postdata = urlencode(sorted_data)

    signature = hmac.new(
            secret.encode(),
            postdata.encode(),
            hashlib.sha256
        )

    return signature.hexdigest()


def auth_headers(key:str):
    return {
        "X-MBX-APIKEY": key
    }


def auth_timestamp():
    return int(time.time()*10**3)