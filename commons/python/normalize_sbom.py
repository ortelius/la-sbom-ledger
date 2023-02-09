from pydantic import BaseModel
from typing import Optional
from nft_storage_utils import *


class Hashes(BaseModel):
    alg: Optional[str] = None
    content: Optional[str] = None

class PackageDetailsNFT(BaseModel):
    description: Optional[str] = None
    modified: Optional[bool] = None
    name: Optional[str] = None
    publisher: Optional[str] = None
    purl: Optional[str] = None
    type: Optional[str] = None
    vesion: Optional[str] = None
    hashes: Optional[Hashes] = None
    meta: Optional[dict] = None

class LicenseNFT(BaseModel):
    shortid: Optional[str] = None
    fullname: Optional[str] = None
    definitionurl: Optional[str] = None

# This method will normalize sbom josn to create multiple json data and store them as NFTs.
def normalize(json_data):
    license = json_data["licenses"]

    json_object = json.dumps(json_data, indent = 4) 
    package_details = PackageDetailsNFT(**json.loads(json_object))

    print(type(convert_to_dict(package_details)))
    return {
        "purl": json_data["purl"], 
        "details": normalize_helper(convert_to_dict(package_details)), 
        "licenses": normalize_helper(license)}


# This method will wrap json object and store all the nested objects as NFT recersively
def wrap_to_nft(jsonData):

    for key in jsonData:
        if (isinstance(jsonData[key], dict)):
            print("++ dict found ++" + str(jsonData[key]))
            jsonData[key] = normalize_helper(jsonData[key])
        elif (isinstance(jsonData[key], list)):
            list_of_element = []
            for elem in jsonData[key]:
                list_of_element.append(normalize_helper(elem))
            jsonData[key] = list_of_element
    return jsonData


def normalize_helper(jsonData):
    if(isinstance(jsonData, list)):
        list_of_cids = []
        for elem in jsonData:
            list_of_cids.append(normalize_helper(elem))
        return list_of_cids

    elif (detect_inner_object(jsonData)):
        print("++ inner_object found inside ++" + str(jsonData))
        for key in jsonData:
            if (isinstance(jsonData[key], dict)):
                jsonData[key] = normalize_helper(jsonData[key])
                print("++ creating cid for ++" + str(jsonData))
                minified_json_element = get_minimize_data(jsonData)
                response = save(minified_json_element, 'json')
                return response['value']['cid']

            elif (isinstance(jsonData[key], list)):
                list_of_element = []
                for elem in jsonData[key]:
                    list_of_element.append(normalize_helper(elem))
                jsonData[key] = list_of_element

                print("++ creating cid for ++" + str(jsonData))
                minified_json_element = get_minimize_data(jsonData)
                response = save(minified_json_element, 'json')
                return response['value']['cid']
    else:
        print("++ creating cid for ++" + str(jsonData))
        minified_json_element = get_minimize_data(jsonData)
        response = save(minified_json_element, 'json')
        return response['value']['cid']


def detect_inner_object(jsonData):
    print("++ traversing inside Object ++")
    for key in jsonData:
        if (isinstance(jsonData[key], dict) or isinstance(jsonData[key], list)):
            return True

def convert_to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))