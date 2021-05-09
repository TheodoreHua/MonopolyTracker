# Monopoly Tracker

[![Actively Developed](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://github.com/TheodoreHua/MaintenanceLevels#actively-developed)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/theodorehuadev@gmail.com)  
[![GitHub issues](https://img.shields.io/github/issues/TheodoreHua/MonopolyTracker)](https://github.com/TheodoreHua/MonopolyTracker/issues)
![GitHub pull requests](https://img.shields.io/github/issues-pr/TheodoreHua/MonopolyTracker)
[![GitHub license](https://img.shields.io/github/license/TheodoreHua/MonopolyTracker)](https://github.com/TheodoreHua/MonopolyTracker/blob/master/LICENSE)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/TheodoreHua/MonopolyTracker)
![GitHub repo size](https://img.shields.io/github/repo-size/TheodoreHua/MonopolyTracker)

A utility program to keep track of a monopoly game. Note that this is NOT a computer version of Monopoly, this only
keeps track of some elements of a physical game.

## Installation and Use

1. Download the latest stable release from the releases page and extract it to a folder of your choice.
2. Run `pip install -r requirements.txt` in the folder where you extracted the files (you might need to do so as
   root/admin).
3. Run `MonopolyTracker.pyw`

## Screenshots

![Main Menu](https://pomf.lain.la/f/kuovh95k.png)

## Config Options

Config file is located at `data/config.ini` in the installation directory.

- ***Money:*** Amount of money players start with.
- ***Go Money:*** Amount of money players get when passing Go.
- ***Name Prefix:*** Default prefix for player names.
- ***Monopoly Set:*** Which monopoly set to use (end of filename, `card_set_us.json` would be `US` in the config option)
- ***Dice Num:*** Number of dice to roll in the dice roll option.
- ***Minimum Prop Similarity:*** Minimum amount of similarity for typo detection in property names.

## Menu Options

- ***Selected Player:*** Current selected player for actions.

---

### Money

#### Add Money

Add a certain amount of money to the current selected player.

#### Subtract Money

Opposite of [Add Money](#add-money).

#### Transfer Money

Transfer money from the current selected player to a player of your choice.

#### Add Go Money

Adds the preset amount of money for passing go (set in [config options](#config-options)).

#### Ignore Bankrupt

Disables showing bankrupt notice for current selected player.

#### Unignore Bankrupt

Opposite of [Ignore Bankrupt](#ignore-bankrupt).

#### Check Net Worth

Calculates the net-worth of the selected player (total of money, properties, and houses).

#### Show Money Graph

Shows a graph with of the selected player's money history.

---

### Property

#### Add Property

Add a property to the current selected player and automatically withdraw the default price.

#### Add Auction Property

[Add Property](#add-property) except you get to specify the price.

#### Transfer Property

Transfers a property to a player of your choice. [*Selected player doesn't matter in this case*]

#### Mortgage Property

Mortgage a property and adds the mortgage price to the player. [*Selected player doesn't matter in this case*]

#### Unmortgage Property

Opposite of [Mortgage Property](#mortgage-property), will automatically withdraw the unmortgage price from the owner.
[*Selected player doesn't matter in this case*]

#### Transfer All Properties

Transfer all properties from selected player to a player of your choice.

#### Add House(s)

Add a house to a property of your choice, owner will automatically pay for it.
[*Selected player doesn't matter in this case*]

#### Sell House(s)

Opposite of [Add House(s)](#add-houses), will refund the owner half the price of the house (as monopoly rules state).
[*Selected player doesn't matter in this case*]

#### Step Property

Have the selected player step on a property and automatically pay the owner of the property the rent.

#### Show Properties

Show a list of properties the selected player owns and how many houses those properties have.

#### Property Data

Show the number of times a property has been stepped on and how much money it's made (on average and in total).
[*Selected player doesn't matter in this case*]

---

### Misc.

#### Jail

Send the current selected player to jail.

#### Unjail

Opposite of [Jail](#jail).

#### Change Name

Change the name of the current selected player.

#### Check Winner

Calculate the current winner based on total money (based on net worth). [*Selected player doesn't matter in this case*]

---

### Non-Gameplay Actions

#### Check Property Info

Shows info about a property. [*Selected player doesn't matter in this case*]

#### Dice Roll

Rolls (a) die/dice, number of dice is determined in the [config options](#config-options). Note that unlike actual dice,
this doesn't favor specific numbers (a pair of actual dice would favor 6), it just decides on a random number from 1 - (
number of dice * 6). [*Selected player doesn't matter in this case*]

## FAQ

### Can I see progress and what's planned for this project?

Yes, there's a public list [here](https://app.gitkraken.com/glo/board/X7UQ_Lw5GgAS1Gj1)

### The program crashed, is there any copy of the data lost?

Kind of, the program saves all data in RAM so unfortunately the program state is not recoverable. However, there is a
file located at `data/last_data.txt` which saves *some* information of the game state. At some point I'm going to make a
feature that can semi-recover the state from the saved data and load it (you can see progress
[here](https://app.gitkraken.com/glo/view/card/b136c23ed17044d1a79b8448c4fd1feb)). Note that when that feature is
implemented, some data will still be lost however most of the important data is saved. Some of what's saved is:

- Player List
- Player Money
- Player Jail State
- Property List
    - Property Name
    - Number of Houses on Property
    - Property Mortgage State

Here's what the file is formatted as:

```
---- (Player Name):
Money: <amount of money here>
--
In Jail: <True/False>
--
Properties:
<Property Name> - <Number of Houses (only if it's a normal property)> - <Mortgage: True/False>
```

For example:

```
---- (Player 1):
Money: 1100
--
In Jail: False
--
Properties:
Boardwalk - 0 - False
```
