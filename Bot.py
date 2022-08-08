# Import a module, Python searches for all files that are importable by Python.
import discord, json, os, re
from discord.ext import commands
from flask import Flask
from threading import Thread
idWhitelist = ['ids', 'of', 'whitelisted', 'channels]
auditLogId = '' #Audit log channel id here
               
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

token = 'Token Here'
with open('blacklist.txt', 'r') as file:
  blacklist = file.read().splitlines()
nitroscans = [item for item in blacklist if not(item == '' or item.startswith('#'))]
with open('rickroll.txt', 'r') as file:
  blacklist = file.read().splitlines()
rickroll = [item for item in blacklist if not(item == '' or item.startswith('#'))]
with open('ads.txt', 'r') as file:
  blacklist = file.read().splitlines()
ads = [item for item in blacklist if not(item == '' or item.startswith('#'))]
# This is about Bot Status & Login
@bot.event
async def on_ready():
    print("Bot is Online")

# This is about Link Blocker + Word Blocker
async def linkCheck(message, list, reason):
    if str(message.channel.id) in idWhitelist:
        return True
    elif list != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedLink in list:
            if msg_contains_word(message.content.lower(), bannedLink):
                await message.delete()
                await message.channel.send('***SECURLY BLOCKED***\n*The message has been deleted!*\n**Author:** <@' + str(message.author.id) + '>\n**Reason:** ' + str(reason))
                channel = bot.get_channel(auditLogId)
                await channel.send('***SECURLY BLOCKED***\n*The message has been deleted!*\n**Author:** <@' + str(message.author.id) + '>\n**Message:** ' + str(message.content)+'\n**Channel:** <#'+str(message.channel.id)+'>\n**Reason:** ' + str(reason))
                return True
def msg_contains_word(msg, word):
    if word in msg.lower():
        return True
    else:
        return False
    #return re.search(fr"\b({word})\b", msg) is not None
async def wordCheck(message, reason = 'Banned word: '):
    with open('bannedwords.txt', 'r') as file:
      blacklist = file.read().splitlines()
    list = [item for item in blacklist if not(item == '' or item.startswith('#'))]
    if str(message.channel.id) in idWhitelist:
        return True
    elif list != None and (isinstance(message.channel, discord.channel.DMChannel) == False):
        for bannedLink in list:
            if msg_contains_word(message.content.lower(), bannedLink):
                await message.delete()
                await message.channel.send('***SECURLY BLOCKED***\n*The message has been deleted!*\n**Author:** <@' + str(message.author.id) + '>\n**Reason:** ' + str(reason)+ bannedLink)
                channel = bot.get_channel(auditLogId)#<- same here
                await channel.send('***SECURLY BLOCKED***\n*The message has been deleted!*\n**Author:** <@' + str(message.author.id) + '>\n**Message:** ' + str(message.content)+'\n**Channel:** <#'+str(message.channel.id)+'>\n**Reason:** ' + str(reason) + bannedLink)
                return True
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if await linkCheck(message, nitroscans, 'Nitro Scam') or await linkCheck(message, rickroll, 'Rickroll') or await linkCheck(message, ads, 'Promo/Advertisement'):
        pass
    elif await wordCheck(message):   
        await bot.process_commands(message)
        return
    await bot.process_commands(message)
 bot.run(token)
