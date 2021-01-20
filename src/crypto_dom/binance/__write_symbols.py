import asyncio
import json

import httpx

from crypto_dom.binance.market_data.exchange_info import URL

async def _write_binance_symbols():

    async with httpx.AsyncClient() as client:
        r = await client.get(URL)
        rjson = r.json()
        symbols_data = rjson["symbols"]
        symbols_list = [k["symbol"] for k in symbols_data]

        with open("_data_symbols.json", "w") as file:
            json.dump(symbols_data, file)

        with open("_definitions_symbols.py", "w") as file:
            file.write("# This file is auto-generated\n\n")
            file.write("from typing_extensions import Literal\n\n")
            file.write("SYMBOL = Literal[\n")
            file.writelines(map(lambda x: f"{4*' '}'{str(x)}',\n", symbols_list))
            file.write("]")


if __name__ == "__main__":
    asyncio.run(_write_binance_symbols())