import json
from enum import Enum
from os.path import abspath
from typing import List


class Output(Enum):
    html = 1


class Config(object):
    def __init__(self,
                 subreddits: List[str],
                 hackernews: bool,
                 output: Output,
                 output_options: dict):
        self.subreddits = subreddits
        self.hackernews = hackernews
        self.output = output
        self.output_options = output_options

    @classmethod
    def from_json(cls, location: str) -> object:
        with open(abspath(location), 'r') as f:
            j = json.load(f)
            output_type = Output[j['output']['type']]
            return Config(j['subreddits'], j['hackernews'],
                          output_type, j['output']['options'])
