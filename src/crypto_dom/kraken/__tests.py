import hypothesis
import pydantic

# public
from crypto_dom.kraken.ohlc import OhlcReq, OhlcResp
from crypto_dom.kraken.asset_pairs import AssetPairsResp
from crypto_dom.kraken.assets import AssetsResp
from crypto_dom.kraken.ticker import TickerResp
from crypto_dom.kraken.spread import SpreadResp

# private
from crypto_dom.kraken.account_balance import _AccountBalanceResp
from crypto_dom.kraken.trade_balance import _TradeBalanceResp
from crypto_dom.kraken.open_orders import _OpenOrdersResp
from crypto_dom.kraken.orders_info import _QueryOrdersResp
from crypto_dom.kraken.user_trades import _TradesHistoryResp


#! IMPORTS HAVE NOT BEEN UPDATED


#================================================================================
# OHLC
#================================================================================


test = OhlcResp("XXBTZUSD")


data1 = {
    "XXBTZUSD":[
       [1607947200,"19100.8","19123.7","19025.1","19108.2","19076.7","88.36173782",671],
       [1607950800,"19108.2","19195.2","19062.4","19174.3","19151.0","117.93370323",704],
       [1607954400,"19174.4","19215.4","19099.9","19215.4","19153.3","163.81512930",753]],
    "last":"number"
}

data2 = {
    "XXBTZUSD":[
       [1607947200,"19100.8","19123.7","19025.1","19108.2","19076.7","88.36173782",671],
       [1607950800,"19108.2","19195.2","19062.4","19174.3","19151.0","117.93370323",704],
       [1607954400,"19174.4","19215.4","19099.9","19215.4","19153.3","163.81512930",753]],
    "last": 123014050535
}

# should be fine
print("\nFirst call", test(**data2))

# should throw error
# print("\nSecond call", test(**data1))


#================================================================================
# SPREAD
#================================================================================

print(40*"-")
print("---- SPREAD")

spread_data = {
    "XXBTZUSD":[
        [1610566166,"35813.40000","35823.90000"],
        [1610566166,"35813.40000","35824.50000"]
    ],
    "last":1610566227
}

model = SpreadResp("XXBTZUSD")
sp_resp = model(**spread_data)
print(sp_resp)

#================================================================================
# ASSET PAIRS
#================================================================================

print(40*"-")
print("---- ASSETPAIRS")

assetpairs = {
    "AAVEETH":
        {"altname":"AAVEETH","wsname":"AAVE\/ETH","aclass_base":"currency","base":"AAVE","aclass_quote":"currency","quote":"XETH","lot":"unit","pair_decimals":4,"lot_decimals":8,"lot_multiplier":1,"leverage_buy":[],"leverage_sell":[],"fees":[[0,0.26],[50000,0.24],[100000,0.22],[250000,0.2],[500000,0.18],[1000000,0.16],[2500000,0.14],[5000000,0.12],[10000000,0.1]],"fees_maker":[[0,0.16],[50000,0.14],[100000,0.12],[250000,0.1],[500000,0.08],[1000000,0.06],[2500000,0.04],[5000000,0.02],[10000000,0]],"fee_volume_currency":"ZUSD","margin_call":80,"margin_stop":40,"ordermin":"0.1"},
    "AAVEEUR":
        {"altname":"AAVEEUR","wsname":"AAVE\/EUR","aclass_base":"currency","base":"AAVE","aclass_quote":"currency","quote":"ZEUR","lot":"unit","pair_decimals":2,"lot_decimals":8,"lot_multiplier":1,"leverage_buy":[],"leverage_sell":[],"fees":[[0,0.26],[50000,0.24],[100000,0.22],[250000,0.2],[500000,0.18],[1000000,0.16],[2500000,0.14],[5000000,0.12],[10000000,0.1]],"fees_maker":[[0,0.16],[50000,0.14],[100000,0.12],[250000,0.1],[500000,0.08],[1000000,0.06],[2500000,0.04],[5000000,0.02],[10000000,0]],"fee_volume_currency":"ZUSD","margin_call":80,"margin_stop":40,"ordermin":"0.1"}
}

