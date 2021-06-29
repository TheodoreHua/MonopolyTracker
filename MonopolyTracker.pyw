# ------------------------------------------------------------------------------
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ------------------------------------------------------------------------------

# noinspection PyUnresolvedReferences
import sys
from random import randint
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, showinfo, showerror, askyesno

from ttkSimpleDialog.ttkSimpleDialog import askinteger, askstring

import helpers
from helpers.gvars import *
from models import *
from models.exceptions import *


def exc_hook(exc_class, message, traceback):
    """Global exception handler"""
    helpers.write_error(exc_class, message, traceback)
    if exc_class is TclError:
        pass
    elif exc_class in [AlreadyChosenValue, LimitReached, NotFound, PropertyAlreadyOwned, PropertyNotOwned,
                       NotAuthorized, NoPaymentNeeded]:
        showerror(exc_class.__name__, message)
    else:
        helpers.write_last_data(player_dict)
        sys.__excepthook__(exc_class, message, traceback)
        graceful_exit()


def error_handler(error):
    """Error handler that can be called"""
    if type(error) in [AlreadyChosenValue, LimitReached, NotFound, PropertyAlreadyOwned, PropertyNotOwned,
                       NotAuthorized, NoPaymentNeeded]:
        showerror(type(error).__name__, getattr(error, "message", getattr(error, "args", [repr(error)])[0]))
    else:
        helpers.write_last_data(player_dict)
        raise error


def bankrupt_err(player: Player):
    if player.check_bankrupt() and not player.bankrupt_ignored:
        showwarning("Bankrupt", "{} is bankrupt with ${:,} and ${:,} needed to return to a non-bankrupt state".format(
            player.name, player.get_money(), abs(player.get_money()) + 1))


def update_player_names(old_name: str, new_name: str):
    """Update the names in the different functions of the program"""
    global player_dict
    unordered_player_dict = player_dict.copy()
    for name, val in unordered_player_dict.items():
        del player_dict[name]
        if name == old_name:
            player_dict[new_name] = val
        else:
            player_dict[name] = val
    for widget in money_grid.winfo_children():
        if type(widget) is ttk.Label:
            player_name = widget.cget("text").split(":")[0]
            if player_name == old_name:
                widget.config(text="{}: {:,}".format(new_name, get_player(new_name).get_money()))
    for widget in jail_grid.winfo_children():
        if type(widget) is ttk.Label:
            player_name = widget.cget("text").split(":")[0]
            if player_name == old_name:
                widget.config(text="{}: {}".format(new_name, get_player(new_name).in_jail))
    player_selector.set_menu(new_name, *list(player_dict.keys()))
    current_player.set(new_name)


def update_money_grid():
    for widget in money_grid.winfo_children():
        if type(widget) is ttk.Label:
            player_name = widget.cget("text").split(":")[0]
            new_text = "{}: ${:,}".format(player_name, get_player(player_name).get_money())
            widget.config(text=new_text)
    for widget in networth_grid.winfo_children():
        if type(widget) is ttk.Label:
            player_name = widget.cget("text").split(":")[0]
            new_text = "{}: ${:,}".format(player_name, get_player(player_name).get_networth())
            widget.config(text=new_text)


def update_jail_grid():
    for widget in jail_grid.winfo_children():
        if type(widget) is ttk.Label:
            player_name = widget.cget("text").split(":")[0]
            new_text = "{}: {}".format(player_name, get_player(player_name).in_jail)
            widget.config(text=new_text)


def get_player(player_name: str = None) -> Player:
    """Get Player object from current selected player or provided name"""
    if player_name is None:
        return player_dict[current_player.get()]
    else:
        try:
            return player_dict[player_name]
        except KeyError as e:
            raise NotFound("Could not find player with name " + player_name) from e


