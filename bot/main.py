import os
import discord
from discord.utils import get
from discord.ext import commands
from random import *
from datetime import datetime
import pytz
intents = discord.Intents.default()
intents.members = True

wffle = commands.Bot(command_prefix = '!', intents = intents)
TOKEN = os.getenv("DISCORD_TOKEN")

# confirms the bot's online status
@wffle.event
async def on_ready():
    print('We have logged in as {0.user}'.format(wffle))

# welcomes new users to its server
@wffle.event
async def on_member_join(member):
    channel = wffle.get_channel(835366700093407255)
    await channel.send("Welcome to my server")

# various events checked when a message is sent
@wffle.event
async def on_message(message):
    
    # ignores messages from the bot itself
    if message.author == wffle.user:
        return

    # responds to being mentioned
    if wffle.user.mentioned_in(message):
        if 'LOL' in message.content:
            roleID = 921612594912059412
            role = message.guild.get_role(roleID)
            print(role)
            toPing = role.members
            print(toPing)
            rand = randint(0, len(toPing)-1)
            randUser = toPing[rand]
            await message.channel.send('LOL <@'+ str(randUser.id) + '>')
        else:
            roleID = 835575488147226674
            role = message.guild.get_role(roleID)
            if role in message.author.roles:
                await message.channel.send(':michal')
            else:
                await message.channel.send('<:Michael:835690736342007878>')       

    # responds to certified funny keywords with LOL
    if 'POO' in message.content or 'PEE' in message.content:
        await message.channel.send('LOL')

    # @s NBad when monday is mentioned
    if 'monday' in str.lower(message.content):
        await message.channel.send('<@240192847209299969>')

    await wffle.process_commands(message)

# reposts a random message from the corkboard, ignoring plain text messages
@wffle.command()
async def cork(ctx):
    channel = wffle.get_channel(836433543726628935)
    messages = await channel.history(limit=500).flatten()
    rand = randint(0, len(messages)-1)
    randMessage = messages[rand]
    
    while randMessage.embeds == None and rand !=0:
        rand -= 1
        randMessage = messages[rand]
    for e in randMessage.embeds:
        await ctx.send(embed=e.copy())

# returns the current time in NST
@wffle.command()
async def invytime(ctx):
    invytime = datetime.now(pytz.timezone('America/St_Johns'))
    await ctx.send(f'The correct time is: {invytime.strftime("%#I:%M %p")}')

# calls up hitbox visuals for Rivals of Aether
@wffle.command()
async def mollo(ctx, arg):
    if arg == 'jab':
        await ctx.send('https://gfycat.com/embarrassedtenderfinch')

# connecting the script to the bot
if __name__ == "__main__":
    wffle.run(TOKEN)
