import hypothesis
import pydantic

from ohlc import _OhlcReq, _OhlcResp, T_OhlcResp
from asset_pairs import _AssetPairsResp
from assets import _AssetsResp
from ticker import _TickerResp
from spread import _SpreadResp
from account_balance import _AccountBalanceResp
from trade_balance import _TradeBalanceResp


#================================================================================
# OHLC
#================================================================================

generictype = T_OhlcResp["XXBTZUSD"]

test = _OhlcResp("XXBTZUSD")


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

model = _SpreadResp("XXBTZUSD")
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

model = _AssetPairsResp()
ap_resp = model(**assetpairs)
print(ap_resp)


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

model = _TickerResp()
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

model = _AssetsResp()
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
@hypothesis.given(hypothesis.strategies.from_type(_OhlcReq))
def test_request(generated: _OhlcReq):

    print (generated)

    request = _OhlcReq(
        pair=generated.pair,
        interval=generated.interval,
        #! since there is no way to test this for now we will leave it at 1
        #! == still doesnt work
        since=1
    )

    assert isinstance(request, _OhlcReq)

# test_request()

