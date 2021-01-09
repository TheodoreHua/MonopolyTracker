# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import datetime
from operator import itemgetter
from traceback import format_exception
from typing import Tuple, Union, List

from models.exceptions import *
from models.properties import NormalProperty, Railroad, Utility


def get_winner(player_list: dict) -> Tuple[Union[str, List[str]], int, bool]:
    """Get the winner based on net worth of all players"""
    net_worths = {}
    for player in player_list.values():
        net_worths[player] = player.get_networth()
    win_player, win_worth = max(net_worths.items(), key=itemgetter(1))
    tie_list = [win_player.name]
    for player, net_worth in net_worths.items():
        if net_worth == win_worth and player != win_player:
            tie_list.append(player.name)
    if len(tie_list) > 1:
        return tie_list, win_worth, True
    return win_player.name, win_worth, False


def process_card_set(properties: List[dict]) -> List[Union[NormalProperty, Railroad, Utility]]:
    """Return list of property objects from card set list file"""
    property_list = []
    for prop in properties:
        if prop["type"] == "normal":
            property_list.append(NormalProperty(prop["name"], prop["prices"], prop["group"]))
        elif prop["type"] == "railroad":
            property_list.append(Railroad(prop["name"], prop["prices"]))
        elif prop["type"] == "utility":
            property_list.append(Utility(prop["name"], prop["prices"]))
        else:
            raise UnexpectedValue("Unknown property type {} loaded from card set file".format(prop["type"]))
    return property_list


def write_last_data(player_dict: dict):
    """Writes most data from active session to file as backup"""
    with open("data/last_data.txt", "w") as f:
        written_data = ""
        for player in player_dict.values():
            written_data += "---- ({}):\nMoney: {}\n--\nIn Jail: {}\n--\nProperties:\n".format(
                player.name, str(player.get_money()), str(player.in_jail))
            if len(player.properties) == 0:
                written_data += "None\n\n"
            else:
                for prop in player.properties:
                    prop_data = prop.name + " - "
                    if type(prop) is NormalProperty:
                        prop_data += str(prop.houses) + " - "
                    prop_data += str(prop.mortgaged)
                    written_data += prop_data + "\n"
                written_data += "\n"
        f.write(written_data)


def write_error(etype, value, tb):
    """Appends errors (and their traceback) to a logging file"""
    with open("data/errors.txt", "a") as f:
        f.write("---- ({})\n{} - {}\n--\n{}\n".format(
            datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S.%f %Z").strip(), etype.__name__,
            value, "".join(format_exception(etype, value, tb))))
