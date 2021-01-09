# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from difflib import SequenceMatcher
from operator import itemgetter
from typing import List, Union, Tuple

from models import Player
from models.exceptions import *
from models.properties import Property, NormalProperty, Railroad, Utility
from .gvars import CONFIG


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def transfer_money(t_from: Player, t_to: Player, amount: int):
    """Transfer money from a player object to another player object"""
    t_from.transfer_from(t_to, amount)


def transfer_property(t_from: Player, t_to: Player, prop: Property):
    """Transfer a property from a player object to another player object"""
    if not prop.check_owner(t_from):
        raise NotAuthorized(
            "Player {} does not own the property {} and is trying to transfer it.".format(t_from.name, prop.name))
    prop.transfer(t_to)


def transfer_all_properties(t_from: Player, t_to: Player):
    """Transfer all properties from a player object to another player object"""
    for prop in t_from.properties:
        prop.transfer(t_to)


def get_formatted_property_list(player: Player) -> List[str]:
    """Get list of formatted properties of the player"""
    if len(player.properties) == 0:
        return ["None"]
    formatted_properties = []
    for prop in player.properties:
        formatted = prop.name
        if prop.mortgaged:
            formatted += " (Mortgaged)"
        if type(prop) is NormalProperty:
            formatted += ": " + str(prop.houses)
        formatted_properties.append(formatted)
    return formatted_properties


def get_property(property_name: str, card_set: list) -> Tuple[Union[NormalProperty, Railroad, Utility], bool]:
    card_list = []
    for card in card_set:
        if card.name.casefold() == property_name.casefold():
            return card, False
        card_list.append((similar(card.name.casefold(), property_name.casefold()), card))
    highest_card = max(*card_list, key=itemgetter(0))
    if highest_card[0] * 100 >= CONFIG.getint("DEFAULTS", "min_prop_similarity"):
        return highest_card[1], True
    raise NotFound("Couldn't find property {} in property list.".format(property_name))
