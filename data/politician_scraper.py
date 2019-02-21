import requests
from bs4 import BeautifulSoup

# Put report card URLS from govtrack.us below
url = 'https://www.govtrack.us/congress/members/report-cards/2018/senate/ideology'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
rows = soup.find_all('tr')

# Data becomes a list of lists. Each item in the list is a politician, and 
# each politician is a list composed of Rank, Score, Name, Party, and State
# in that order.

data = []
for row in rows:
    politician = []
    cols = row.find_all('td')
    if len(cols) == 3:
        cols = [ele.text.strip() for ele in cols]
        cols[0] = int(cols[0][-1:])
        cols[1] = float(cols[1])
        name_party_state = cols[2].split('[')
        cols[2] = name_party_state[0][:-1]
        party_state = name_party_state[1].split(',')[0]
        party_state = party_state.split(']')[0]
        parts = party_state.split('-')
        party = parts[0]
        state = parts[1]
        cols.append(party)
        cols.append(state)
        data.append([ele for ele in cols]) 
print(data)