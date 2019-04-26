# Installation and Setup
* Python 3.x.x and pip3
* keys/keys.json file (not hosted in repository for security reasons.
  * Never commit keys.json to the repository or we're toast.

The following commands are sufficient for setup and should run without error:
```
git clone https://github.com/aayc/politweet.git
cd politweet
mkdir keys/
mv [YOUR KEYS.JSON PATH] keys/keys.json
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
cd data
mkdir tmp # this directory is gitignored so that we don't keep committing data changes.
```

## Retrieving Data (large files)
The following commands will produce (after a very long time) a set of raw tweet and other metadata.
```
python3 get-tweets.py 1 537 stable-datasets/congress.json OUTPUT_FILE_NAME.json ERROR_FILE_LOG.json
```

## Doc2Vec Wikipedia Model
Download and untar the archive found [here](https://ibm.ent.box.com/s/3f160t4xpuya9an935k84ig465gvymm2), then store the model as `data/doc\_models/enwiki_dbow/doc2vec.bin`.  Execute `tests/test-doc-model.py` to verify that the model is saved to the right location.

# Preprocessing Data
You will need:

* a sample dataset from the tweet scrape (the scrape takes really long, so download it from the Google Drive folder)
* the congress.json information file (located in stable-datasets/, committed)
* the doc2vec model (see under installation and setup)

Run `python3 preprocess.py <tweets file, like stable-datasets/3-4-2019-0-537.json> <congress file, like stable-datasets/congress.json> <OUTPUT FILE NAME.csv>`

# Results and Conclusion
Due to the imbalanced dataset and the many tweets we had that were nonpolitical in nature, our results were mixed.  For political tweets, our model seemed to perform fairly accurately (although somewhat inconsistently).  Several factors including emojis, short-length tweets and mispelled words, etc., were confusing for our model.  Overall, we achieved a 79% accuracy with a baseline accuracy of 55% (due to our lopsided dataset) using a Support Vector Machine with an RBF kernel.  We were pretty happy with it.

# Authors
Aaron Chan, Austin Kolander, Jonathan Dutson, Andrew Tate
