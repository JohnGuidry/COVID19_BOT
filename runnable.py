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
page = requests.get('https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html#states')
soup = BeautifulSoup(page.content, 'html.parser')   
table = soup.table
for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) == 6:
        webState = cells[0].find(text=True, recursive=False)
        totalCases = cells[1].find(text=True)
        newCases = cells[2].find(text=True)
        totalDeaths = cells[3].find(text=True)

        stateStrip = webState.strip().replace(':', '')
        totalCasesNum = int(totalCases.strip().replace(',', '') or 0)

        print(stateStrip)
        print(totalCasesNum)