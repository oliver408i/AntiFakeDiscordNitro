# Import a module, Python searches for all files that are importable by Python.
import discord
from discord.ext import commands
import json
import os
import re

# This is about the config -> config.json
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
    pass
else:
    config = {"Token": "", "Prefix": "", "bannedLinks": []}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(config, f)

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

token = configData["Token"]
bannedLinks = configData["bannedLinks"]

# This is about Bot Status & Login
@bot.event
async def on_ready():
    print("Bot is Online")

# This is about Link Blocker + Word Blocker

def msg_contains_word(msg, word):
    return re.search(fr"\b({word})\b", msg) is not None

@bot.event
async def on_message(message):
    messageAuthor = message.author
    if bannedLinks != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedLink in bannedLinks:
            if msg_contains_word(message.content.lower(), bannedLink):
                await message.delete()
    await bot.process_commands(message)


bot.run(token)
