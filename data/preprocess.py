import json
import csv
import sys
import re
import text_to_vector
import pandas as pd
import nltk
from functools import reduce
from nltk.corpus import stopwords
nltk.download('stopwords')
import string

if len(sys.argv) < 4:
    print("USAGE <input-tweets.json> <input-congress.json> <out.json>")
    sys.exit(0)

TWEET_FILE_NAME = sys.argv[1]
CONGRESS_FILE_NAME = sys.argv[2]
OUTPUT_FILE_NAME = sys.argv[3]
STOP_WORDS = set(stopwords.words('english'))
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
        s = str(tweet["text"].replace("\u00a0\u2026", ""))  # weird tags at the end of tweets, not adding information.
        url_pattern = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|pic\.[a-zA-Z0-9]+\.[^\s]{2,})'
        s = re.sub(url_pattern, '', s)
        s = re.sub("#[a-zA-Z]+", '', s) # remove hash tags
        s = s.translate(str.maketrans('', '', string.punctuation))
        words = [word.lower() for word in s.split(" ") if word not in STOP_WORDS and \
                                                          word not in string.punctuation and \
                                                          not word.isdigit()]
        #print(words)

        ls = text_to_vector.infer(s.split(" ")).tolist()
        for i in range(len(ls)):
            d["x" + str(i)] = ls[i]
        
        d["x" + str(len(ls))] = tweet["favorite_count"]
        
        d["ideology"] = ideologies[twitter_handle]
        output.append(d)
'''
with open(OUTPUT_FILE_NAME, 'w') as f:
    w = csv.DictWriter(f, output[0].keys())
    w.writeheader()
    w.writerows(output)

'''
'''
print("Concatenating data frames together and putting out as csv (", len(output),"records )")
dfs = [pd.DataFrame(output[x:x + 1000]) for x in range(0, len(output) - 1000, 1000)]
print("dfs done: ", len(dfs))
df = reduce(lambda x, y: pd.concat([x, y]), dfs, pd.DataFrame())
print("reduced")
'''
df = pd.DataFrame(output)
df.to_csv(OUTPUT_FILE_NAME)
