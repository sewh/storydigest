import datetime
import jinja2
import logging
from os.path import abspath, join, dirname
from storydigest.config import Output
from storydigest.story import Story
from typing import List


def output(stories: List[Story], _type: Output, config: dict):
    if _type == Output.html:
        logging.info("Outputting HTML.")
        # Load template
        dir_name = dirname(abspath(__file__))
        with open(join(dir_name, "template.html"), 'r') as f:
            template = jinja2.Template(f.read())
        with open(abspath(config['location']), 'w') as f:
            date = datetime.datetime.now().strftime("%d-%m-%y %p")
            f.write(template.render(date=date, stories=stories))
        logging.info("Wrote " + abspath(config['location']))
