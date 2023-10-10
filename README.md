![ezgif-5-df3b4075c4](https://github.com/zad-sixstrings/cakepg/assets/14813374/aaf7cc9d-a526-416a-9c9c-16449ac2a9cd)
# CakePG - A locally run Discord bot for RPG sessions

This is a bot I created for a francophone community having spontaneous RPG sessions in voice chat from time to time. **The bot writes outputs in french** but the code is commented in english, which can help if you need to translate the outputs. I might upload an english version in the future, but this is not a priority at the moment.

I made this bot because I couldn't find any that suited our needs. The existing bots were either too complex or were missing one or more features we needed. Therefore, I will only update it if we need it. I am totally open to suggestions though.

Use it, tweak it, translate it, have fun !

### What it does
It's very simple. It lets people roll dice and manage their character sheets, which only have few data (name, race, class, inventory, gold and level). The character sheets are stored locally in a JSON file. It is aimed at small groups of people. Consider using a proper database for bigger parties.

### Commands
Here's a list of the commands to use with the bot :
- $char (name) | Display character sheet
- $newchar | Create new character sheet
- $delchar (name) | Delete character sheet
- $editchar (name)| Edit existring character sheet
- $roll (NdN) | Roll dice (NdN format)
- $ding (name) | Level-up a character
- $gold (name) (amount) | Add gold to a character
- $loot (name) (item) | Add item to character inventory
- $unloot (name) (item) | Delete item from character inventory
- $help | Display available commands

### Installation & Usage
- Download [latest version](https://github.com/zad-sixstrings/cakepg/releases/tag/1.0)
- Extract files where you want
- Edit ".env-template" with the appropriate information and rename it ".env"
- Run cakepg.py

**Enjoy !**
