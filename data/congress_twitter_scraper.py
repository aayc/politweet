from bs4 import BeautifulSoup

import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

handlers = list()

twitter_web_data = list()
with open("data.txt", "r") as f:
    twitter_web_data = f.readlines()

for url in twitter_web_data:
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
        handlers.append('@' + item['data-screen-name'])

with open("congressman.json", 'w') as f:
    f.write(json.dumps(handlers, indent=4,  sort_keys=True))

