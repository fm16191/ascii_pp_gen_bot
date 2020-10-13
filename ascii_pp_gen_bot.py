# from requests import get
# import random
import sys
import os
import discord
from discord.ext import commands
from datetime import datetime
import asyncio
from fake_useragent import UserAgent
ua = UserAgent()
from PIL import Image
import requests

headers = {'content-type' : 'application/json; charset=utf-8', 'UserAgent' : ua.chrome}

async def makedir(author):
    # str = str(datetime.now()) + "_" +
    str = f"{datetime.now()}_{author.id}"
    os.mkdir(str)
    return str


async def download_pp(author):
    res = requests.get(author.avatar_url, allow_redirects=True, headers = headers)

    print(author.avatar_url)
    reqcontent = res.content
    path = await makedir(author)
    print(path)
    open(f"{path}/pp.png","wb").write(reqcontent)
    return path

async def image_to_ascii(author):
    # path = download_pp(author)
    path = "2020-10-13 23:36:16.472576_391582181392384000"
    file_path = f"{path}/pp.png"

    return True



# IMPORT BOT : https://discord.com/api/oauth2/authorize?client_id=765714860221661204&permissions=8&scope=bot

TOKEN = "NzY1NzE0ODYwMjIxNjYxMjA0.X4Y1iA.WJKFKe3vZ_CDsMgkkZ4g-iFUAgM"
prefix = "&"
# client = commands.Bot(command_prefix = prefix)
client = discord.Client()
bot = commands.Bot(command_prefix = "")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "&asciipp":
        author = message.author
        await image_to_ascii(author)

# bot.run(TOKEN)
client.run(TOKEN)
