from bs4 import BeautifulSoup

import json
import requests
import sys
import pandas as pd

if len(sys.argv) < 4:
    print("USAGE python3 merge-politician-scrape.py <senate json> <house json> <output file name>")
    sys.exit()

SENATE_FILE_NAME = sys.argv[1]
HOUSE_FILE_NAME = sys.argv[2]
OUTPUT_FILE_NAME = sys.argv[3]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}
stop_words = ["rep.", "rep", "senator", "sen", "sen.", "congressman", "u.s.", ",m.d.", "congresswoman",
              "DDS", "Rep.", "Dr.", "U.S. Representative", "Cong.", "cong.", "U.S. Rep.", "Senator"]

missing_handlers = list()

def name_util(name):
    sub_names = name.split()
    name = ''
    for part in sub_names:
        part = part.replace(",", "")
        temp = part.lower()
        if temp in stop_words:
            del part
        elif "." in part:
            del part
        elif "“" in part:
            name = part.replace("“", "").replace("”", "")
        else:
            name += part + ' '
        name.strip()

    if len(name.split()) == 1:
        letters = name[1:]
        name = name[0]
        for letter in letters:
            if letter.isupper():
                name += ' ' + letter
            else:
                name += letter
    return name.strip()

"""
    Combines data from scrape, csv for house of senate.
"""
def create_df(json_path, csv_path='senate.csv'):
    with open(json_path, "r") as f:
        crawled_data = json.loads(f.read())

    crawled_data.reverse()

    frame = pd.read_csv(csv_path)
    frame = frame.drop(['rank_from_low', 'rank_from_high', 'percentile', 'id', 'bioguide_id', 'district'], axis=1)
    frame['party'] = ''

    rows = list()
    for index, row in frame.iterrows():
        info = crawled_data[index]
        name = name_util(info[2])
        row['name'] = name
        row['party'] = info[3]
        rows.append(row)

    return pd.DataFrame(rows)

def twitter_handler(name):
    try:
        return '@' + twitter_lookup[name]
    except KeyError:
        missing_handlers.append(name)
        return ''

def create_twitter_lookup():
    lookup = dict()
    with open("twitter_urls.txt", "r") as f:
        twitter_urls = f.readlines()

    for url in twitter_urls:
        print(url)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Invalid access for -> " + str(url))
            continue

        json_obj = json.loads(response.text)

        if '!items_html' in json_obj or json_obj is None:
            print("No HTML for -> " + str(url))
            continue

        html = json_obj['items_html']
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', attrs={'class': 'account'})

        for item in items:
            name = name_util(item['data-name'])
            lookup[name] = item['data-screen-name']
    return lookup

senators = create_df(SENATE_FILE_NAME, csv_path='senate.csv')
representatives = create_df(HOUSE_FILE_NAME, csv_path='house.csv')
congress = pd.concat([senators, representatives])

twitter_lookup = create_twitter_lookup()
congress['twitter_handler'] = congress['name'].apply(lambda name: twitter_handler(name))

print(congress)
print(congress.columns)
print(twitter_lookup)

# Save to json.
with open(OUTPUT_FILE_NAME, "w") as f:
    data = []
    for jdict in congress.to_dict(orient='records'):
        data.append({jdict['name']: jdict})
    f.write(json.dumps(data, indent=2, sort_keys=True))

# Save to csv.
#with open("congress.csv", "w") as f:
#    congress.to_csv(f)

#with open("needTwitterHandlers", "w") as f:
#    f.write(json.dumps(missing_handlers, indent=True, sort_keys=True))
