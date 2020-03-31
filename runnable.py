# runnable.py
# Runs the python without the Discord
# Produces list of US States and Territories with the their total number of confirmed cased in total desc
import requests
import sys
import os
from bs4 import BeautifulSoup

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
        newDeaths = cells[4].find(text=True)
        activeCases = cells[5].find(text=True)
        source = cells[6].find(text=True)
        print(state.strip() + ': ' + totalCases)