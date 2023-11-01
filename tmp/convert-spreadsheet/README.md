This utility is for creating a mockup overlay of recommended signals for the COVESA CV BoF

after we decide how to store the sampling campaign to be used in an overlay or represent otherwise, this will no longer be needed

wget https://github.com/COVESA/vehicle_signal_specification/releases/download/v4.0/vss_rel_4.0.yaml

File->Download->CSV from https://docs.google.com/spreadsheets/d/1jXDBlig_0faVm91P7Y6tgOa3HH4dEGu6flyxlYpvGAY/edit?pli=1#gid=2020824572

mv ~/Downloads/'Fork of Fleet Management Data [PUBLIC] - Pillar -_ UseCase -_ Data Needs.csv' sheet.csv 

snapshots of those resource and output from this script are in this folder of this repo, the spreadsheet csv might be out of date

pip install pandas pyyaml
python3.8 merge-sheet.py
