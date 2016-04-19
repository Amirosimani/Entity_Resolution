import pandas as pd
import json
import re
import sys
import os
from Levenshtein import distance
import csv

with open('foursquare_test_hard.json') as json_data:
    foursquare_test = json.load(json_data)
with open('locu_test_hard.json') as json_data:
    locu_test = json.load(json_data)

#normalizing phone numbers
for i, phone in enumerate(d['phone'] for d in foursquare_test): 
    if phone is None:
        foursquare_test[i]['phone'] = '0'
    else:
        foursquare_test[i]['phone'] = re.sub(r'[-|)|(| ]', '', phone)

for i, phone in enumerate(d['phone'] for d in foursquare_test): 
    if phone is None:
        foursquare_test[i]['phone'] = '0'
    else:
        foursquare_test[i]['phone'] = re.sub(r'[-|)|(| ]', '', phone)
        print(i,phone)


#decision
fsT_id = []
locuT_id = []

for d in foursquare_test:
    for e in locu_test:
        if e['name'].lower() == d['name'].lower():
            if e['latitude'] == d['latitude'] or ['longitude'] == d['longitude']:
                fsT_id.append(d['id'])
                locuT_id.append(e['id'])
            elif len(e['website'])>1 and len(d['website']) >1:
                if (1 - (distance(e['website'].lower(), d['website'].lower())/max(len(e['website']), len(d['website'])))) > 0.8:
                    if d not in fsT_id:
                        fsT_id.append(d['id'])
                        locuT_id.append(e['id'])
            elif len(e['street_address'])>1 and len(d['street_address']) >1:
                if (1 - (distance(e['street_address'].lower(), d['street_address'].lower())/max(len(e['street_address']), len(d['street_address'])))) > 0.8:
                    if d not in fsT_id:
                        fsT_id.append(d['id'])
                        locuT_id.append(e['id'])
        elif (1 - (distance(e['name'].lower(), d['name'].lower())/max(len(e['name']), len(d['name'])))) > 0.7:
                if e['latitude'] == d['latitude'] or ['longitude'] == d['longitude'] or e['phone'] == d['phone']:
                    fsT_id.append(d['id'])
                    locuT_id.append(e['id'])
                elif len(e['website'])>1 and len(d['website']) >1:
                    if (1 - (distance(e['website'].lower(), d['website'].lower())/max(len(e['website']), len(d['website'])))) > 0.7:
                        fsT_id.append(d['id'])
                        locuT_id.append(e['id'])
                elif len(e['street_address'])>1 and len(d['street_address']) >1:
                    if (1 - (distance(e['street_address'].lower(), d['street_address'].lower())/max(len(e['street_address']), len(d['street_address'])))) > 0.7:
                        fsT_id.append(d['id'])
                        locuT_id.append(e['id'])  

rowsT = zip(locuT_id, fsT_id)
my_filenameT = 'match_test03.csv'

w = csv.writer(open(my_filenameT,"w"))
w.writerow(['locu_id', 'foursquare_id'])
w.writerows(rowsT)