def ask_prop(title: str):
    prop_name = askstring(title, "Property Name")
    if prop_name is None or prop_name == "":
        raise NotFound("Property prompt canceled or name blank")
    prop, non_exact = helpers.get_property(prop_name, card_set)
    if non_exact:
        if not askyesno("Non Exact", "Do you wish to proceed with most similar property?\nMost Similar Property: {}\n"
                                     "Entered: {}".format(prop.name, prop_name)):
            raise NotFound("Could not find property {} in property list".format(prop_name))
    return prop


def add_money_prompt():
    money = askinteger("Add Money", "Amount")
    get_player().add_money(money)


def subtract_money_prompt():
    money = askinteger("Subtract Money", "Amount")
    get_player().subtract_money(money)


def transfer_money_prompt():
    t_from = get_player()
    t_to = get_player(askstring("Transfer To", "Player"))
    money = askinteger("Transfer Money", "Amount")
    helpers.transfer_money(t_from, t_to, money)


def add_property_prompt():
    prop = ask_prop("Add Property")
    prop.buy(get_player())


def transfer_property_prompt():
    prop = ask_prop("Transfer Property")
    prop.transfer(get_player())


def mortgage_property_prompt():
    prop = ask_prop("Mortgage Property")
    prop.mortgage()


def unmortgage_property_prompt():
    prop = ask_prop("Unmortgage Property")
    prop.unmortgage()


def add_house_prompt():
    prop = ask_prop("Add House(s)")
    if type(prop) != NormalProperty:
        raise LimitReached("Railroads or Utilities cannot have houses")
    house_num = askinteger("Add House(s)", "Amount")
    prop.add_house(house_num)


def sell_house_prompt():
    prop = ask_prop("Sell House(s)")
    if type(prop) != NormalProperty:
        raise LimitReached("Railroads or Utilities cannot have houses")
    house_num = askinteger("Sell House(s)", "Amount")
    prop.add_house(house_num)


def step_property_prompt():
    prop = ask_prop("Step Property")
    if type(prop) is Utility:
        dice_roll = askinteger("Utility Dice Roll", "Dice Roll")
        prop.step_property(get_player(), dice_roll=dice_roll)
    else:
        # noinspection PyTypeChecker
        prop.step_property(get_player())


def show_property_prompt(player: Player):
    fp_list = helpers.get_formatted_property_list(get_player())
    tl_win = Toplevel()
    tl_win.title("{}'s Properties".format(player.name))
    tl_win.iconbitmap("res/icon.ico")
    tl_win.resizable(0, 0)
    tl_win.bind("<Return>", lambda e: tl_win.destroy())
    tl_win.wm_attributes("-topmost", 1)
    tl_win.wait_visibility()
    tl_win.grab_set()
    scroll_win = helpers.ScrolledFrame(tl_win)
    scroll_win.grid(row=0, column=0)
    largest_width = 0
    for line, line_text in enumerate(fp_list):
        lab = ttk.Label(scroll_win.interior, text=line_text)
        lab.grid(row=line, column=0)
        if lab.winfo_reqwidth() > largest_width:
            largest_width = lab.winfo_reqwidth()
    scroll_win.canvas.config(width=largest_width + 20)
    scroll_win.grid(row=0, column=0)
    cls_btn = ttk.Button(tl_win, text="Close", command=tl_win.destroy)
    cls_btn.grid(row=1, column=0)
    cls_btn.focus_set()


def change_name_prompt():
    new_name = askstring("Change Name", "Name")
    get_player().change_name(new_name)


def check_net_worth_prompt():
    cur_player = get_player()
    showinfo("{}'s Net Worth".format(cur_player.name), "${:,}".format(cur_player.get_networth()))


def add_auction_property_prompt():
    prop = ask_prop("Add Auction Property")
    amount = askinteger("Add Auction Property", "Amount")
    prop.auction_buy(get_player(), amount)


def transfer_all_properties_prompt():
    t_to = get_player(askstring("Transfer To", "Player"))
    get_player().transfer_all_properties(t_to)


