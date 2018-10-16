import discord
from discord.ext import commands
import asyncio
import random
import pyodbc
import pandas as pd
from itertools import cycle
TOKEN = 'NDczMzQ2NTg5MDIxMTc1ODA5.DoKvmg.zJKXSjyR0_84TkW8qxCBGSiCGHE'

client = commands.Bot(command_prefix = '!')
msg1 = "Practicing Backboard Shots"
msg2 = "With qlyoung's Locks"
msg3 = "Watching Sealable Ding"
msg4 = "Chooching Fat Clouds"
msg5 = "Seeking Vlastro Advice"
status = [msg5,msg2,msg3,msg4,msg1]

cnxt_string = cxntString = 'Driver={SQL Server Native Client 11.0};''Server=LAPTOP-GL92M0V0;''Database=myDB;''Trusted_Connection=yes;'

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(20)

def get_clip(name):
    temp = []
    connection = pyodbc.connect(cnxt_string)
    cursor = connection.cursor()
    cursor.execute("SELECT Link FROM clips WHERE Team =?", name)
    for row in cursor:
        full_link = "https://clips.twitch.tv/" + row[0]
        temp.append(full_link)
        print(full_link)
    ret_val = random.choice(temp)
    temp.clear()
    return ret_val

@client.event
async def on_ready():
    print("Bot is ready!")
    print('Logged in as:')
    print(client.user.id)
    print('------------')

@client.command()
async def qlyoung():
    responses = ['Always Goes Backboard!', 'Learned everything he knows from Vlastro', \
    'Chooches the fatest of cloudz', 'Is an idiot!', 'IS POONANNERS BIGGEST FAN!']
    await client.say(random.choice(responses))
    await asyncio.sleep(1)

@client.command()
async def subtlety():
    response = random.randint(1,5)
    if response == 1:
        await client.say('Is this guy ready?!?')
        await asyncio.sleep(1)
        await client.say('I DONT THINK THIS GUY IS READY!')
        await asyncio.sleep(2)
        await client.say('HE DOES IT AGAIN!!')
    elif response == 2:
        await client.say(':ear: _Lets goooo_')
    elif response == 3:
        await client.say("LETS FUCKING GO!!!!")
    elif response ==4:
        await client.say("ARE YOU KIDDING ME!?")
        await asyncio.sleep(1)
        await client.say("ARE YOU FUCKING KIDDING ME!?")
        await asyncio.sleep(1)
        await client.say("NO ONE CAN STOP THIS GUY!")

@client.command()
async def gatorz():
    link = get_clip("gatorz")
    await client.say(link)

@client.command()
async def kang():
    link = get_clip("kang")
    await client.say(link)
@client.command()
async def add_clip(*args):
    team = args[0]
    clip = args[1]
    if(team != 'gatorz') and (team != 'kang'):
        return
    connection = pyodbc.connect(cxntString)
    cursor = connection.cursor()
    str = clip[24:]
    print(str)
    cursor.execute("INSERT INTO clips(Team, Link) VALUES (?, ?)", team, str)
    connection.commit()
    connection.close()
    await client.say('Clip Added :movie_camera:')

@client.command()
async def sealable():
    await client.say('SLAM!')

@client.command()
async def ping():
    await client.say('Pong!')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command()
async def reverse(*args):
    output = ''
    for word in reversed(args):
        output += word[::-1]
        output += ' '
    await client.say(output)

@client.command(pass_context=True)
async def clear(ctx, amount=2):
    author = ctx.message.author
    if discord.utils.get(author.roles, name="KING ROO") is None:
        return
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say(':spy:')

@client.command(pass_context=True)
async def roll(ctx):
    num = random.randint(1,1000)
    await client.say("{} rolled a: {}".format(ctx.message.author.mention, num))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot: return
    if 'ego' in message.content:
        await client.send_message(message.channel, "Someone mention @Strembitsky#6372")
    await client.process_commands(message)

client.loop.create_task(change_status())
client.run(TOKEN)
