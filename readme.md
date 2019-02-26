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
python3 get-tweets.py
```

## Doc2Vec Wikipedia Model
Download and untar the archive found [here](https://ibm.ent.box.com/s/3f160t4xpuya9an935k84ig465gvymm2), then store the model as `analysis/doc\_models/enwiki_dbow/doc2vec.bin`.  Execute `tests/test-doc-model.py` to verify that the model is saved to the right location.

# Authors
Aaron Chan, Austin Kolander, Jonathan Dutson, Andrew Tate
