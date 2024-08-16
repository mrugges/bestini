from bestini.config import config
import glob
from icecream import ic
import re
from collections import defaultdict


class FileLoader:

    patterns = {
        "section": re.compile(r"^\[([\w ]+)]$"),
        "option": re.compile(r"^([\w \/()-]+)=([\w \/|':!${[}\](.)<>]+)"),
        "gem": re.compile(r"((\/Gem\|)(\d+))"),
    }

    ini_path = config["INI_PATH"] or "tests/data/*"

    bots = {}

    def parse(self):

        files = glob.glob(pathname=self.ini_path)
        ic(files)
        for file in files:
            bot_name = file.split("/")[-1].split("_")[0]
            ic(file)
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
                                gem = gem_matches[3]
                                self.bots.update(
                                    {bot_name: {"gems": {gem: [{"section": section}]}}}
                                )

            ic(self.bots)
