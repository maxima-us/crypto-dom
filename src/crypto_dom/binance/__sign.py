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
    creds = {k: v for k, v in environ.items() if any(i in k for i in ["BINANCE_API_KEY", "BINANCE_API_SECRET"])}
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
def auth_signature(url: str, data: dict, *, secret: str):

    sorted_data = sorted([(k, v) for k, v in data.items()], reverse=False)
    # print("Sorted data", sorted_data, "\n")
    postdata = urlencode(sorted_data)
    # print("Query String", postdata, "\n")
    signature = hmac.new(
            secret.encode(),
            postdata.encode(),
            hashlib.sha256
        )

    return signature.hexdigest()


def auth_payload(url: str, data: dict, *, secret: str):
    sorted_data = sorted([(k, v) for k, v in data.items()], reverse=False)
    sig = auth_signature(url, data, secret=secret)
    sorted_data.append(("signature", sig))

    print("Query String", sorted_data, "\n")
    return sorted_data 


def auth_headers(key: str):
    return {
        "X-MBX-APIKEY": key
    }


def auth_timestamp():
    return int(time.time()*10**3)