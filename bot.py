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

    if message.content == '!covid':
        response = '+ State + Total Cases + Total Deaths +' + '\n'
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
                
                #TODO: 
                #string length compare add spaces against United States Virgin Islands
                #Add ratio for Deaths / Cases

                response = response + '+ ' + state.strip() + ' + ' + totalCases.strip() + ' + '+ totalDeaths.strip() + ' + ' + '\n'
        response = '+--------------+--------------+--------------+ \n' + response + '+--------------+--------------+--------------+'
        await message.channel.send(response)
        response = ''

client.run(TOKEN)