import aiohttp
import asyncio
import json
from random import shuffle
from storydigest.story import Story
from typing import List
from urllib.parse import urlparse

class HackernewsGrabber(object):
    def __init__(self, amount=10):
        self.amount = amount

    async def get_stories(self, loop: asyncio.BaseEventLoop=None) \
            -> List[Story]:
        if loop is None:
            loop = asyncio.get_event_loop()

        # Set up aiohttp session
        conn = aiohttp.TCPConnector(verify_ssl=True, limit=5)
        self.session = aiohttp.ClientSession(connector=conn, loop=loop)
        self.headers = {'User-Agent': 'u/steviehy storydigest'}

        top_ids = await self.get_top_ids(loop)
        shuffle(top_ids)
        top_ids = top_ids[:self.amount]

        tasks = [asyncio.ensure_future(self.get_story(_id, loop))
                 for _id in top_ids]

        results = await asyncio.gather(*tasks)
        self.session.close()
        return results

    async def get_top_ids(self, loop: asyncio.BaseEventLoop) -> List[int]:
        top_url = "https://hacker-news.firebaseio.com/v0/" + \
            "topstories.json?print=pretty"
        async with self.session.get(top_url, headers=self.headers) as resp:
            res = await resp.read()
            return json.loads(res.decode())

    async def get_story(self, _id: int, loop: asyncio.BaseEventLoop) -> Story:
        _url = "https://hacker-news.firebaseio.com/v0/item/{}.json" \
            .format(_id)
        comment_url = "https://news.ycombinator.com/item?id={}".format(
            _id
        )
        async with self.session.get(_url, headers=self.headers) as resp:
            res = await resp.read()
            j = json.loads(res.decode())
            if 'url' not in j.keys():
                j['url'] = comment_url
            return Story(url=urlparse(j['url']),
                         comment_url=urlparse(comment_url),
                         title=j['title'])
