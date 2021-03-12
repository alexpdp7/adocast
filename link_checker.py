#!/usr/bin/env python3
import asyncio
import json
import logging
import sys

import aiohttp


async def check_link(session, link):
    try:
        logging.info("checking %s", link["link"])
        async with session.get(link["link"]) as u:
            logging.info("checked %s", link["link"])
            return {"ok": 200 <= u.status < 300, **link}
    except Exception as e:
        logging.error("failed %s %s", link["link"], e)
        return {"ok": False, **link}


async def main():
    logging.basicConfig(level=logging.INFO)
    d = json.load(sys.stdin)
    async with aiohttp.ClientSession() as session:
        async def check_link_session(link):
            return await check_link(session, link)
        checks = await asyncio.gather(*list(map(check_link_session, d)))
    result = {
        "failed": [c for c in checks if not c["ok"]],
        "ok": [c for c in checks if c["ok"]],
    }
    json.dump(result, sys.stdout)
    return 1 if result["failed"] else 0

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    sys.exit(result)
