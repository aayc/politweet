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
python3 data/get-tweets.py
```

# Authors
Aaron Chan, Austin Kolander, Jonathan Dutson, Andrew Tate
