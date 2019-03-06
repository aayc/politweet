import twitter
from bs4 import BeautifulSoup
import requests
import os
import json
import sys


if len(sys.argv) < 6:
    print("USAGE: python3 get-tweets.py <start> <end> <congress json file> <output file name> <error file name>")
    sys.exit()

START_HANDLE_IX = int(sys.argv[1])
END_HANDLE_IX = int(sys.argv[2])
CONGRESS_FILE_NAME = sys.argv[3]
OUTPUT_FILE_NAME = sys.argv[4]
ERROR_FILE_NAME = sys.argv[5]

# Retrieve Twitter handles from congress json file
handles = []
errors = []
with open(CONGRESS_FILE_NAME, "r") as f:
    congress = json.load(f)
    handles = []
    for o in congress:
        for k, v in o.items():
            handles.append(v["twitter_handler"])

"""
    Gets tweets for a given twitter user. 
    
    @param: screen_name: name of twitter user, exp: @realdonaldtrump
    @param: count: how many to pull down, TWITTER MAX IS 250.
"""
def get_tweets(screen_name, count=250):
    tweets = []
    try:
        tweets = [i.AsDict() for i in api.GetUserTimeline(screen_name=screen_name, count=count)]
    except:
        errors.append(("faulty tweet return", None, screen_name))
        return []

    '''
    Band-Aid to capture tweets over 150 characters. Reading online it appears twitter doesn't
    officially support this. So we use the URL from the json to scrape the tweet from twitter.
    '''


    for item in tweets:
        try:
            if 'truncated' in item and item['truncated']:
                url = item['urls'][0]['expanded_url']
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    full_tweet = soup.find('div', attrs = {'class': 'js-tweet-text-container'})

                    # Save back to json.
                    if full_tweet is not None:
                        item['text'] = full_tweet.text.strip()
                        item['truncated'] = False
        except:
            print("URL:",str(url))
            errors.append(("faulty url", item['urls'][0]['expanded_url'], screen_name))

    return tweets


KEY_DIRECTORY = "../keys/keys.json"

# Open Twitter API keys file
if os.path.isfile(KEY_DIRECTORY):
    with open(KEY_DIRECTORY) as f:
        keys = json.loads(f.read())
else:
    print("API Key file not found. Message Aaron Chan for a copy.")
    raise SystemExit()

api = twitter.Api(consumer_key = keys["consumer_api_key"],
                  consumer_secret = keys["consumer_api_secret"],
                  access_token_key = keys["access_token"],
                  access_token_secret = keys["access_token_secret"])


results = {}

for i in range(START_HANDLE_IX, END_HANDLE_IX):
    handle = handles[i]
    print(handle, i,"/",len(handles))
    results[handle] = get_tweets(handle, 250)

'''
# Print tweets to file, (for debugging)
with open("tmp/tweets.txt", 'w') as f:
    for t in items:
        f.write(t['text'])
        f.write('\n\n')
'''
# Print tweets to file, (for debugging)
with open(OUTPUT_FILE_NAME, 'w') as f:
    f.write(json.dumps(results))

# Log errors
with open(ERROR_FILE_NAME, 'w') as f:
    f.write(json.dumps(errors))
