
This utility is for creating an overlay of recommended signals for data campaigns being defined by the COVESA CV BoF from VSS yaml and a Google spreadsheet.

After we decide how to organize the sampling campaigns to be used in an overlay or represent otherwise, this utility may be deprecated along with the spreadhseet and continued contributions managed completely in github.

## Install Dependencies

'pip install pandas pyyaml'

or if on debian/ubuntu

'apt install python3-{yaml,pandas}'

## Use

grab appropriate version of vss

'wget -O vss.yaml https://github.com/COVESA/vehicle_signal_specification/releases/download/v6.1/vss.yaml'

(snapshots vss_rel_4.0.yaml and vss_rel_6.1.yaml are kept in this folder; the script takes the VSS yaml path as an optional first argument, default vss.yaml)

In a browser retrieve csv output from the latest version of data campaign spreadsheet being worked on and name it sheet.csv

File->Download->CSV from

Fleet:

https://docs.google.com/spreadsheets/d/1FMtSLhJy1REgadlnSwAqPX7r57rqdLYyw4W7ZsWyg8E/edit#gid=2020824572

Insurance: 

https://docs.google.com/spreadsheets/d/1Np9uLvwEESZ09dMcXoSvoyoyj5L_Le0k

mv ~/Downloads/'Fleet Management Data [PUBLIC] - Pillar -_ UseCase -_ Data Needs.csv' sheet.csv 

move the downloaded csv into the same directory as vss.yaml 

Should we continue to use the spreadsheet, consider replacing above with a script with arguments for which data campaign and version of VSS to use as input, wgets the resources, converts to csv and runs the conversion util.

snapshots of those resource and output from this script are in this folder of this repo, the spreadsheet csv might be out of date. 

python3 merge-sheet.py vss_rel_6.1.yaml

A VSS cell may list several signals (newline, space or comma separated, braces like {a,b} and * wildcards are expanded against the VSS tree). Rows with no Vehicle.* token (e.g. 'not in VSS yet, proposal: ...') are skipped.

Last refreshed from the spreadsheet: 2026-11-04 (VSS 6.1; 107 signals matched, 6 proposals not yet in VSS).

results in output.yaml
