
This utility is for creating an overlay of recommended signals for data campaigns being defined by the COVESA CV BoF from VSS yaml and a Google spreadsheet.

After we decide how to organize the sampling campaigns to be used in an overlay or represent otherwise, this utility may be deprecated along with the spreadhseet and continued contributions managed completely in github.

## Install Dependencies

'pip install pandas pyyaml'

or if on debian/ubuntu

'apt install python3-{yaml,pandas}'

## Use

grab appropriate version of vss

'wget -o vss.yaml https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.yaml'

In a browser retrieve csv output from the latest version of data campaign spreadsheet being worked on and name it sheet.csv

File->Download->CSV from https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E/edit#gid=2020824572

mv ~/Downloads/'Fleet Management Data [PUBLIC] - Pillar -_ UseCase -_ Data Needs.csv' sheet.csv 

move the downloaded csv into the same directory as vss.yaml 

Should we continue to use the spreadsheet, consider replacing above with a script with arguments for which data campaign and version of VSS to use as input, wgets the resources, converts to csv and runs the conversion util.

snapshots of those resource and output from this script are in this folder of this repo, the spreadsheet csv might be out of date. 

python3.8 merge-sheet.py

results in output.yaml
