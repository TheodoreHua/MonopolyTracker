# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

from typing import Union

from .exceptions import *


def step_decorator(func):
    def wrapper(self, player, **kwargs):
        self.ownerless_check()
        self.no_payment_check()
        rent = func(self, **kwargs)
        player.transfer_from(self.owner, rent)
        self.times_stepped += 1
        self.stepped_price += rent

    return wrapper


class Property:
    """Represents a Monopoly Property"""

    def __init__(self, name: str, price_data: dict):
        self.name = name
        self.owner = None
        self.price = price_data["property"]
        self.mortgage_price = price_data["mortgage"]
        self.unmortgage_price = price_data["unmortgage"]
        self.mortgaged = False
        self.times_stepped = 0
        self.stepped_price = 0

    def mortgage(self):
        """Mortgage the Property"""
        self.ownerless_check()
        if self.mortgaged:
            raise AlreadyChosenValue("The property is already mortgaged")
        self.mortgaged = True
        self.owner.add_money(self.mortgage_price)

    def unmortgage(self):
        """Unmortgage the Property"""
        self.ownerless_check()
        if not self.mortgaged:
            raise AlreadyChosenValue("The property is not mortgaged")
        self.mortgaged = False
        self.owner.subtract_money(self.unmortgage_price)

    def set_owner(self, player):
        """Set the property owner"""
        self.owner = player

    def check_owner(self, chk) -> bool:
        """Check if a player is this properties owner"""
        return self.owner == chk

    def ownerless_check(self):
        """Check if the owner is none, if yes raise an error"""
        if self.owner is None:
            raise PropertyNotOwned("This function requires this property to be owned")

    def no_payment_check(self):
        """Checks if no payment is needed for the property"""
        if self.mortgaged:
            raise NoPaymentNeeded("The property is mortgaged")
        if self.owner.in_jail:
            raise NoPaymentNeeded("The property owner is in jail")

    def buy(self, player):
        """Buy the property with default price"""
        if self.owner is not None:
            raise PropertyAlreadyOwned(
                "The property is already owned by {}, do you mean to transfer the property?".format(self.owner.name))
        player.add_property(self)
        player.subtract_money(self.price)

    def auction_buy(self, player, amount: int):
        """Buy the property with custom price"""
        if self.owner is not None:
            raise PropertyAlreadyOwned(
                "The property is already owned by {}, do you mean to transfer the property?".format(self.owner.name))
        player.add_property(self)
        player.subtract_money(amount)

    def transfer(self, to):
        """Transfer the property from one player to another"""
        self.ownerless_check()
        self.owner.remove_property(self)
        to.add_property(self)

    def get_property_step_average(self) -> float:
        """Get average money made per step"""
        self.ownerless_check()
        try:
            return self.stepped_price / self.times_stepped
        except ZeroDivisionError:
            return 0

    def get_owner_name(self) -> str:
        """Get name of property owner or None if no one owns it"""
        if self.owner is None:
            return "None"
        else:
            return self.owner.name


class NormalProperty(Property):
    """Represents a Standard Monopoly Property"""

    def __init__(self, name: str, price_data: dict, group: dict):
        super().__init__(name, price_data)
        self.house_price = price_data["buy_house"]
        self.rent = {0: price_data["rent"], 0.5: price_data["street"], 1: price_data["1"], 2: price_data["2"],
                     3: price_data["3"], 4: price_data["4"], 5: price_data["hotel"]}
        self.group = group
        self.houses = 0

    def get_rent(self, houses: Union[int, float]) -> int:
        """Get the rent for x amount of houses in this property"""
        try:
            return self.rent[houses]
        except KeyError as e:
            raise NotFound(
                "Could not find rent for {} houses (0: Normal Rent, 0.5: Street, 1-4: Houses, 5: Hotel)".format(
                    houses)) from e

    def check_colour_set(self) -> bool:
        """Check whether or not the owner has the entire colour set of the property"""
        group_count = 0
        for prop in self.owner.properties:
            if type(prop) is NormalProperty and prop.group["colour"] == self.group["colour"]:
                group_count += 1
        return group_count == self.group["count"]

    def add_house(self, num: int):
        """Add houses to the property"""
        self.ownerless_check()
        if not self.check_colour_set():
            raise LimitReached("You cannot have any houses without a colour set")
        if self.houses + num > 5:
            raise LimitReached("Adding too many houses. You can add at most {} houses".format(5 - self.houses))
        self.houses += num
        self.owner.subtract_money(self.house_price * num)

    def sell_house(self, num: int):
        """Sell houses from the property for the default price"""
        self.ownerless_check()
        if self.houses - num < 0:
            raise LimitReached("Selling too many houses. You can sell at most {} houses".format(self.houses))
        self.houses -= num
        self.owner.add_money((self.house_price / 2) * num)

    @step_decorator
    def step_property(self):
        """Perform the action for when a user steps on the property"""
        if self.check_colour_set() and self.houses == 0:
            return self.get_rent(0.5)
        else:
            return self.get_rent(self.houses)

    def get_property_info(self) -> str:
        """Return formatted string of property info"""
        return """
        Property Name: {}\n
        Owner: {}\n
        Price: {:,}\n
        PPH (Price per House): {:,}\n
        Rent: {:,}\n
        Set Rent: {:,}\n
        1 House: {:,}\n
        2 Houses: {:,}\n
        3 Houses: {:,}\n
        4 Houses: {:,}\n
        Hotel: {:,}\n
        Mortgage Price: {:,}\n
        Unmortgage Price: {:,}\n
        Colour Set: {}\n
        Mortgaged: {}\n
        Houses (0.5: Street, 5: Hotel): {}
        """.format(self.name, self.get_owner_name(), self.price, self.house_price, self.get_rent(0),
                   self.get_rent(0.5), self.get_rent(1), self.get_rent(2), self.get_rent(3),
                   self.get_rent(4), self.get_rent(5), self.mortgage_price, self.unmortgage_price,
                   self.group["colour"].title(), self.mortgaged, self.houses)


