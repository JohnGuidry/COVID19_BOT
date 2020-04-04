# bot.py
# Discord bot that will post covid statistics using covid! in discord.
# Produces list of US States and Territories with the their total number of confirmed cased in total desc
import requests
import sys
import discord
import os
import math

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PETEID = os.getenv('PETE_ID')
SPONGE_MEME = 'https://vignette.wikia.nocookie.net/mlg-parody/images/1/1b/Mocking-spongebob-1556133078.jpg/revision/latest?cb=20190812032513'
STAT_SITE = 'https://www.worldometers.info/coronavirus/country/us/'

# Rounds up to nearest decimal place given the number of places
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# Set bot to go by commands !<command_name>
bot = commands.Bot(command_prefix='!')

# Verify we have connected
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# !covid command
@bot.command()
async def covid(ctx, args=''):

    # 1000 argument to mock Pete's suggestion
    if args == '1000':
        await ctx.send('{} mAyBE HaVe iT oNlY ShOw STatEs wItH oVer 1,000 CaSEs'.format(PETEID))
        await ctx.send(SPONGE_MEME)

    # No argument outputs all the data
    if args == '':
        response = '|State: Total Cases | Total Deaths | Ratio |' + '\n'
        page = requests.get(STAT_SITE)
        soup = BeautifulSoup(page.content, 'html.parser')   
        table = soup.table
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 7:
                state = cells[0].find(text=True)
                totalCases = cells[1].find(text=True)
                newCases = cells[2].find(text=True)
                totalDeaths = cells[3].find(text=True)

                stateStrip = state.strip().replace(':', '')
                totalCasesNum = int(totalCases.strip().replace(',', '') or 0)
                totalDeathsNum= int(totalDeaths.strip().replace(',', '') or 0)
                deathPercent =  round_up((totalDeathsNum / totalCasesNum), 2)
                response = response + '|' + stateStrip + ': ' + str(totalCasesNum) + ' | '+ str(totalDeathsNum) + ' | ' + str(deathPercent) +  ' | ' +'\n'
        await ctx.send(response)
        response = ''  
    
bot.run(TOKEN)