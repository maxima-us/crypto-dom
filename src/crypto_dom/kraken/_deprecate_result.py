from typing import Optional, List, Tuple, Union

from pydantic import BaseModel, create_model, ValidationError, validator

from crypto_dom.kraken.errors import ERROR



def _generate_model(result_model: BaseModel, result_data: Union[dict, str]):


    if isinstance(result_data, dict):
        _instance = result_model()
        _success = _instance(**result_data)
    elif isinstance(result_data, str):
        _success = result_model(result_data)
    else:
        raise TypeError

    #! This is hopw we would need to do it for "usertrades" endpoint for ex
    #!  _m1 = result_model()
    #!  _m2 = _m1(**result_data)
    #! Then we pass m2 to Optional of result field
    
    kwargs = {
        "result": (Optional[_success], ...),
        "error": (List[Optional[Tuple[ERROR, ...]]], ...),
    }

    model = create_model(
        "_KrakenResponse",
        **kwargs
    )

    return model


class KrakenResponse:

    def __new__(_cls, result_model: BaseModel, result_data: Union[dict, str]):
        model = _generate_model(result_model, result_data)
        return model



if __name__ == '__main__':


    #!  we will need to change this up, _generate model needs to take a class as first arg and the result dict as a second arg instead of
    #!      and already created instance. Current way to do it will crash when we try to pass models that are passed the entire result dict
    #!      result model needs to be instantiated inside the _generate_model function


    #------------------------------------------------------------
    # OHLC
    #------------------------------------------------------------


    from crypto_dom.kraken.ohlc import OhlcResp

    data = {
        "XXBTZUSD":[
        [1607947200,"19100.8","19123.7","19025.1","19108.2","19076.7","88.36173782",671],
        [1607950800,"19108.2","19195.2","19062.4","19174.3","19151.0","117.93370323",704],
        [1607954400,"19174.4","19215.4","19099.9","19215.4","19153.3","163.81512930",753]],
        "last": 123014050535
    }

    response = {
        "error": [],
        "result": data
    }
    
    response_model = KrakenResponse(OhlcResp, "XXBTZUSD")
    # print("Model", response_model, "\n")
    # print("Fields", response_model.__fields__, "\n")
    # print("Success Fields", ohlc_model.__fields__, "`\n")

    try:
        r= response_model(**response)
        print(r, "\n")
        print("Last", r.result.last)
    except ValidationError as e:
        raise e
    
    
    #------------------------------------------------------------
    # ASSET PAIRS
    #-----------------------------------------------------------
    
    
    from crypto_dom.kraken.asset_pairs import AssetPairsResp
    
    assetpairs = {
        "AAVEETH":
            {"altname":"AAVEETH","wsname":"AAVE\/ETH","aclass_base":"currency","base":"AAVE","aclass_quote":"currency","quote":"XETH","lot":"unit","pair_decimals":4,"lot_decimals":8,"lot_multiplier":1,"leverage_buy":[],"leverage_sell":[],"fees":[[0,0.26],[50000,0.24],[100000,0.22],[250000,0.2],[500000,0.18],[1000000,0.16],[2500000,0.14],[5000000,0.12],[10000000,0.1]],"fees_maker":[[0,0.16],[50000,0.14],[100000,0.12],[250000,0.1],[500000,0.08],[1000000,0.06],[2500000,0.04],[5000000,0.02],[10000000,0]],"fee_volume_currency":"ZUSD","margin_call":80,"margin_stop":40,"ordermin":"0.1"},
        "AAVEEUR":
            {"altname":"AAVEEUR","wsname":"AAVE\/EUR","aclass_base":"currency","base":"AAVE","aclass_quote":"currency","quote":"ZEUR","lot":"unit","pair_decimals":2,"lot_decimals":8,"lot_multiplier":1,"leverage_buy":[],"leverage_sell":[],"fees":[[0,0.26],[50000,0.24],[100000,0.22],[250000,0.2],[500000,0.18],[1000000,0.16],[2500000,0.14],[5000000,0.12],[10000000,0.1]],"fees_maker":[[0,0.16],[50000,0.14],[100000,0.12],[250000,0.1],[500000,0.08],[1000000,0.06],[2500000,0.04],[5000000,0.02],[10000000,0]],"fee_volume_currency":"ZUSD","margin_call":80,"margin_stop":40,"ordermin":"0.1"}
    }

    response = {
        "error": [],
        "result": assetpairs
    }
    
    
    response_model = KrakenResponse(AssetPairsResp, assetpairs)
    print("Model", response_model, "\n")
    print("Fields", response_model.__fields__, "\n")
    # print("Fields", response_model.__fields__, "\n")


    try:
        r = response_model(**response)
        print(r, "\n")
    except ValidationError as e:
        raise e