class Railroad(Property):
    """Represents a Monopoly Railroad"""

    def __init__(self, name: str, price_data: dict):
        super().__init__(name, price_data)
        self.rent = {1: price_data["1"], 2: price_data["2"], 3: price_data["3"], 4: price_data["4"]}

    def get_rent(self, railroads: int) -> int:
        """Get the rent for x amount of railroads"""
        try:
            return self.rent[railroads]
        except KeyError as e:
            raise NotFound("Could not find rent for {} railroads (1-4: Railroads)".format(str(railroads))) from e

    def get_railroad_count(self) -> int:
        """Get the number of railroads the owner has"""
        set_count = 0
        for prop in self.owner.properties:
            if type(prop) is Railroad:
                set_count += 1
        return set_count

    @step_decorator
    def step_property(self):
        """Perform the action for when a user steps on the property"""
        return self.get_rent(self.get_railroad_count())

    def get_property_info(self) -> str:
        """Return formatted string of property info"""
        return """
        Property Name: {}\n
        Owner: {}\n
        Price: {:,}\n
        1 Railroad: {:,}\n
        2 Railroads: {:,}\n
        3 Railroads: {:,}\n
        4 Railroads: {:,}\n
        Mortgage Price: {:,}\n
        Unmortgage Price: {:,}\n
        Mortgaged: {}
        """.format(self.name, self.get_owner_name(), self.price, self.get_rent(1), self.get_rent(2),
                   self.get_rent(3), self.get_rent(4), self.mortgage_price, self.unmortgage_price,
                   self.mortgaged)


class Utility(Property):
    """Represents a Monopoly Utility"""

    def __init__(self, name: str, price_data: dict):
        super().__init__(name, price_data)
        self.rent = {1: price_data["1"], 2: price_data["2"]}

    def get_multiplier(self, utilities: int) -> int:
        """Get the rent for x amount of utilities"""
        try:
            return self.rent[utilities]
        except KeyError as e:
            raise NotFound("Could not find rent for {} utilities (1-2: Utilities)".format(str(utilities))) from e

    def get_utility_count(self) -> int:
        """Get the number of utilities the owner has"""
        utility_count = 0
        for prop in self.owner.properties:
            if type(prop) is Utility:
                utility_count += 1
        return utility_count

    @step_decorator
    def step_property(self, dice_roll: int):
        """Perform the action for when a user steps on the property"""
        return self.get_multiplier(self.get_utility_count()) * dice_roll

    def get_property_info(self) -> str:
        """Return formatted string of property info"""
        return """
        Property Name: {}\n
        Owner: {}\n
        Price: {:,}\n
        Multiplier for 1 Utility: {:,}\n
        Multiplier for 2 Utilities: {:,}\n
        Mortgage Price: {:,}\n
        Unmortgage Price: {:,}\n
        Mortgaged: {}
        """.format(self.name, self.get_owner_name(), self.price, self.get_multiplier(1),
                   self.get_multiplier(2), self.mortgage_price, self.unmortgage_price, self.mortgaged)