def show_winner():
    winner, win_worth, tied = helpers.get_winner(player_dict)
    if tied:
        showinfo("Winner",
                 "{}, and {} tied with a net worth of ${:,}".format(", ".join(winner[:-1]), winner[-1], win_worth))
    else:
        showinfo("Winner", "{} wins with a net worth of ${:,}!".format(winner, win_worth))


def check_property_info_prompt():
    prop = ask_prop("Check Property Info")
    val = prop.get_property_info()
    tl_win = Toplevel()
    tl_win.title("{}".format(prop.name))
    tl_win.iconbitmap("res/icon.ico")
    tl_win.resizable(0, 0)
    tl_win.bind("<Return>", lambda e: tl_win.destroy())
    tl_win.wm_attributes("-topmost", 1)
    tl_win.wait_visibility()
    tl_win.grab_set()
    scroll_win = helpers.ScrolledFrame(tl_win)
    scroll_win.grid(row=0, column=0)
    largest_width = 0
    for line, line_text in enumerate(val.split("\n")):
        # ttk.Label(scroll_win.interior, text=line_text, justify=CENTER).grid(row=line, column=0)
        lab = ttk.Label(scroll_win.interior, text=line_text, justify=CENTER)
        lab.grid(row=line, column=0)
        if lab.winfo_reqwidth() > largest_width:
            largest_width = lab.winfo_reqwidth()
    scroll_win.canvas.config(width=largest_width + 20)
    cls_btn = ttk.Button(tl_win, text="Close", command=tl_win.destroy)
    cls_btn.grid(row=1, column=0)
    cls_btn.focus_set()


def property_average_prompt():
    prop = ask_prop("Property Average")
    showinfo("Property Average", "{} has made ${:,} on average "
                                 "(${:,}, {:,} times stepped)".format(prop.name, prop.get_property_step_average(),
                                                                      prop.stepped_price, prop.times_stepped))


def dice_roll_prompt():
    number_dices = int(DEFAULTS["dice_num"])
    rolled = randint(number_dices, 6 * number_dices)
    showinfo("Dice Roll", str(rolled))


def call_func(func, *args, **kwargs):
    """Call a function with error parsing and pre/post-function actions (if any)"""
    try:
        func(*args, **kwargs)
    except Exception as e:
        helpers.write_error(*sys.exc_info())
        error_handler(e)


def graceful_exit():
    """Perform exit operations"""
    helpers.write_last_data(player_dict)
    main.destroy()
    sys.exit()


# Set global exception handler
sys.excepthook = exc_hook

# Ensure data integrity
helpers.assert_data()

# Get property objects from card set
card_set = helpers.process_card_set(helpers.get_card_set())

# Create and setup tkinter window
main = Tk()
main.title("Monopoly Tracker v" + VERSION)
main.iconbitmap("res/icon.ico")
main.resizable(0, 0)
main.protocol("WM_DELETE_WINDOW", graceful_exit)

# Get number of players
number_players = askinteger("Player Number", "Number of Players")

if number_players < 1 or number_players > 15:
    showerror("Error", "Too many players")
    sys.exit()

# Create player objects
player_dict = {}
for number in range(1, number_players + 1):
    player_dict[DEFAULTS["name_prefix"] + " " + str(number)] = Player("Player " + str(number), update_money_grid,
                                                                      update_jail_grid, update_player_names,
                                                                      bankrupt_err)

# Set default options for widgets
btndopts = {}
btndefopts = {"padx": 4, "sticky": "we", "ipadx": 10}
framedefopts = {"columnspan": 3, "padx": 10, "pady": 10, "ipadx": 10, "ipady": 5, "sticky": "nesw"}

