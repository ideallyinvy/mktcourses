import os
import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from random import *
from datetime import datetime
import pytz
from wonderwords import RandomWord
import asyncio
import json

# multipurpose Discord bot used for a specific friend server involving several dumb inside jokes.
# peruse at your own risk.
# author @mjhancock
# last updated: 1-5-22

# local token file
config = json.load(open('./config.json', 'r'))

# online hosting token
TOKEN = os.getenv("DISCORD_TOKEN")

# set intents
intents = nextcord.Intents.default()
intents.members = True
intents.reactions = True

# initialize bot
wffle = commands.Bot(command_prefix = '!', intents = intents)

# confirms the bot's online status
@wffle.event
async def on_ready():
    print('We have logged in as {0.user}'.format(wffle))

# welcomes new users to its server
@wffle.event
async def on_member_join(member):
    ctx = await wffle.get_context(member)
    async with ctx.typing():
        channel = wffle.get_channel(835366700093407255)
        await asyncio.sleep(0.3)
    await ctx.send("Welcome to my server")

# adds messages to the wall of shame once they reach 5 tomato reacts;
# updates the tomato count as it increases
@wffle.event
async def on_reaction_add(reaction, user):

    message = reaction.message
    author = message.author
    attachments = message.attachments
    channel = wffle.get_channel(921430906412073070)
    reactions = message.reactions
    tomatoCount = 0

    if reaction.emoji != '\N{TOMATO}' or author == user:
        return
    
    for reaction in reactions:
        if reaction.emoji == '\N{TOMATO}':
            tomatoCount = reaction.count
    
    content = ":tomato: **" + str(tomatoCount) + "** <#" + str(message.channel.id) + ">"

    if tomatoCount == 5:
        embed = nextcord.Embed(description=message.content, colour=0xe74c3c)
        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
        source = '[Jump!](' + message.jump_url + ')'
        embed.add_field(name='Source', value=source, inline=False)

        if attachments:
            if attachments[0].content_type.startswith('image'):
                embed.set_image(url=attachments[0].url)
            else:
                if attachments[0].content_type.startswith('video'):
                    attachment = '[' + attachments[0].filename + '](' + attachments[0].url + ')'
                    embed.add_field(name='Attachment', value=attachment)

        embed.timestamp = message.created_at
        embed.set_footer(text=str(message.id))
        await channel.send(content=content, embed=embed.copy())

    if tomatoCount > 5:
        async for m in channel.history(limit=2000):
            for e in m.embeds:
                for field in e.fields:
                    if message.jump_url in field.value:
                        await m.edit(content=content)
                        return

# various events checked when a message is sent
@wffle.event
async def on_message(message):

    ctx = await wffle.get_context(message)
    
    # ignores messages from the bot itself
    if message.author == wffle.user:
        return

    # responds to being mentioned
    if wffle.user.mentioned_in(message):
        async with ctx.typing():
            await asyncio.sleep(0.3)
            if 'LOL' in message.content:
                roleID = 921612594912059412
                role = message.guild.get_role(roleID)
                toPing = role.members
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
        async with ctx.typing():
            await asyncio.sleep(0.1)
        await message.channel.send('LOL')

    # @s NBad when monday is mentioned
    if 'monday' in str.lower(message.content):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        await message.channel.send('<@240192847209299969>')

    await wffle.process_commands(message)

# returns a list of commands the bot has
@wffle.command()
async def sauce(ctx):
    help = 'My commands are:\n!cork\n!invytime\n!tierlist\n!whlist\n!randlist\n!msb\n!tg\n!dichi'
    await ctx.send(help)

# reposts a random message from the corkboard, ignoring plain text messages
@wffle.command()
async def cork(ctx):
    async with ctx.typing():
        channel = wffle.get_channel(836433543726628935)
        messages = await channel.history(limit=500).flatten()
        rand = randint(0, len(messages)-1)
        randMessage = messages[rand]
        
        while randMessage.embeds == None and rand !=0:
            rand -= 1
            randMessage = messages[rand]
        await asyncio.sleep(1)
    for e in randMessage.embeds:
        await ctx.send(embed=e.copy())

# returns the current time in NST
@wffle.command()
async def invytime(ctx):
    async with ctx.typing():
        invytime = datetime.now(pytz.timezone('America/St_Johns'))
        await asyncio.sleep(0.3)
    await ctx.send(f'The correct time is: {invytime.strftime("%#I:%M %p")}')

