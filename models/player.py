# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

from helpers.gvars import DEFAULTS
from .exceptions import *
from .properties import Property, NormalProperty

NOTFOUND_PROPERTY = "Couldn't find property {} in property list."


class Player:
    def __init__(self, name: str, update_money_func, update_jail_func, update_name_func, bankrupt_err_func):
        self.name = name
        self.in_jail = False
        self.bankrupt_ignored = False
        self._money = DEFAULTS.getint("money")
        self.go_money = DEFAULTS.getint("go_money")
        self._money_history = [self._money]
        self.properties = []
        self.update_money_func = update_money_func
        self.update_jail_func = update_jail_func
        self.update_name_func = update_name_func
        self.bankrupt_err_func = bankrupt_err_func

    def add_money(self, amount: int):
        """Add money to the player"""
        self._money += amount
        self._money_history.append(self._money)
        self.update_money_func()
        self.bankrupt_err_func(self)

    def subtract_money(self, amount: int):
        """Subtract money from the player"""
        self._money -= amount
        self._money_history.append(self._money)
        self.update_money_func()
        self.bankrupt_err_func(self)

    def get_money(self) -> int:
        """Get the amount of money the player has"""
        return self._money

    def add_go_money(self):
        """Adds the default go money amount"""
        self.add_money(self.go_money)

    def transfer_from(self, to: 'Player', amount: int):
        """Transfer money from this player to the specified player"""
        self.subtract_money(amount)
        to.add_money(amount)

    def jail(self):
        """Jail the player"""
        if self.in_jail:
            raise AlreadyChosenValue("The player is already jailed.")
        self.in_jail = True
        self.update_jail_func()

    def unjail(self):
        """Unjail the player"""
        if not self.in_jail:
            raise AlreadyChosenValue("The player is not in jail.")
        self.in_jail = False
        self.update_jail_func()

    def check_bankrupt(self) -> bool:
        """Check whether or not the user is bankrupt"""
        if self.bankrupt_ignored:
            return False
        return self._money <= 0

    def ignore_bankrupt(self):
        """Set bankrupt to ignored"""
        if self.bankrupt_ignored:
            raise AlreadyChosenValue("Bankrupt is already being ignored.")
        self.bankrupt_ignored = True

    def unignore_bankrupt(self):
        if not self.bankrupt_ignored:
            raise AlreadyChosenValue("Bankrupt is not being ignored.")
        self.bankrupt_ignored = False

    def add_property(self, prop: Property):
        """Add a property"""
        self.properties.append(prop)
        prop.set_owner(self)

    def remove_property(self, prop: Property):
        """Remove a property"""
        try:
            self.properties.remove(prop)
            prop.set_owner(None)
        except ValueError as e:
            raise NotFound(NOTFOUND_PROPERTY.format(prop.name)) from e

    def change_name(self, new_name: str):
        """Change the player name"""
        self.update_name_func(self.name, new_name)
        self.name = new_name

    def show_money_graph(self):
        """Show a graph of the player money history"""
        plt.plot(self._money_history)
        plt.title("Money History of {}".format(self.name))
        plt.xlabel("Transactions")
        plt.ylabel("Money")
        plt.show(block=False)

    def show_property_graph(self):
        """Show a graph of which properties was stepped on how many times and how much money they made"""
        price_step_label = [[], [], []]
        # Iterate through all owned properties and add data to list
        for prop in self.properties:
            price_step_label[0].append(prop.stepped_price)
            price_step_label[1].append(prop.times_stepped)
            price_step_label[2].append(prop.name)

        # Create matplotlib figure
        fig = plt.figure()

        # Create subplot and twin y axis
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        # Add axis labels
        ax1.set_xlabel("Property Name")
        ax1.set_ylabel("Times Stepped")
        ax2.set_ylabel("Money Earned")

        # Create NumPy arrays and scalars
        steps = np.array(price_step_label[1])
        m_earned = np.array(price_step_label[0])
        X = np.arange(len(steps))
        width = 0.35

        # Create the bars
        ax1.bar(X - width / 2, steps, width, label="Steps", color="blue")
        ax2.bar(X + width / 2, m_earned, width, label="Money Earned", color="green")

        # Set the xticks and x axis labels
        ax1.set_xticks(X)
        ax1.set_xticklabels(price_step_label[2])

        # Create the legend
        fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax1.transAxes)

        # Show the graph
        plt.show(block=False)

    def get_networth(self) -> int:
        """Get networth of player"""
        networth = self._money
        for prop in self.properties:
            if prop.mortgaged:
                networth -= prop.unmortgage_price
            networth += prop.price
            if type(prop) is NormalProperty:
                networth += prop.houses * prop.house_price
        return networth

    def transfer_all_properties(self, to: 'Player'):
        """Transfer all properties from player to another player"""
        for prop in self.properties:
            to.add_property(prop)
        self.properties = []
