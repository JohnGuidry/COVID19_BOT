# runnable.py
# Runs the python without the Discord
# Produces list of US States and Territories with the their total number of confirmed cased in total desc
import requests
import sys
import os
import math
import stateDictionary
from bs4 import BeautifulSoup

# returns the column with adjusted spacing for table formating 
def adjustCol(column, maxLength):
    currLength = len(column)
    if (currLength < maxLength):
        adjustment = maxLength
        column = column.ljust(adjustment)
    return column

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

print('| State | Cases  | Deaths | %    |')
page = requests.get('https://www.worldometers.info/coronavirus/country/us/')
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.table
for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 7:
        webState = cells[0].find(text=True)
        totalCases = cells[1].find(text=True)
        newCases = cells[2].find(text=True)
        totalDeaths = cells[3].find(text=True)
        newDeaths = cells[4].find(text=True)
        activeCases = cells[5].find(text=True)
        source = cells[6].find(text=True)

        stateStrip = webState.strip().replace(':', '')
        if (stateStrip != 'Wuhan Repatriated' and stateStrip != 'Diamond Princess Cruise'):
            state =  adjustCol(stateDictionary.us_state_abbrev[stateStrip], 5)
            totalCasesNum = int(totalCases.strip().replace(',', '') or 0)
            cases = adjustCol(str(totalCasesNum), 6)
            totalDeathsNum= int(totalDeaths.strip().replace(',', '') or 0)
            deaths = adjustCol(str(totalDeathsNum), 6)
            deathPercent =  round_up((totalDeathsNum / totalCasesNum) * 100, 2)
            ratio = adjustCol(str(deathPercent), 4)
            print('| ' + state + ' | ' + cases + ' | '+ deaths + ' | ' + ratio +  ' |')