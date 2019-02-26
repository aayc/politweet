#!/bin/bash

# NOTE: Austin manually filled in the twitter handlers in congress.json.  It's not recommended to replace his hard work!

# Use temporary data folder to avoid committing unnecessary files with git
mkdir -p tmp/

# Use Jonathan's script to scrape house, senate
python3 get-politician-ideologies.py house tmp/house.json
python3 get-politician-ideologies.py senate tmp/senate.json

# Pull house, senate csv files
curl https://www.govtrack.us/congress/members/report-cards/2018/house/ideology.csv > tmp/house.csv
curl https://www.govtrack.us/congress/members/report-cards/2018/senate/ideology.csv > tmp/senate.csv

# Run Austin's merge script
python3 merge-politician-data.py tmp/senate.json tmp/senate.csv tmp/house.json tmp/house.csv stable-datasets/output.json

