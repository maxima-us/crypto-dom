import hypothesis
import pydantic

from ohlc import _OhlcReq, _OhlcResp, T_OhlcResp
from asset_pairs import _AssetPairsResp


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
# ASSET PAIRS
#================================================================================

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