# Create frames
actions = ttk.LabelFrame(main, text="Gameplay Actions")
data_frame = ttk.LabelFrame(main, text="Data")
gameplay_money = ttk.LabelFrame(actions, text="Money")
gameplay_property = ttk.LabelFrame(actions, text="Property")
gameplay_misc = ttk.LabelFrame(actions, text="Misc.")
nongameplay_actions = ttk.LabelFrame(actions, text="Non-Gameplay Actions")
money_grid = ttk.LabelFrame(data_frame, text="Money")
networth_grid = ttk.LabelFrame(data_frame, text="Networth")
jail_grid = ttk.LabelFrame(data_frame, text="Jail")
actions.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
data_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nesw")
data_frame.rowconfigure(0, weight=1)
money_grid.grid(row=1, column=0, **framedefopts)
networth_grid.grid(row=2, column=0, **framedefopts)
jail_grid.grid(row=3, column=0, **framedefopts)
data_frame.rowconfigure(4, weight=1)
gameplay_money.grid(row=1, column=0, **framedefopts)
gameplay_property.grid(row=2, column=0, **framedefopts)
gameplay_misc.grid(row=3, column=0, **framedefopts)
nongameplay_actions.grid(row=4, column=0, **framedefopts)

# Center widgets in frames by putting a buffer/spacer on the leftmost and rightmost columns of each frame
for frame in [money_grid, networth_grid, jail_grid, gameplay_money, gameplay_property, gameplay_misc,
              nongameplay_actions]:
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(4, weight=1)

# Create and place player widgets
current_player = StringVar()
player_selector = ttk.OptionMenu(actions, current_player, list(player_dict.keys())[0], *list(player_dict.keys()))
player_selector.grid(row=0, column=1, columnspan=2, pady=15, sticky="we")
player_selector_label = ttk.Label(actions, text="Selected Player", width=18)
player_selector_label.grid(row=0, column=0, pady=15)

# Money widgets
add_money = ttk.Button(gameplay_money, text="Add Money", command=lambda: call_func(add_money_prompt), **btndopts)
add_money.grid(row=0, column=1, **btndefopts)
subtract_money = ttk.Button(gameplay_money, text="Subtract Money",
                            command=lambda: call_func(subtract_money_prompt), **btndopts)
subtract_money.grid(row=0, column=2, **btndefopts)
transfer_money = ttk.Button(gameplay_money, text="Transfer Money",
                            command=lambda: call_func(transfer_money_prompt), **btndopts)
transfer_money.grid(row=0, column=3, **btndefopts)
add_go_money = ttk.Button(gameplay_money, text="Add Go Money",
                          command=lambda: call_func(get_player().add_go_money), **btndopts)
add_go_money.grid(row=1, column=1, **btndefopts)
ignore_bankrupt = ttk.Button(gameplay_money, text="Ignore Bankrupt",
                             command=lambda: call_func(get_player().ignore_bankrupt), **btndopts)
ignore_bankrupt.grid(row=1, column=2, **btndefopts)
unignore_bankrupt = ttk.Button(gameplay_money, text="Unignore Bankrupt",
                               command=lambda: call_func(get_player().unignore_bankrupt), **btndopts)
unignore_bankrupt.grid(row=1, column=3, **btndefopts)
check_net_worth = ttk.Button(gameplay_money, text="Check Net Worth",
                             command=lambda: call_func(check_net_worth_prompt), **btndopts)
check_net_worth.grid(row=2, column=1, **btndefopts)
show_money_graph = ttk.Button(gameplay_money, text="Show Money Graph",
                              command=lambda: call_func(get_player().show_money_graph), **btndopts)
show_money_graph.grid(row=2, column=2, **btndefopts)

# Property widgets
add_property = ttk.Button(gameplay_property, text="Add Property",
                          command=lambda: call_func(add_property_prompt), **btndopts)
add_property.grid(row=0, column=1, **btndefopts)
add_auction_property = ttk.Button(gameplay_property, text="Add Auction Property",
                                  command=lambda: call_func(add_auction_property_prompt), **btndopts)
