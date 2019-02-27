import twitter
import os
import json
import sys


if len(sys.argv) < 3:
    print("USAGE: python3 get-tweets.py <congress json file> <output file name>")
    sys.exit()

CONGRESS_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]

# Retrieve Twitter handles from congress json file
handles = []
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
    tweets = [i.AsDict() for i in api.GetUserTimeline(screen_name=screen_name, count=count)]

    '''
    Band-Aid to capture tweets over 150 characters. Reading online it appears twitter doesn't
    officially support this. So we use the URL from the json to scrape the tweet from twitter.
    '''
    from bs4 import BeautifulSoup
    import requests

    for item in tweets:
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

results = { handle: get_tweets(handle, 250) for handle in handles[0:3] }

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
