from pydantic import BaseModel
from typing import Optional
from nft_storage_utils import *
import re
import coloredlogs, logging

# Create a logger object.
logger = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG')


# This method will wrap json object and store all the nested objects as NFT recersively
def normalize(sbom):

    if(isinstance(sbom, dict)):
        for key in sbom:
            if ( isinstance(sbom[key], dict)):
                sbom[key] = convert_object_to_cid(sbom[key])

            elif (isinstance(sbom[key], list)):
                list_of_element = []
                for elem in sbom[key]:
                    list_of_element.append(convert_object_to_cid(elem))
                sbom[key] = list_of_element
    
    elif(isinstance(sbom, list)):
        list_of_cids = []
        for elem in sbom:
            list_of_cids.append(convert_object_to_cid(elem))
        return list_of_cids
    return sbom

def convert_object_to_cid(jsonData):
    if(isinstance(jsonData, list)):
        list_of_cids = []
        for elem in jsonData:
            list_of_cids.append(convert_object_to_cid(elem))
        return list_of_cids

    elif (isinstance(jsonData, dict) and detect_inner_object(jsonData)):
        # logger.debug("++ inner_object found inside ++" + str(jsonData))
        for key in jsonData:
            if (isinstance(jsonData[key], dict)):
                jsonData[key] = convert_object_to_cid(jsonData[key])
                get_clean_json(jsonData)
                minified_json_element = get_minimize_data(jsonData)
                response = save(minified_json_element, 'json')
                return "ipfs://" + response['value']['cid']

            elif (isinstance(jsonData[key], list)):
                list_of_element = []
                for elem in jsonData[key]:
                    list_of_element.append(convert_object_to_cid(elem))
                jsonData[key] = list_of_element
                get_clean_json(jsonData)
                minified_json_element = get_minimize_data(jsonData)
                response = save(minified_json_element, 'json')
                return "ipfs://"+ response['value']['cid']
    elif(isinstance(jsonData, dict)):
        get_clean_json(jsonData)
        minified_json_element = get_minimize_data(jsonData)
        response = save(minified_json_element, 'json')
        cid = response['value']['cid']
        return "ipfs://"+ str(cid)
    
    else:
        return jsonData

def get_clean_json(json):
    json.pop('_key', 'No Key found')

def detect_inner_object(jsonData):
    # logger.debug("++ traversing inside Object ++")
    for key in jsonData:
        
        if (isinstance(jsonData[key], dict) or isinstance(jsonData[key], list)):
            return True

def convert_to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


# Unwrap nft data to actual nested Json Object

def de_normalize(sbom):
    if(isinstance(sbom, list)):
        list_of_element = []
        for each_obj in sbom:
            list_of_element.append(decode_nft_helper(each_obj))
        
        return list_of_element

    elif(isinstance(sbom, dict)):
        return decode_nft_helper(sbom)

    return sbom

def decode_nft_helper(sbom):
    if(isinstance(sbom, dict)):
        for key in sbom:
            if (isinstance(sbom[key], str) and detect_nft(sbom[key]) != None):
                sbom[key] = convert_cid_to_object(sbom[key])

            elif(isinstance(sbom[key], list)):
                list_of_element = []
                for maybe_cid in sbom[key]:

                    if(detect_nft(maybe_cid) != None):
                        list_of_element.append(convert_cid_to_object(maybe_cid))
                    else:
                        list_of_element.append(maybe_cid)
                
                sbom[key] = list_of_element

    elif(isinstance(sbom, str) and detect_nft(sbom) != None):
        return convert_cid_to_object(sbom)

    return sbom

def convert_cid_to_object(cid):
    address = cid.split("://")[1]
    fetched_cid = json.loads(getData(address))
    
    fetched_cid_data = json.loads(fetched_cid)
    if(isinstance(fetched_cid_data, dict)):
        for key in fetched_cid_data:
            # logger.debug("detecting cids in --" + str(fetched_cid_data))
            if( isinstance(fetched_cid_data[key], str) and detect_nft(fetched_cid_data[key])):
                # logger.debug("---- unwraping again inside ----"+ str(fetched_cid_data))
                fetched_cid_data[key] = convert_cid_to_object(fetched_cid_data[key])
            elif(isinstance(fetched_cid_data[key], list)):
                list_of_element = []
                for maybe_cid in fetched_cid_data[key]:
                    if(detect_nft(maybe_cid) != None):
                        list_of_element.append(convert_cid_to_object(maybe_cid))
                    else:
                        list_of_element.append(maybe_cid)
                
                fetched_cid_data[key] = list_of_element

    fetched_cid_data['_key'] = cid
    return fetched_cid_data

ipfs_regex = r"^ipfs://Qm[1-9A-HJ-NP-Za-km-z]{44,}|^ipfs://b[A-Za-z2-7]{58,}|^ipfs://B[A-Z2-7]{58,}|^ipfs://z[1-9A-HJ-NP-Za-km-z]{48,}|^ipfs://F[0-9A-F]{50,}"

# this method checks if this value is valid IPFS url or not
def detect_nft(value):
    pattern = re.compile(ipfs_regex, re.IGNORECASE)
    return pattern.match(value)




