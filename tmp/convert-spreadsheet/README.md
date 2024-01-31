2024/01/31: Note update pending, a few additional signals have been added and will be exposing curve logging thresholds. 

This utility is for creating a mockup overlay of recommended signals for the COVESA CV BoF

after we decide how to store the sampling campaign to be used in an overlay or represent otherwise, this will no longer be needed

wget https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.yaml

File->Download->CSV from https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E/edit#gid=2020824572

mv ~/Downloads/'Fleet Management Data [PUBLIC] - Pillar -_ UseCase -_ Data Needs.csv' sheet.csv 

snapshots of those resource and output from this script are in this folder of this repo, the spreadsheet csv might be out of date. 

We will switch at some point from coordinating in the spreadsheet to YAML as this tool currently produces and manage changes through pull requests 

pip install pandas pyyaml
python3.8 merge-sheet.py
results in output.yaml
