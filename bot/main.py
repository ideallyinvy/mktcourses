import os
import discord
from discord.utils import get
from discord.ext import commands
from random import *
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)
TOKEN = os.getenv("DISCORD_TOKEN")

# confirms the bot's online status
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# various events checked when a message is sent
@client.event
async def on_message(message):
    
    # ignores messages from the bot itself
    if message.author == client.user:
        return
    # responds to being mentioned
    if client.user.mentioned_in(message):
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
            await message.channel.send('<:Michael:835690736342007878>')       

    # responds to certified funny keywords with LOL
    if 'POO' in message.content or 'PEE' in message.content:
        await message.channel.send('LOL')

    # @s NBad when monday is mentioned
    if 'monday' in str.lower(message.content):
        await message.channel.send('<@240192847209299969>')

    await client.process_commands(message)

# reposts a random message from the corkboard, ignoring plain text messages
@client.command()
async def cork(ctx):
    print("Called!")
    channel = client.get_channel(836433543726628935)
    print(channel)
    messages = await channel.history(limit=300).flatten()
    rand = randint(0, len(messages)-1)
    randMessage = messages[rand]
    print(randMessage)
    
    if randMessage.content.startswith('http'):
        prev = messages[rand+1]
        for e in prev.embeds:
            await ctx.send(embed=e.copy())
        await ctx.send(randMessage.content)
    else:
        while randMessage.embeds == None and rand !=0:
            rand -= 1
            randMessage = messages[rand]
        for e in randMessage.embeds:
            await ctx.send(embed=e.copy())
        if '<#921529365827821608>' in randMessage.content:
            nextMessage = messages[rand-1]
            if nextMessage.content.startswith('http'):
                await ctx.send(nextMessage.content)

@client.command()
async def mollo(ctx, *args):
    if args == 'jab':
        await ctx.send('https://gfycat.com/embarrassedtenderfinch')

# connecting the script to the bot
if __name__ == "__main__":
    client.run(TOKEN)
