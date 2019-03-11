import json
import sys
import re
import text_to_vector
import pandas as pd


if len(sys.argv) < 4:
    print("USAGE <input-tweets.json> <input-congress.json> <out.json>")
    sys.exit(0)

TWEET_FILE_NAME = sys.argv[1]
CONGRESS_FILE_NAME = sys.argv[2]
OUTPUT_FILE_NAME = sys.argv[3]
print("LOADING DOC2VEC MODEL, this might take a minute...")
text_to_vector.load_doc_model();

full_dataset = []
print("LOADING DATA, please wait for about 30 seconds.")
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
total_progress = len(list(full_dataset.keys()))
progress = 0
for twitter_handle in full_dataset.keys():
    progress += 1
    print("PROGRESS: ", progress, total_progress)

    for tweet in full_dataset[twitter_handle]:
        if not all([f in tweet for f in features]):
            continue

        d = {}

        # Clean up the tweets!
        string = str(tweet["text"].replace("\u00a0\u2026", ""))  # weird tags at the end of tweets, not adding information.
        url_pattern = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|pic\.[a-zA-Z0-9]+\.[^\s]{2,})'
        string = re.sub(url_pattern, '', string)
        # TODO: Remove hash tags by looking at hash tag param in text and remove #TheText + any punctuation?

        ls = text_to_vector.infer(string.split(" ")).tolist() # TODO remove stop words?
        for i in range(len(ls)):
            d["x" + str(i)] = ls[i]

        d["ideology"] = ideologies[twitter_handle]
        output.append(d)

    '''
    # OLD VERSION OF PREPROCESSING 
    politician = {}
    politician["twitter_handle"] = twitter_handle
    politician["tweets"] = []
    for tweet in full_dataset[twitter_handle]:
        if not all([f in tweet for f in features]):
            continue

        # Clean up the tweets!
        string = str(tweet["text"].replace("\u00a0\u2026", ""))  # weird tags at the end of tweets, not adding information.
        url_pattern = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|pic\.[a-zA-Z0-9]+\.[^\s]{2,})'
        string = re.sub(url_pattern, '', string)
        # TODO: Remove hash tags by looking at hash tag param in text and remove #TheText + any punctuation?

        tweet["text"] = string
        tweet["vector"] = "hello"#text_to_vector.infer(string.split(" ")).tolist() # TODO remove stop words?
        politician["tweets"].append([tweet[f] for f in features] + [tweet["vector"]])
        politician["ideology"] = ideologies[twitter_handle]

    output.append(politician)
    '''

df = pd.DataFrame(output)
df.to_csv(OUTPUT_FILE_NAME)

