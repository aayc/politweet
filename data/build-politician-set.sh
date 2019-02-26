#!/bin/bash

# Use temporary data folder to avoid committing unnecessary files with git
mkdir -p tmp/

# Use Jonathan's script to scrape house, senate
python3 get-politician-ideologies.py house tmp/house.json
python3 get-politician-ideologies.py senate tmp/senate.json
