import asyncio
import json

import httpx

from crypto_dom.binance.market_data.exchange_info import URL


async def _write_binance_assets(folder):

    async with httpx.AsyncClient() as client:
        r = await client.get(URL)
        rjson = r.json()
        symbols_data = rjson["symbols"]
        baseassets = set([k["baseAsset"] for k in symbols_data])
        quoteassets = set(k["quoteAsset"] for k in symbols_data)
        assets = baseassets.union(quoteassets)

        with open(f'{folder}_data_assets.json', 'w') as file:
            json.dump(symbols_data, file)
        
        with open(f"{folder}_definitions_assets.py", "w") as file:
            file.write("# This file is auto-generated\n\n")
            file.write("from typing_extensions import Literal\n\n")
            file.write("ASSET = Literal[\n")
            file.writelines(map(lambda x: f"{4*' '}'{str(x)}',\n", assets))
            file.write("]")


if __name__ == "__main__":
    asyncio.run(_write_binance_assets())