# from requests import get
# import random
import os
import discord
from discord.ext import commands
from datetime import datetime
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
    print(f"{path}/pp.png correctly downloaded")
    return path

async def image_to_ascii(author):
  path = await download_pp(author)
  #path = "2020-10-14 13:50:38.650156_705398715409498175"
  file_path = f"{path}/pp.png"

  img = Image.open(file_path)
  pix = img.load()
  (sx, sy) = img.size
  print(f"Image size : {sx}:{sy}")
  pasx = sx / 22
  pasy = sy / 44
  pasm = pasx if pasx > pasy else pasy
  print("pasx, pasy, pasm", pasx, pasy, pasm)

  matpa = []
  l = 0
  #pasm = int(pasm)
  for i in range(sx):
      if int(i % (pasm / 2)) == 0:
          lst = []
          l = 0
      l = l + 1
      for j in range(sy):
          (r, g, b) = pix[i, j]
          try:
              lst[int(j / pasm)] += int(r + g + b)
          except:
              lst.append(int(r + g + b))
          pass
      if int(i % (pasm / 2)) == 0 and l != 0:
          #print(len(lst))
          for k in range(len(lst)):
              lst[k] = int(lst[k] / (pasm * pasm))
          #print(lst)
          matpa.append(lst)

  print("len matpa", len(matpa), len(matpa[0]))
  #print(matpa)

  min = matpa[0][0]
  max = matpa[0][0]

  for i in range(len(matpa)):
      for j in range(len(matpa[0])):
          if matpa[i][j] < min:
              min = matpa[i][j]
          if matpa[i][j] > max:
              max = matpa[i][j]

  print("min, max", min, max)

  spectre = " .:#"
  spectre = ".:#█"
  spectre = " ░▒▓█"
  spectre = "░▒▓█"
  print("len spectre : ", len(spectre))
  taille_intensite = max - min
  intensite_diff = taille_intensite / (len(spectre) - 1)
  print("intensite_diff", intensite_diff)

  mascii = list()

  for j in range(len(matpa[0])):
      lst = []
      for i in range(len(matpa)):
          intensite_case = int((matpa[i][j] - min) / intensite_diff)
          #print(intensite_case, spectre[intensite_case])
          lst.append(spectre[intensite_case])
      mascii.append(lst)

  strr = str(mascii).replace("[", "").replace("], ","\n").replace(", ", "").replace("]", "").replace("\'", "")
  #print(strr)
  print(len(strr))
  print("len mascii", len(mascii), len(mascii[0]))
  return strr




# IMPORT BOT : https://discord.com/api/oauth2/authorize?client_id=765714860221661204&permissions=8&scope=bot

TOKEN = open("token.txt","r").readlines()[0]
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
    #await message.channel.send(message)
    #await message.channel.send(message.content)
    #await message.channel.send(message.mentions)
    if message.content.startswith("&asciipp"):
      #if len(message.content.split(" ")) == 2:
      #  id = message.content.split(" ")[1]
      #  if id.isnumeric():
      #    author = client.get_user(id)
      if len(message.mentions) > 0:
        author = message.mentions[0]
      else:
        author = message.author
      strr = await image_to_ascii(author)
      #await message.channel.send(strr)

      embed = discord.Embed(title = f"Ascii pp for {author}", description = strr, color=0x29c87e)
      embed.timestamp = datetime.utcnow()
      embed.set_footer(text="footer : En dev", icon_url=client.get_user(391582181392384000).avatar_url)
      await message.channel.send(embed = embed)
      return

    if message.content == "&invite" and message.author.id == 391582181392384000:
      await message.channel.send("https://discord.com/api/oauth2/authorize?client_id=765714860221661204&permissions=8&scope=bot")


# bot.run(TOKEN)
client.run(TOKEN)
