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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PETEID = os.getenv('PETE_ID')

# Rounds up to nearest decimal place given the number of places
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Do not want the bot to loop itself
    if message.author == client.user:
        return

    # Mocking Pete
    if message.content == '!covid 1000':
        await message.channel.send('{} mAyBE HaVe iT oNlY ShOw STatEs wItH oVer 1,000 CaSEs'.format(PETEID))
        await message.channel.send('https://vignette.wikia.nocookie.net/mlg-parody/images/1/1b/Mocking-spongebob-1556133078.jpg/revision/latest?cb=20190812032513')

    # !covid command outputs the State Total Cases, Total Deaths, and ratio of death to cases
    if message.content == '!covid':
        response = '| State: Total Cases | Total Deaths | Ratio |' + '\n'
        page = requests.get('https://www.worldometers.info/coronavirus/country/us/')
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
                response = response + '| ' + stateStrip + ': ' + str(totalCasesNum) + ' | '+ str(totalDeathsNum) + ' | ' + str(deathPercent) +  ' | ' +'\n'
        await message.channel.send(response)
        response = ''

client.run(TOKEN)