#########################################
#                                       #
#                CakePG                 #
#                                       #
# The bot for your Discord RPG sessions #
#                                       #
#                     By zad_sixstrings #
# v1.1                                  #
#########################################

import random
import re
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import asyncio

# Set up bot client with intents
description = '''Un bot pour gérer du JDR simple dans les channels Discord'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Game(name="v1.1 - $help")

client = commands.Bot(command_prefix='$', description=description, activity=activity, intents=intents, help_command=None)

# Create a JSON file to store character data
if not os.path.exists('characters.json'):
    with open('characters.json', 'w') as f:
        json.dump({}, f)

# Create a JSON file to store GM data
if not os.path.exists('gm.json'):
    with open('gm.json', 'w') as f:
        json.dump({}, f)

# Command to display a list of commands with brief descriptions, replacing default help command
@client.command(brief='Afficher la liste des commandes.')
async def help(ctx):
    embed = discord.Embed(title='Liste des commandes', description='Voici la liste des commandes disponibles (à taper avec le préfixe "$"):')

    # Sort the commands alphabetically by name
    commands = sorted(client.commands, key=lambda c: c.name)

    for command in commands:
        embed.add_field(name=f"{command.name} {command.signature}", value=command.brief, inline=False)
    await ctx.send(embed=embed)

# Command to set the Game Master
@client.command(brief='Définir un utilisateur comme maître de jeu. *Le MJ doit avoir une feuille de personnage au préalable.*')
async def setgm(ctx, user: discord.User):
    with open('gm.json', 'w') as f:
        json.dump({'gm_id': user.id}, f, indent=4)
    await ctx.send(f"**{user.name}** a été défini comme maître de jeu!")
    print(f"Set GM to {user.name} ({user.id})")  # Logging

# Function to check if the user is the GM
def is_gm():
    async def predicate(ctx):
        with open('gm.json', 'r') as f:
            gm_data = json.load(f)
        gm_id = gm_data.get('gm_id')
        print(f"Checking GM: {gm_id} vs {ctx.author.id}")  # Logging
        return gm_id == ctx.author.id
    return commands.check(predicate)

# Command to unset the Game Master
@client.command(brief='Supprimer le maître de jeu.')
@is_gm()  # This ensures only the current GM can unset the GM role
async def unsetgm(ctx):
    with open('gm.json', 'w') as f:
        json.dump({}, f, indent=4)
    await ctx.send("Le maître de jeu a été supprimé.")
    print("GM role unset")  # Logging

# Command to roll dice
@client.command(brief='Lancer les dés au format NdN.')
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Indiquez un format NdN! Par exemple : $roll 1d20 pour lancer un dé à 20 faces')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    message = f':game_die: {ctx.author.name} a lancé les dés et obtient: **{result}** !'
    await ctx.send(message)

# Command to see character sheet
@client.command(brief='Afficher la feuille de personnage.')
async def char(ctx, name):
    with open("characters.json", "r") as f:
        characters = json.load(f)
        if name in characters:
            character = characters[name]
            inventory_str = ", ".join(character["inventory"]) or "Aucun objet dans l'inventaire"
            sheet_str = f"""
            :troll: *Race* : **{character["race"]}**\n
            :crossed_swords: *Classe* : **{character["class"]}**\n
            :military_medal: *Niveau* : **{character["level"]}**\n
            :handbag: *Inventaire* : **{inventory_str}**\n
            :coin: *Or* : **{character["gold"]}**
            """
            embed = discord.Embed(title=f'{name}', description=sheet_str)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"**{name}** n'existe pas (et c'est peut-être mieux ainsi).")

# Command to list all saved characters
@client.command(brief='Afficher la liste de tous les personnages.')
async def chars(ctx):
    with open("characters.json", "r") as f:
        characters = json.load(f)
        
        if not characters:
            await ctx.send("Il n'y a aucun personnage enregistré.")
            return
        
        embed = discord.Embed(title='Liste des personnages', description='Voici la liste de tous les personnages enregistrés:')
        
        for name, details in characters.items():
            inventory_str = ", ".join(details["inventory"]) or "Aucun objet dans l'inventaire"
            char_str = f"""
            :troll: - {details["race"]}
            :crossed_swords: - {details["class"]}
            :military_medal: - {details["level"]}
            :handbag: - {inventory_str}
            :coin: - {details["gold"]}
            """
            embed.add_field(name=name, value=char_str, inline=False)
        
        await ctx.send(embed=embed)

# Command to create a character sheet
@client.command(brief='Créer une feuille de personnage.')
async def newchar(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send(':label: Entrez le nom de votre personnage:')
    name_msg = await client.wait_for('message', check=check)
    name = name_msg.content

    await ctx.send(':troll: Entrez la race de votre personnage:')
    race_msg = await client.wait_for('message', check=check)
    race = race_msg.content

    await ctx.send(':crossed_swords: Entrez la classe de votre personnage:')
    class_msg = await client.wait_for('message', check=check)
    class_ = class_msg.content

    data = {}
    with open('characters.json', 'r') as f:
        data = json.load(f)

    if name in data:
        await ctx.send(f'Le personnage **{name}** existe déjà.')
        return

    data[name] = {'race': race, 'class': class_, 'level': 1, 'inventory': [], 'gold': 0}
    with open('characters.json', 'w') as f:
        json.dump(data, f, indent=4)

    await ctx.send(f':tada: La feuille de personnage pour **{name}** a été créée! ')

# Command to edit existing character
@client.command(brief='Modifier un personnage existant.')
async def editchar(ctx, name: str):
    # Load character data from file
    with open('characters.json', 'r') as f:
        characters = json.load(f)

    # Check if character exists
    if name not in characters:
        await ctx.send(f"**{name}** n'existe pas!")
        return

    # Prompt user for updated character information
    await ctx.send(f"Modifiez les informations pour **{name}**:")
    await ctx.send(":troll: Quelle est la race du personnage?")
    race = await client.wait_for('message', check=lambda m: m.author == ctx.author)
    await ctx.send(":crossed_swords: Quelle est la classe du personnage?")
    class_ = await client.wait_for('message', check=lambda m: m.author == ctx.author)

    # Update character data
    characters[name]['race'] = race.content
    characters[name]['class'] = class_.content

    # Save updated character data to file
    with open('characters.json', 'w') as f:
        json.dump(characters, f)

    await ctx.send(f":tada: **{name}** a été modifié!")

# Command to delete character
@client.command(brief='Supprimer un personnage.')
@is_gm()
async def delchar(ctx, name: str):
    with open('characters.json', 'r') as f:
        characters = json.load(f)
    
    if name in characters:
        message = await ctx.send(f"Êtes-vous sûr de vouloir yeet **{name}** ? Réagissez avec ✅ pour confirmer ou ❌ pour annuler.")
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and reaction.emoji in ['✅', '❌']
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"Vous n'avez pas réagi à temps. La suppression du personnage **{name}** a été annulée. Même les dieux se sont endormis.")
        else:
            if reaction.emoji == '✅':
                del characters[name]
                await ctx.send(f":ghost: **{name}** a traversé le voile...")
            else:
                await ctx.send(f"**{name}** est passé(e) à ça :pinching_hand: du casse-pipe...")
    else:
        await ctx.send(f"Le personnage **{name}** n'existe pas.")
    
    with open('characters.json', 'w') as f:
        json.dump(characters, f, indent=4)

# Command to level up character
@client.command(brief='Modifie le niveau d\'un personnage.')
@is_gm()
async def ding(ctx, character_name: str, level_up: int = 1):
    # Load the characters from the JSON file
    with open('characters.json', 'r') as f:
        characters = json.load(f)

    # Check if the character exists
    if character_name not in characters:
        await ctx.send(f'Le personnage "{character_name}" n\'existe pas.')
        return

    # Update the character's level
    characters[character_name]['level'] += level_up

    # Save the updated characters to the JSON file
    with open('characters.json', 'w') as f:
        json.dump(characters, f, indent=4)

    # Send a message to confirm the level up
    await ctx.send(f':tada: **{character_name}** est désormais niveau :military_medal:{characters[character_name]["level"]} !')

# Command to add gold to a character
@client.command(brief='Modifie la fortune d\'un personnage.')
@is_gm()
async def gold(ctx, character_name: str, add_gold: int = 1):
    # Load the characters from the JSON file
    with open('characters.json', 'r') as f:
        characters = json.load(f)

    # Check if the character exists
    if character_name not in characters:
        await ctx.send(f'Le personnage "{character_name}" n\'existe pas.')
        return

    # Update the character's fortune
    characters[character_name]['gold'] += add_gold

    # Save the updated characters to the JSON file
    with open('characters.json', 'w') as f:
        json.dump(characters, f, indent=4)

    # Send a message to confirm the added gold
    await ctx.send(f':tada: **{character_name}** possède désormais :coin:**{characters[character_name]["gold"]}** !')

# Command do add items to character inventories
@client.command(brief='Ajoute un objet à l\'inventaire d\'un personnage')
@is_gm()
async def loot(ctx, name, *item):
    item = ' '.join(item)  # join the item name together
    
    # Check if item contains any special characters or accented letters
    if re.search('[^A-Za-z0-9\s]+', item):
        await ctx.send('Désolé, les lettres accentuées, les runes maudites et les caractères spéciaux ne sont pas autorisés.')
        return
    
    with open("characters.json", "r+") as f:
        characters = json.load(f)

        if name in characters:
            characters[name]['inventory'].append(item)
            f.seek(0)
            json.dump(characters, f, indent=4)
            await ctx.send(f":handbag: {item} a été ajouté à l'inventaire de {name}")
        else:
            await ctx.send(f"{name} n'existe pas.")

# Command to delete items from character inventories
@client.command(brief='Supprime un objet de l\'inventaire d\'un personnage')
@is_gm()
async def unloot(ctx, name, *, item):
    with open("characters.json", "r") as f:
        characters = json.load(f)
    
    # convert all item names to lower case for case-insensitive matching
    item = item.lower()
    
    if name in characters and item in map(str.lower, characters[name]['inventory']):
        characters[name]['inventory'].remove(next(x for x in characters[name]['inventory'] if x.lower() == item))
        with open("characters.json", "w") as f:
            json.dump(characters, f, indent=4)
        await ctx.send(f":handbag: {item} a été supprimé de l'inventaire de {name}.")
    else:
        await ctx.send(f"L'objet {item} n'est pas dans l'inventaire de {name}.")

# Event to confirm bot is connected
@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} (user ID {client.user.id})")

# Event to handle errors and send custom messages
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Seul le maître de jeu peut prendre ce genre de décision...")
    else:
        await ctx.send("Une erreur est survenue. Veuillez vérifier votre commande et réessayer.")
        raise error  # Re-raise the error so that other error handlers are not bypassed

# Run the bot
load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))
