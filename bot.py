# bot.py
# Discord bot that will post covid statistics using covid! in discord.
# Produces list of US States and Territories with the their total number of confirmed cased in total desc
import requests
import sys
import discord
import os
import math
import stateDictionary

from dotenv import load_dotenv
from bs4 import BeautifulSoup
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PETEID = os.getenv('PETE_ID')
SPONGE_MEME = 'https://vignette.wikia.nocookie.net/mlg-parody/images/1/1b/Mocking-spongebob-1556133078.jpg/revision/latest?cb=20190812032513'
STAT_SITE = 'https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html#states'

# returns the column with adjusted spacing for table formating 
def adjustCol(column, maxLength):
    currLength = len(column)
    if (currLength < maxLength):
        adjustment = maxLength
        column = column.ljust(adjustment)
    return column

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
        await ctx.send('mAyBE HaVe iT oNlY ShOw STatEs wItH oVer 1,000 CaSEs')
        await ctx.send(SPONGE_MEME)

    # No argument outputs all USA State data
    elif args == '':
        await ctx.send('Initializing all USA state data...')

    
    elif int(args) > 0 and args != '':
        await ctx.send('Initializing USA state data with cases >= ' + args)

    #TODO: This is broken, we never get here due to previous elif error on int(args)
    # We couldn't find the command the user typed
    else: 
        await ctx.send('Command does not exist.')

    response = '```| State | Cases  | Deaths | %    |' + '\n'
    page = requests.get(STAT_SITE)
    soup = BeautifulSoup(page.content, 'html.parser')   
    table = soup.table
    resultCases = 0
    resultDeaths = 0
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) == 6:
            webState = cells[0].find(text=True, recursive=False)
            totalCases = cells[1].find(text=True)
            newCases = cells[2].find(text=True)
            totalDeaths = cells[3].find(text=True)

            stateStrip = webState.strip().replace(':', '')
            totalCasesNum = int(totalCases.strip().replace(',', '') or 0)

            # No argument outputs all USA State data
            if args == '':

                # Don't process US territories and misc.
                if (stateStrip != 'Wuhan Repatriated' 
                and stateStrip != 'Diamond Princess Cruise' 
                and stateStrip != 'United States Virgin Islands' 
                and stateStrip != 'Northern Mariana Islands' 
                and stateStrip != 'American Samoa'
                and stateStrip != 'Guam'):

                    
                    state =  adjustCol(stateDictionary.us_state_abbrev[stateStrip], 5)
                    totalCasesNum = int(totalCases.strip().replace(',', '') or 0)
                    resultCases = resultCases + totalCasesNum
                    cases = adjustCol(str(totalCasesNum), 6)
                    totalDeathsNum= int(totalDeaths.strip().replace(',', '') or 0)
                    resultDeaths = resultDeaths + totalDeathsNum
                    deaths = adjustCol(str(totalDeathsNum), 6)
                    deathPercent =  round_up((totalDeathsNum / totalCasesNum) * 100, 2)
                    ratio = adjustCol(str(deathPercent), 4)
                    response = response + '| ' + state + ' | ' + cases + ' | '+ deaths + ' | ' + ratio +  ' |' +'\n'

            # Grab all the instances over the argument
            elif int(args) > 0:

                if (stateStrip != 'Wuhan Repatriated' 
                and stateStrip != 'Diamond Princess Cruise' 
                and stateStrip != 'United States Virgin Islands' 
                and stateStrip != 'Northern Mariana Islands' 
                and stateStrip != 'American Samoa'
                and stateStrip != 'Guam'
                and totalCasesNum >= int(args)):
            
                    state =  adjustCol(stateDictionary.us_state_abbrev[stateStrip], 5)
                    totalCasesNum = int(totalCases.strip().replace(',', '') or 0)
                    resultCases = resultCases + totalCasesNum
                    cases = adjustCol(str(totalCasesNum), 6)
                    totalDeathsNum= int(totalDeaths.strip().replace(',', '') or 0)
                    resultDeaths = resultDeaths + totalDeathsNum
                    deaths = adjustCol(str(totalDeathsNum), 6)
                    deathPercent =  round_up((totalDeathsNum / totalCasesNum) * 100, 2)
                    ratio = adjustCol(str(deathPercent), 4)
                    response = response + '| ' + state + ' | ' + cases + ' | '+ deaths + ' | ' + ratio +  ' |' +'\n'
    
    deathPercentTotal =  round_up((resultDeaths / resultCases) * 100, 2)
    printResultCases = adjustCol(str(resultCases), 6)
    printResultDeaths = adjustCol(str(resultDeaths), 6)
    printRatio = adjustCol(str(deathPercentTotal), 4)
    response = response + '| ' + 'Total' + ' | ' + printResultCases + ' | '+ printResultDeaths + ' | ' + printRatio +  ' |' +'\n'
    await ctx.send(response + '```')
    response = ''
    
bot.run(TOKEN)