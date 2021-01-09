# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import configparser
import json
from os import mkdir
from os.path import isfile, isdir
from typing import List


def get_config() -> configparser.ConfigParser:
    """Get config file as config parser"""
    config = configparser.ConfigParser()
    config.read("data/config.ini")
    return config


def get_defaults() -> configparser.SectionProxy:
    """Get defaults from config file"""
    return get_config()["DEFAULTS"]


def get_card_set() -> List[dict]:
    with open("data/card_set.json", "r") as f:
        return json.load(f)


def assert_data():
    """Create data from default values if it does not already exist and cross check set differences"""
    if not isdir("data"):
        mkdir("data")
    if not isfile("data/config.ini"):
        with open("data/config.ini", "w") as f:
            config = configparser.ConfigParser()
            config.read("defaults/config.ini")
            config.write(f)
    if not isfile("data/card_set.json"):
        with open("data/card_set.json", "w") as f:
            with open("defaults/card_set_{}.json".format(get_defaults()["monopoly_set"].lower()), "r") as cards:
                json.dump(json.load(cards), f, indent=2)
    else:
        with open("data/card_set.json", "r+") as dcs:
            with open("defaults/card_set_{}.json".format(get_defaults()["monopoly_set"].lower()), "r") as dfcs:
                dfcs_data = json.load(dfcs)
                dcs_data = json.load(dcs)
                if dcs_data != dfcs_data:
                    dcs.seek(0)
                    json.dump(dfcs_data, dcs, indent=2)
                    dcs.truncate()
    if not isfile("data/last_data.txt"):
        with open("data/last_data.txt", "w"):
            pass
