import twitter
from bs4 import BeautifulSoup
import requests
import os
import json

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
                    full_tweet = soup.find('div', attrs={'class': 'js-tweet-text-container'})

                    # Save back to json.
                    if full_tweet is not None:
                        item['text'] = full_tweet.text.strip()
                        item['truncated'] = False
        except:
            print("URL:", str(url))

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

scraped_data = dict()

# Presidents.
scraped_data["@realdonaldtrump"] = get_tweets("@realdonaldtrump")
scraped_data["@barackobama"] = get_tweets("@barackobama")
scraped_data["@GeorgeWBush"] = get_tweets("@GeorgeWBush")
scraped_data["@BillClinton"] = get_tweets("@BillClinton")
scraped_data["@GeorgeHWBush"] = get_tweets("@GeorgeHWBush")

# Business people
scraped_data["@BillGates"] = get_tweets("@BillGates")
scraped_data["@tim_cook"] = get_tweets("@tim_cook")
scraped_data["@elonmusk"] = get_tweets("@elonmusk")
scraped_data["@richardbranson"] = get_tweets("@richardbranson") # Virgin
scraped_data["@satyanadella"] = get_tweets("@satyanadella")
scraped_data["@jeffbezos"] = get_tweets("@jeffbezos")

# News people...
# CNN
scraped_data["@andersoncooper"] = get_tweets("@andersoncooper")
scraped_data["@CNNSitRoom"] = get_tweets("@CNNSitRoom")
scraped_data["@jaketapper"] = get_tweets("@jaketapper")
scraped_data["@donlemo"] = get_tweets("@donlemo")
scraped_data["@JohnKingCNN"] = get_tweets("@JohnKingCNN")
scraped_data["@VanJones68"] = get_tweets("@VanJones68")

# Fox
scraped_data["@seanhannity"] = get_tweets("@seanhannity")
scraped_data["@oreillyfactor"] = get_tweets("@oreillyfactor")
scraped_data["@DanaPerino"] = get_tweets("@DanaPerino")
scraped_data["@BretBaier"] = get_tweets("@BretBaier")
scraped_data["@TuckerCarlson"] = get_tweets("@TuckerCarlson")

# MSNBC
scraped_data["@JoeNBC"] = get_tweets("@JoeNBC")
scraped_data["@KatyTurNBC"] = get_tweets("@KatyTurNBC")

# Singers
scraped_data["@katyperry"] = get_tweets("@katyperry")
scraped_data["@justinbieber"] = get_tweets("@justinbieber")
scraped_data["@rihanna"] = get_tweets("@rihanna")
scraped_data["@taylorswift13"] = get_tweets("@taylorswift13")
scraped_data["@ladygaga"] = get_tweets("@ladygaga")
scraped_data["@ArianaGrande"] = get_tweets("@ArianaGrande")
scraped_data["@selenagomez"] = get_tweets("@selenagomez")
scraped_data["@britneyspears"] = get_tweets("@britneyspears")

# Authors
scraped_data["@jk_rowling"] = get_tweets("@jk_rowling")

# Actors / TV People
scraped_data["@tomhanks"] = get_tweets("@tomhanks")
scraped_data["@SteveCarell"] = get_tweets("@SteveCarell")
scraped_data["@TheRock"] = get_tweets("@TheRock")
scraped_data["@WhoopiGoldberg"] = get_tweets("@WhoopiGoldberg")
scraped_data["@Oprah"] = get_tweets("@Oprah")
scraped_data["@kingsthings"] = get_tweets("@kingsthings")
scraped_data["@TheRealStanLee"] = get_tweets("@TheRealStanLee")

# Save to json.
with open("./stable-datasets/show.json", "w") as f:
    data = []
    f.write(json.dumps(scraped_data, indent=2, sort_keys=True))
