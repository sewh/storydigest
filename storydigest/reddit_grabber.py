import aiohttp
import asyncio
import json
import logging
from html import unescape
from itertools import chain
from random import shuffle
from storydigest.story import Story
from typing import List
from urllib.parse import urlparse


class RedditGrabber(object):
    def __init__(self, subreddits: List[str], amount=10):
        self.subreddits = subreddits
        self.amount = amount

    async def get_stories(self, loop: asyncio.BaseEventLoop=None) \
            -> List[Story]:
        if loop is None:
            loop = asyncio.get_event_loop()

        # Set up aiohttp session
        conn = aiohttp.TCPConnector(verify_ssl=True, limit=5)
        self.session = aiohttp.ClientSession(connector=conn, loop=loop)
        self.headers = {'User-Agent': 'u/steviehy storydigest'}
        tasks = [asyncio.ensure_future(self.get_story(subreddit, loop))
                 for subreddit in self.subreddits]

        """Gather all Story objects, randomise them, and return the
        correct amount per subreddit"""
        results = await asyncio.gather(*tasks)
        self.session.close()
        flat_results = list(chain(*[self.json_to_stories(result)
                                    for result in results]))
        shuffle(flat_results)
        return flat_results[:self.amount]

    async def get_story(self,
                        subreddit: str,
                        loop: asyncio.BaseEventLoop) -> Story:
        logging.getLogger(__name__) \
            .info("Getting https://reddit.com/r/{}.json".format(subreddit))
        async with self.session.get("https://reddit.com/r/{}.json"
                                    .format(subreddit),
                                    headers=self.headers) as resp:
            return await resp.read()

    def json_to_stories(self, _json: bytes) -> List[Story]:
        j = json.loads(_json.decode('utf-8'), encoding='utf-8')
        children = j['data']['children']
        stories = []
        for child in children:
            data = child['data']
            story = Story(url=urlparse(data['url']),
                          comment_url="https://reddit.com/{}"
                          .format(data['permalink']),
                          title=unescape(data['title']))
            stories.append(story)
        return stories
