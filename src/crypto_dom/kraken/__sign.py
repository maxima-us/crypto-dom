from urllib.parse import urlparse, urlencode
import hashlib
import base64
import hmac
import os

from dotenv import load_dotenv
load_dotenv()


class EmptyEnv(Exception):
    pass


def get_keys():
    
    creds = {k: v for k, v in dict(os.environ).items()}
    if creds is None:
        raise EmptyEnv("Missing credentiels in .env file")

    # we need to match each api-key to its api-secret
    key_pairs = set()
    
    for k, v in creds.items():
        if "KEY" in k:
            # TODO length for api-key is always the same (56 iirc), same for api-secret
            # TODO we should test for the length to make sure the user has pasted the full key
            # print("Length of key/secret", v, len(v))
            pair = (v, creds[k.replace("KEY", "SECRET")])
            key_pairs.add(pair)

    print('Returned set', key_pairs)
    # returns a set of tuples (key, secret)
    return key_pairs


# see: https://www.kraken.com/features/api#general-usage
def auth_headers(url, data, *, key, secret):

    if data.get("nonce") is None:
        raise AttributeError("Missing nonce")
    else: 
        nonce = data["nonce"]

    path = getattr(urlparse(url), "path")

    encoded_data = (str(nonce) + urlencode(data)).encode()
    message = path.encode() + hashlib.sha256(encoded_data).digest()

    signature = hmac.new(
            base64.b64decode(secret),
            message,
            hashlib.sha512
        )
    sigdigest = base64.b64encode(signature.digest())


    auth_headers = {
        "API-Key": key,
        "API-Sign": sigdigest.decode()
    }

    return auth_headers