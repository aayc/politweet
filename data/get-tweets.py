import twitter
import os
import json

KEY_DIRECTORY = "../keys/keys.json"

# Open Twitter API keys file
if os.path.isfile(KEY_DIRECTORY):
    with open(KEY_DIRECTORY) as f:
        keys = json.loads(f.read())
else:
    print("API Key file not found.  Message Aaron Chan for a copy.")
    raise SystemExit()


api = twitter.Api(consumer_key = keys["consumer_api_key"],
                  consumer_secret = keys["consumer_api_secret"],
                  access_token_key = keys["access_token"],
                  access_token_secret = keys["access_token_secret"])



