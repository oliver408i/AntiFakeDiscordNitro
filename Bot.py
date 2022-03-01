# Import a module, Python searches for all files that are importable by Python.
import discord
from discord.ext import commands
import json
import os
import re

# This is about the config -> config.json


bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

token = 'TOKEN HERE'
with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()
nitroscans = [item for item in blacklist if not(item == '' or item.startswith('#'))]
with open('rickroll.txt', 'r') as file:
  blacklist = file.read().splitlines()
rickroll = [item for item in blacklist if not(item == '' or item.startswith('#'))]
# This is about Bot Status & Login
@bot.event
async def on_ready():
    print("Bot is Online")

# This is about Link Blocker + Word Blocker
async def checkMessage(message, list, reason):
    if list != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedLink in list:
            if msg_contains_word(message.content.lower(), bannedLink):
                await message.delete()
                await message.channel.send('***BLOCKED***\n*The message has been deleted!*\n**Author:** <@' + str(message.author.id) + '>\n**Reason:** ' + str(reason))
def msg_contains_word(msg, word):
    if word in msg.lower():
        return True
    else:
        return False
    #return re.search(fr"\b({word})\b", msg) is not None

@bot.event
async def on_message(message):
    await checkMessage(message, nitroscans, 'Nitro Scam')
    await checkMessage(message, rickroll, 'Rickroll')

    await bot.process_commands(message)


bot.run(token)
