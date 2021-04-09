from typing_extensions import Literal



# see doc: vscode://vscode.github-authentication/did-authenticate?windowid=1&code=3f542b80a08f6e325f48&state=d2aca957-3df1-4de6-962f-27a18754ec56

SYMBOL = Literal[
    "BTC",
    "ETH",
    "EOS",
    "BCH",
    "LTC",
    "XRP",
    "BSV",
    "ETC",
    "TRX",
    "LINK",

    # supported but not mentionned
    "DOT"
]


EXCHANGE = Literal[
    "Okex",
    "Huobi",
    "Binance",
    "FTX",
    "Bitmex",
    "Bybit",
    "Deribit",
    "BTCMEX",
    "Kraken",
    "Bitfinex",
    "BTSE",
    "Gate"
]