model = AssetPairsResp()
ap_resp = model(**assetpairs)
print(ap_resp)


#================================================================================
# OPEN ORDERS
#================================================================================
print(40*"-")
print("---- OPEN ORDERS")


open_orders_resp = {
    "open": {
    "OTCJRA-SZYUP-LBLOTQ": {
        "refid": None,
        "userref": 0,
        "status": "open",
        "opentm": 1587243440.5982,
        "starttm": 0,
        "expiretm": 0,
        "descr": {
        "pair": "ETHUSD",
        "type": "buy",
        "ordertype": "limit",
        "price": "98.58",
        "price2": "0",
        "leverage": "none",
        "order": "buy 2.34154630 ETHUSD @ limit 98.58",
        "close": ""
        },
        "vol": "2.34154630",
        "vol_exec": "0.00000000",
        "cost": "0.00000",
        "fee": "0.00000",
        "price": "0.00000",
        "stopprice": "0.00000",
        "limitprice": "0.00000",
        "misc": "",
        "oflags": "fciq"
    },

    "OS5GER-FI6DI-VWXUD4": {
        "refid": None,
        "userref": 0,
        "status": "open",
        "opentm": 1587242256.38,
        "starttm": 0,
        "expiretm": 0,
        "descr": {
        "pair": "ETHUSD",
        "type": "buy",
        "ordertype": "limit",
        "price": "130.34",
        "price2": "0",
        "leverage": "none",
        "order": "buy 5.00000000 ETHUSD @ limit 130.34",
        "close": ""
        },
        "vol": "5.00000000",
        "vol_exec": "0.00000000",
        "cost": "0.00000",
        "fee": "0.00000",
        "price": "0.00000",
        "stopprice": "0.00000",
        "limitprice": "0.00000",
        "misc": "",
        "oflags": "fciq"
    },

    "O5TYA6-EC2HN-KJ65ZG": {
        "refid": None,
        "userref": 0,
        "status": "open",
        "opentm": 1587240556.5647,
        "starttm": 0,
        "expiretm": 0,
        "descr": {
        "pair": "ETHUSD",
        "type": "buy",
        "ordertype": "limit",
        "price": "130.00",
        "price2": "0",
        "leverage": "none",
        "order": "buy 5.00000000 ETHUSD @ limit 130.00",
        "close": ""
        },
        "vol": "5.00000000",
        "vol_exec": "0.00000000",
        "cost": "0.00000",
        "fee": "0.00000",
        "price": "0.00000",
        "stopprice": "0.00000",
        "limitprice": "0.00000",
        "misc": "",
        "oflags": "fciq"
    }}
}

model = _OpenOrdersResp()
opo_resp = model(**open_orders_resp)
print(opo_resp)



#================================================================================
# QUERY ORDER INFO
#================================================================================
print(40*"-")
print("---- ORDER INFO")

model = _QueryOrdersResp()
oinf = model (**(open_orders_resp["open"]))
print(oinf)


#================================================================================
# USER TRADES
#================================================================================
print(40*"-")
print("---- USER TRADES")

