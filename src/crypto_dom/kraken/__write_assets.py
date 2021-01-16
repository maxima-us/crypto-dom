import asyncio
import json

import httpx

from crypto_dom.kraken.assets import URL


async def _write_kraken_assets():
    async with httpx.AsyncClient() as client:
        r = await client.get(URL)
        rjson = r.json()
        result = rjson["result"]
        assets = list(result.keys())

        # json data
        with open('_data_assets.json', 'w') as file:
            json.dump(result, file)

        # type definition (Literal)
        with open('_definitions_assets.py', 'w') as file:
            file.write("# This file is auto-generated\n\n")
            file.write("from typing_extensions import Literal\n\n")
            file.write("ASSET = Literal[\n")
            file.writelines(map(lambda x: f"{4*' '}'{str(x)}',\n", assets))
            file.write("]")


if __name__ == "__main__":
    asyncio.run(_write_kraken_assets())