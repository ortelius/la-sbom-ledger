import json
from nft_storage_utils import *
import time
import ijson

def importByResourceFile(path):

    with open(path) as f:
        data = json.load(f)

        cids = []
        spdx_cids = { 
            "licenseListVersion": data['licenseListVersion'], 
            "licenses": cids ,
            "releaseDate": "2022-11-16"
        }
        
        totalLicenses = 0
        print("The Import started at: "+str(time.time()))
        for elem in data['licenses']:
            response = save(elem, 'json')
            totalLicenses += 1
            assert response['ok'] == True
            print("Imported license Index: "+str(totalLicenses)+" | "+ str(response['value']['cid']))
            cids.append(response['value']['cid'])

        print("Total licenses imported :"+str(totalLicenses))
        print("The Import Ended at: "+str(time.time()))
        f = open("SPDX-license-list-cids.json", "w")
        f.write(json.dumps(spdx_cids))

# importByResourceFile()/

import requests
import json

def importByResourceUrl(url):

    response = requests.get(url)
    data = json.loads(response.text)
    print(data)

# importByResourceUrl('https://raw.githubusercontent.com/spdx/license-list-data/master/json/licenses.json')