# returns a randomized Rivals of Aether tier list
@wffle.command()
async def tierlist(ctx, *, arg = 'lol no'):
    async with ctx.typing():
        s = []
        a = []
        b = []
        c = []
        d = []
        f = []
        tiers = [s, a, b, c, d, f]
        list = ['Mollo', 'Clairen', 'Forsburn', 'Zetterburn', 'Wrastor',
        'Absa', 'Elliana', 'Pomme', 'Olympia', 'Sylvanos', 'Maypul', 'Kragg',
        'Ori', 'Shovel Knight', 'Orcane', 'Etalus', 'Ranno', 'Hodan']
        shuffle(list)
        for i in range(len(list)):
            tiers[randint(0, 5)].append(list[i])
        if arg != 'lol no':
            tierList = '**__' + arg + ' Tier List__**'
        else:
            tierList = '**__My tier list__**'
        tierList = tierList + '\nS: ' + ', '.join(s)
        tierList = tierList + '\nA: ' + ', '.join(a)
        tierList = tierList + '\nB: ' + ', '.join(b)
        tierList = tierList + '\nC: ' + ', '.join(c)
        tierList = tierList + '\nD: ' + ', '.join(d)
        tierList = tierList + '\nF: ' + ', '.join(f)
        await asyncio.sleep(1.5)
    await ctx.send(tierList)

# returns a randomized Waffle House member tier list
@wffle.command()
async def whlist(ctx, *, arg = 'lol no'):
    async with ctx.typing():
        s = []
        a = []
        b = []
        c = []
        d = []
        f = []
        tiers = [s, a, b, c, d, f]
        list = ['Ben', 'Reina', 'Tylor', 'Mia', 'Dinos',
        'NBad', 'Pantch', 'Jordan', 'Aeir', 'Michael', 'MSB',
        'Soren', 'Akashi', 'Quentin', 'TG', 'Stevie', 'Toby',
        'Waffle-bot', 'Acarcion', 'Danzello', 'Brad',
        'Backpack', 'Ceroas', 'Rift', 'Violet', 'Terra',
        'Sawtooth', 'Connor', 'Mage', 'raggedy', 'Jules', 'Subserial', 'Laura']
        shuffle(list)
        for i in range(len(list)):
            tiers[randint(0, 5)].append(list[i])
        if arg != 'lol no':
            tierList = '**__' + arg + ' Tier List__**'
        else:
            tierList = '**__My tier list__**'
        tierList = tierList + '\nS: ' + ', '.join(s)
        tierList = tierList + '\nA: ' + ', '.join(a)
        tierList = tierList + '\nB: ' + ', '.join(b)
        tierList = tierList + '\nC: ' + ', '.join(c)
        tierList = tierList + '\nD: ' + ', '.join(d)
        tierList = tierList + '\nF: ' + ', '.join(f)
        await asyncio.sleep(1.5)
    await ctx.send(tierList)

# ruins lives
@wffle.command()
async def whilst(ctx):
    async with ctx.typing():
        await asyncio.sleep(0.2)
    await ctx.send('BRITISH.')
    
# returns a randomized Waffle House member tier list of random topic
@wffle.command()
async def randlist(ctx=None):
    async with ctx.typing():
        channel = wffle.get_channel(835366700093407255)
        s = []
        a = []
        b = []
        c = []
        d = []
        f = []
        tiers = [s, a, b, c, d, f]
        list = ['Ben', 'Reina', 'Tylor', 'Mia', 'Dinos',
        'NBad', 'Pantch', 'Jordan', 'Aeir', 'Michael', 'MSB',
        'Soren', 'Akashi', 'Quentin', 'TG', 'Stevie', 'Toby',
        'Waffle-bot', 'Acarcion', 'Danzello', 'Brad',
        'Backpack', 'Ceroas', 'Rift', 'Violet', 'Terra',
        'Sawtooth', 'Connor', 'Mage', 'raggedy', 'Jules', 'Subserial', 'Laura']
        shuffle(list)
        for i in range(len(list)):
            tiers[randint(0, 5)].append(list[i])
        r = RandomWord()
        adj = r.word(include_parts_of_speech=['adjectives'])
        tierList = ''
        if ctx == None:
            tierList += "*Tier List of the Day*\n"
        tierList = '**__' + adj.capitalize() + ' Tier List__**'

        tierList = tierList + '\nS: ' + ', '.join(s)
        tierList = tierList + '\nA: ' + ', '.join(a)
        tierList = tierList + '\nB: ' + ', '.join(b)
        tierList = tierList + '\nC: ' + ', '.join(c)
        tierList = tierList + '\nD: ' + ', '.join(d)
        tierList = tierList + '\nF: ' + ', '.join(f)
        await asyncio.sleep(1.5)
    if ctx == None:
        await channel.send(tierList)
    else:
        await ctx.send(tierList)

