# bot.py
# Discord bot that will post covid statistics using covid! in discord.
# Produces list of US States and Territories with the their total number of confirmed cased in total desc
import requests
import sys
import discord
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'covid!':
        response = ''
        page = requests.get('https://www.worldometers.info/coronavirus/country/us/')
        soup = BeautifulSoup(page.content, 'html.parser')   
        table = soup.table
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 7:
                state = cells[0].find(text=True)
                totalCases = cells[1].find(text=True)
                #newCases = cells[2].find(text=True)
                #totalDeaths = cells[3].find(text=True)
                #newDeaths = cells[4].find(text=True)
                #activeCases = cells[5].find(text=True)
                #source = cells[6].find(text=True)
                #response = state.strip() + ': ' + totalCases
                response = response + state.strip() + ': ' + totalCases + '\n'
        await message.channel.send(response)
        response = ''

client.run(TOKEN)