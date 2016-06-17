import asyncio
import argparse
import logging
from itertools import chain
from storydigest.config import Config
from storydigest.hackernews_grabber import HackernewsGrabber
from storydigest.output import output
from storydigest.reddit_grabber import RedditGrabber
from storydigest.story import Story
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Get new stories!")
    parser.add_argument('-c', '--config',
                        help='Configuration JSON file.',
                        required=True)
    return parser.parse_args()


async def get_stories(config: Config) -> List[Story]:
    tasks = []
    if len(config.subreddits) > 0:
        logging.getLogger(__name__).info("Getting subreddits...")
        r = RedditGrabber(config.subreddits)
        tasks.append(asyncio.ensure_future(r.get_stories()))

    if config.hackernews:
        logging.getLogger(__name__).info("Getting hackernews...")
        h = HackernewsGrabber()
        tasks.append(asyncio.ensure_future(h.get_stories()))

    results = await asyncio.gather(*tasks)

    return list(chain(*results))


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    config = Config.from_json(args.config)
    logging.getLogger(__name__).info("Starting storydigest.")
    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(get_stories(config))
    logging.getLogger(__name__).info("Got all stories.")

    output(results, config.output, config.output_options)

if __name__ == '__main__':
    main()