# returns a randomized MSB acronym
@wffle.command()
async def msb(ctx):
    async with ctx.typing():
        r = RandomWord()
        first = r.word(starts_with="m")
        middle = r.word(starts_with="s")
        last = r.word(starts_with="b")
        name = first.capitalize() + " " + middle.capitalize() + " " + last.capitalize()
        await asyncio.sleep(0.5)
    await ctx.send(name)

# returns a randomized TG acronym
@wffle.command()
async def tg(ctx):
    async with ctx.typing():
        r = RandomWord()
        first = r.word(starts_with="t")
        last = r.word(starts_with="g")
        name = first.capitalize() + " " + last.capitalize()
        await asyncio.sleep(0.5)
    await ctx.send(name)

# returns a randomized DiChiDu acronym
@wffle.command()
async def dichi(ctx):
    async with ctx.typing():
        r = RandomWord()
        first = r.word(starts_with="di")
        middle = r.word(starts_with="chi")
        last = r.word(starts_with="du")
        name = first.capitalize() + " " + middle.capitalize() + " " + last.capitalize()
        await asyncio.sleep(0.5)
    await ctx.send(name)

# scrapes plain text messages from the given channel (dev only)
@wffle.command()
async def scrape(ctx):

    if ctx.author.id != 176454993681842176:
        await ctx.send("Unauthorized command LOL")
        return

    async with ctx.typing():
        written = 0
        channel = ctx.channel
        with open('messages.txt', 'a', encoding="utf-8") as f:
            async for message in channel.history(limit=200000):
                content = message.content
                if content and message.author.id != 921269920002633779:
                    if not (content.startswith('!') or content.startswith('https')) and not (content.startswith('<@') and len(content) < 20):
                        f.write(message.content + '\n<|endoftext|>\n')
                        written += 1
        await asyncio.sleep(0.5)
    await ctx.send(str(written) + " messages scraped!")

# combs server history to retroactively populate hall of shame (dev only)
@wffle.command()
async def tomatoes(ctx):

    if ctx.author.id != 176454993681842176:
        await ctx.send("Unauthorized command LOL")
        return
    
    tomatoChannel = wffle.get_channel(921430906412073070)
    
    async with ctx.typing():
        guild = ctx.guild
        channels = await guild.fetch_channels()
        for channel in channels:
            if str(channel.type) == 'text':
                async for message in channel.history(limit=200000, oldest_first=True):

                    author = message.author
                    attachments = message.attachments
                    reactions = message.reactions
                    tomatoCount = 0

                    for reaction in reactions:
                        if reaction.emoji == '\N{TOMATO}':
                            tomatoCount = reaction.count
                    content = ":tomato: **" + str(tomatoCount) + "** <#" + str(message.channel.id) + ">"

                    if tomatoCount >= 5:
                        embed = nextcord.Embed(description=message.content, colour=0xe74c3c)
                        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
                        source = '[Jump!](' + message.jump_url + ')'
                        embed.add_field(name='Source', value=source, inline=False)
                        if attachments:
                            if attachments[0].content_type.startswith('image'):
                                embed.set_image(url=attachments[0].url)
                            else:
                                if attachments[0].content_type.startswith('video'):
                                    attachment = '[' + attachments[0].filename + '](' + attachments[0].url + ')'
                                    embed.add_field(name='Attachment', value=attachment)
                        embed.timestamp = message.created_at
                        embed.set_footer(text=str(message.id))
                        await tomatoChannel.send(content=content, embed=embed.copy())

# for running the bot locally
if config['token']:
    wffle.run(config['token'])

# for running the bot on a host server
else:
    if __name__ == "__main__":
        wffle.run(TOKEN)
