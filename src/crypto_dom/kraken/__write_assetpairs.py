import asyncio
import json

import httpx

from crypto_dom.kraken.market_data.asset_pairs import URL


async def _write_kraken_pairs(folder: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(URL)
        rjson = r.json()
        result = rjson["result"]
        pairs = list(result.keys())
        
        # json data
        with open(f'{folder}_data_assetpairs.json', 'w') as file:
            json.dump(result, file)
        
        # type definition (Literal)
        with open(f'{folder}_definitions_assetpairs.py', 'w') as file:
            file.write("# This file is auto-generated\n\n")
            file.write("from typing_extensions import Literal\n\n")
            file.write("PAIR = Literal[\n")
            file.writelines(map(lambda x: f"{4*' '}'{str(x)}',\n", pairs))
            file.write("]")


if __name__ == "__main__":
    asyncio.run(_write_kraken_pairs())