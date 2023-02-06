from pydantic import BaseModel
from nft_storage_utils import *


class Hashes(BaseModel):
    alg: str
    content: str

class PackageDetailsNFT(BaseModel):
    description: list
    modified: bool
    name: str
    publisher: str
    purl: str
    type: str
    vesion: str
    hashes: Hashes
    meta: dict


class LicenseNFT(BaseModel):
    shortid: str
    fullname: str
    definitionurl: str


class PackageNFT(BaseModel):
    purl: str
    details: str
    licenses: str


# This method will normalize sbom josn to create multiple json data and store them as NFTs.
def normalize_sbom_json(jsonData):

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
    print("++ traversing inside ++")
    if (detect_inner_object(jsonData)):
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
    for key in jsonData:
        if (isinstance(jsonData[key], dict) or isinstance(jsonData[key], list)):
            return True
