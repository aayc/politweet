import json
import sys

if len(sys.argv) < 4:
    print("USAGE <input-tweets.json> <input-congress.json> <out.json>")
    sys.exit(0)

TWEET_FILE_NAME = sys.argv[1]
CONGRESS_FILE_NAME = sys.argv[2]
OUTPUT_FILE_NAME = sys.argv[3]

full_dataset = []
with open(TWEET_FILE_NAME) as f:
    full_dataset = json.loads(f.read())

ideologies = {}
with open(CONGRESS_FILE_NAME) as f:
    congress = json.loads(f.read())
    for politician_wrapper in congress:
        politician_name = list(politician_wrapper.keys())[0]
        data = politician_wrapper[politician_name]
        ideologies[data["twitter_handler"]] = data["ideology"]

# OLD DATA STRUCTURE
# full_dataset[TWITTER HANDLE][0:250][obj with keys ['created_at', 'favorite_count', 'hashtags', 'id', 'id_str', 'lang', 'retweet_count', 'source', 'text', 'truncated', 'urls', 'user', 'user_mentions']]

output = []
features = ["id", "favorite_count", "text", "hashtags"]

# NEW DATA STRUCTURE
# [0:537] list of { twitter_handle, tweets: [{ features } x 250], ideology rating: }
# TODO
# remove http links
# remove hash tags from text

for twitter_handle in full_dataset.keys():
    politician = {}
    politician["twitter_handle"] = twitter_handle
    politician["tweets"] = []
    for tweet in full_dataset[twitter_handle]:
        if not all([f in tweet for f in features]):
            continue
        tweet["text"] = tweet["text"] # TODO remove http links, remove hash tags from text
        politician["tweets"].append([tweet[f] for f in features])
        politician["ideology"] = ideologies[twitter_handle]

    output.append(politician)



