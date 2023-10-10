![ezgif-5-df3b4075c4](https://github.com/zad-sixstrings/cakepg/assets/14813374/aaf7cc9d-a526-416a-9c9c-16449ac2a9cd)
# CakePG
## Discord bot for RPG sessions

This is a bot I created for a francophone community having spontaneous RPG sessions in voice chat from time to time. **The bot writes commands outputs in french** but the code is commented in english. I might upload an english version in the future, but this is not a priority at the moment.

I made this bot because I couldn't find any that suited our needs. The existing bots were either too complex or were missing one or more features we needed. Therefore, I will only update it if we need it. I am totally open to suggestions though.

Use it, tweak it, translate it, have fun !

### What it does
It's very simple and basic. It lets people roll dice and manage their character sheets, which only have few data (name, race, class, inventory, gold). The character sheets are stored locally in a JSON file. It is aimed at small groups of people. Consider using a proper database for bigger parties.

### Commands
Here's a list of the commands to use with the bot :
- $char \<name\> | Display character sheet
- $newchar | Create new character sheet
- $delchar <name> | Delete character sheet
- $editchar <name>| Edit existring character sheet
- $roll <NdN> | Roll dice (NdN format)
- $ding <name> | Level-up a character
- $gold <name> [amount] | Add gold to a character
- $loot <name> [item] | Add item to character inventory
- $unloot <name> [item] | Delete item from character inventory
- $help | Display available commands

### Use a .env file !
The program requires a '.env' file as follows :
```
DISCORD_TOKEN=Your bot application token goes here
DISCORD_GUILD=The name of your server goes here
```

**Enjoy !**
