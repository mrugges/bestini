import glob
import re
import os
from collections import defaultdict
from bestini.models import Bot

from icecream import ic

from bestini.config import config

import redis


class RedisConnection:
    r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


class FileLoader:

    patterns = {
        "section": re.compile(r"^\[([\w ]+)]$"),
        "option": re.compile(r"^([\w \/()-]+)=([\w \/|':!${[}\](.)<>]+)"),
        "gem": re.compile(r"((\/Gem\|)(\d+))"),
    }

    ini_path = config["INI_PATH"] or "tests/data/*"

    def parse(self) -> list[Bot]:

        files = glob.glob(pathname=self.ini_path)
        bots = []
        for file in files:
            bot = Bot(name=file)
            with open(file, encoding="utf-8-sig") as f:
                section, option, action, gem = None, None, None, None
                for line in f.readlines():
                    section_matches = re.search(self.patterns["section"], line)
                    if section_matches:
                        section = section_matches[0]
                    else:
                        option_matches = re.search(self.patterns["option"], line)
                        if option_matches:
                            option = option_matches[0]

                            gem_matches = re.search(
                                self.patterns["gem"], option_matches[2]
                            )
                            if gem_matches:
                                gem = int(gem_matches[3])
                                bot.gems[gem] += [option]
                                bot.spells += []

            bots += [bot]
        ic(bots)
        return bots
