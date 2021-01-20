import asyncio
import json

import httpx

from crypto_dom.binance.market_data.exchange_info import URL


async def _write_binance_assets():

    async with httpx.AsyncClient() as client:
        r = await client.get(URL)
        rjson = r.json()
        symbols_data = rjson["symbols"]
        assets_list = set([k["baseAsset"] for k in symbols_data])

        with open("_definitions_assets.py", "w") as file:
            file.write("# This file is auto-generated\n\n")
            file.write("from typing_extensions import Literal\n\n")
            file.write("ASSET = Literal[\n")
            file.writelines(map(lambda x: f"{4*' '}'{str(x)}',\n", assets_list))
            file.write("]")


if __name__ == "__main__":
    asyncio.run(_write_binance_assets())