add_auction_property.grid(row=0, column=2, **btndefopts)
transfer_property = ttk.Button(gameplay_property, text="Transfer Property",
                               command=lambda: call_func(transfer_property_prompt), **btndopts)
transfer_property.grid(row=0, column=3, **btndefopts)
mortgage_property = ttk.Button(gameplay_property, text="Mortgage Property",
                               command=lambda: call_func(mortgage_property_prompt), **btndopts)
mortgage_property.grid(row=1, column=1, **btndefopts)
unmortgage_property = ttk.Button(gameplay_property, text="Unmortgage Property",
                                 command=lambda: call_func(unmortgage_property_prompt), **btndopts)
unmortgage_property.grid(row=1, column=2, **btndefopts)
transfer_all_properties = ttk.Button(gameplay_property, text="Transfer All Properties",
                                     command=lambda: call_func(transfer_all_properties_prompt), **btndopts)
transfer_all_properties.grid(row=1, column=3, **btndefopts)
add_house = ttk.Button(gameplay_property, text="Add House(s)",
                       command=lambda: call_func(add_house_prompt), **btndopts)
add_house.grid(row=2, column=1, **btndefopts)
sell_house = ttk.Button(gameplay_property, text="Sell House(s)",
                        command=lambda: call_func(sell_house_prompt), **btndopts)
sell_house.grid(row=2, column=2, **btndefopts)
step_property = ttk.Button(gameplay_property, text="Step Property",
                           command=lambda: call_func(step_property_prompt), **btndopts)
step_property.grid(row=2, column=3, **btndefopts)
show_properties = ttk.Button(gameplay_property, text="Show Properties",
                             command=lambda: call_func(show_property_prompt, get_player()), **btndopts)
show_properties.grid(row=3, column=1, **btndefopts)
property_average = ttk.Button(gameplay_property, text="Property Data",
                              command=lambda: call_func(property_average_prompt), **btndopts)
property_average.grid(row=3, column=2, **btndefopts)

# Misc. Widgets
jail = ttk.Button(gameplay_misc, text="Jail", command=lambda: call_func(get_player().jail), **btndopts)
jail.grid(row=0, column=1, **btndefopts)
unjail = ttk.Button(gameplay_misc, text="Unjail", command=lambda: call_func(get_player().unjail), **btndopts)
unjail.grid(row=0, column=2, **btndefopts)
change_name = ttk.Button(gameplay_misc, text="Change Name",
                         command=lambda: call_func(change_name_prompt), **btndopts)
change_name.grid(row=0, column=3, **btndefopts)
check_winner = ttk.Button(gameplay_misc, text="Check Winner", command=lambda: call_func(show_winner), **btndopts)
check_winner.grid(row=1, column=1, **btndefopts)

# Non-Gameplay Widgets
check_property_info = ttk.Button(nongameplay_actions, text="Check Property Info",
                                 command=lambda: call_func(check_property_info_prompt), **btndopts)
check_property_info.grid(row=0, column=1, **btndefopts)
dice_roll = ttk.Button(nongameplay_actions, text="Dice Roll", command=lambda: call_func(dice_roll_prompt), **btndopts)
dice_roll.grid(row=0, column=2, **btndefopts)

# Fill in money and jail frames
row = 0
column = 1
for player in player_dict.values():
    ttk.Label(money_grid, text="{}: ${:,}".format(player.name, player.get_money())).grid(row=row, column=column,
                                                                                         padx=15, pady=5)
    ttk.Label(networth_grid, text="{}: ${:,}".format(player.name, player.get_networth())).grid(row=row, column=column,
                                                                                               padx=15, pady=5)
    ttk.Label(jail_grid, text="{}: {}".format(player.name, player.in_jail)).grid(row=row, column=column, padx=15,
                                                                                 pady=5)
    if column == 3:
        column = 1
        row += 1
    else:
        column += 1
del row, column, player

main.mainloop()