utr_data = {
    "trades": {
        "TZ63HS-YBD4M-3RDG7H": {
            "ordertxid": "OXXRD7-L67OU-QWHJEZ",
            "postxid": "TKH1SE-M7IF3-CFI4LT",
            "pair": "XETHZUSD",
            "time": 1588032030.4648,
            "type": "buy",
            "ordertype": "market",
            "price": "196.94000",
            "cost": "7395.50936",
            "fee": "14.79101",
            "vol": "37.55209384",
            "margin": "0.00000",
            "misc": ""
        },
        "TESD4J-6G7RU-K5C9TU": {
            "ordertxid": "ORZGFF-GENRB-Z20HTV",
            "postxid": "T6HT2W-ER1S7-5MVQGW",
            "pair": "XETHZUSD",
            "time": 1588032024.6599,
            "type": "buy",
            "ordertype": "market",
            "price": "196.93124",
            "cost": "6788.34719",
            "fee": "13.57670",
            "vol": "34.47064696",
            "margin": "1697.08680",
            "misc": "closing"
        },
        "TEF2TE-RRBVG-FLFHG6": {
            "ordertxid": "OL1AHL-OOF5D-V3KKJM",
            "postxid": "TKH0SE-M1IF3-CFI1LT",
            "posstatus": "closed",
            "pair": "XETHZUSD",
            "time": 1585353611.261,
            "type": "sell",
            "ordertype": "market",
            "price": "131.01581",
            "cost": "7401.30239",
            "fee": "17.76313",
            "vol": "56.49167433",
            "margin": "1850.32560",
            "misc": ""
        }
    },
    "count": 3
}

model = _TradesHistoryResp()
utr_resp = model(**utr_data)
print(utr_resp)


#================================================================================
# TICKER
#================================================================================

print(40*"-")
print("---- TICKER")

tickerdata = {
    "XXBTZUSD":
        {"a":["34557.40000","1","1.000"],
        "b":["34557.30000","1","1.000"],
        "c":["34557.40000","0.00278000"],
        "v":["7800.23835878","12026.07036968"],
        "p":["33944.10537","34100.04530"],
        "t":[46558,74999],
        "l":["32349.90000","32349.90000"],
        "h":["35250.00000","35500.00000"],
        "o":"34038.20000"}
}

model = TickerResp()
tk_resp = model(**tickerdata)
print(tk_resp) 


#================================================================================
# ASSETS
#================================================================================
print(40*"-")
print("---- ASSETS")

assets = {
    "AAVE":{"aclass":"currency","altname":"AAVE","decimals":10,"display_decimals":5},
    "ADA":{"aclass":"currency","altname":"ADA","decimals":8,"display_decimals":6},
    "ALGO":{"aclass":"currency","altname":"ALGO","decimals":8,"display_decimals":5},
}

model = AssetsResp()
as_resp = model(**assets)
print(as_resp)


#================================================================================
# ACCOUNT BALANCES
#================================================================================
print(40*"-")
print("---- ACCOUNT BALANCES")

acc_balances = {
    "XBT": 3.5,
    "DOT": 343.5,
    "ETH": 32.535
}


model = _AccountBalanceResp()
acc_b = model(**acc_balances)
print(acc_b)


#================================================================================
# TRADE BALANCES
#================================================================================
print(40*"-")
print("---- TRADE BALANCES")

trd_balances = {
    "eb": 100_000,
    "tb": 90_000,
    "m": 1.34,
    "n": 35355.535,
    "c": 34434,
    "v": 3435.755,
    "e": 346426234,
    "mf": 0,
    "ml": 234
}

model = _TradeBalanceResp()
trd_b = model(**trd_balances)
print(trd_b)


#================================================================================
# HYPOTHESIS
#================================================================================


class User(pydantic.BaseModel):

    name: pydantic.StrictStr
    age: int
    city: str


@hypothesis.given(hypothesis.strategies.from_type(User))
def test_me(person: User):
    user = User(
        name="maximaus",
        age=person.age,
        city=person.city
    )
    assert user.age < 330
    assert isinstance(user, User)


#!!!! constrained types dont work properly, see: https://github.com/samuelcolvin/pydantic/pull/2097#issuecomment-748596129
@hypothesis.given(hypothesis.strategies.from_type(OhlcReq))
def test_request(generated: OhlcReq):

    print (generated)

    request = OhlcReq(
        pair=generated.pair,
        interval=generated.interval,
        #! since there is no way to test this for now we will leave it at 1
        #! == still doesnt work
        since=1
    )

    assert isinstance(request, OhlcReq)

# test_request()

