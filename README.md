# Monopoly Tracker

[![Bug Fixes Only](https://img.shields.io/badge/Maintenance%20Level-Bug%20Fixes%20Only-green.svg)](https://github.com/TheodoreHua/MaintenanceLevels#bug-fixes-only)
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

Config file is located at `installation_directory/data/config.ini`.

- ***Money:*** Amount of money players start with.
- ***Go Money:*** Amount of money players get when passing Go.
- ***Name Prefix:*** Default prefix for player names.
- ***Monopoly Set:*** Which monopoly set to use (end of filename, `card_set_us.json` would be `US` in the config option)
- ***Dice Num:*** Number of dice to roll in the dice roll option.
- ***Minimum Prop Similarity:*** Minimum amount of similarity for typo detection in property names.
