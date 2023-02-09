import nft_storage
from nft_storage.api import nft_storage_api
from utils import get_minimize_data
import yaml
from io import BytesIO, IOBase
import requests
import json

properties = yaml.safe_load(open('../../setup.yml'))

configuration = nft_storage.Configuration(
    host = properties['nft']['host']
)

configuration = nft_storage.Configuration(
    access_token = properties['nft']['API_KEY']
)

def save(data, type):
    with nft_storage.ApiClient(configuration) as client:
        storage = nft_storage_api.NFTStorageAPI(client)

        try:
            if(type == 'file'):
                fileData = open(data, 'rb')
                read_json = json.load(fileData)
                body = BytesIO(bytes(get_minimize_data(read_json), 'utf-8'))
            else :
                if(type == 'json'):
                    body = BytesIO(bytes(get_minimize_data(data), 'utf-8'))
                else:
                    raise Exception("Sorry, Ortelius do not support "+type+" as of now. Valid types are Json or file")

            return storage.store(body,  _check_return_type=False)

        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.save(): %s\n" % e)
            return e
        except Exception as e:
            print("Exception when calling nft_storage_utils.save(): %s\n" % e)
            return e

def check(cid):
    with nft_storage.ApiClient() as client:
        storage = nft_storage_api.NFTStorageAPI(client)
        try:
            return storage.check(cid, _check_return_type=False)
        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.check(): %s\n" % e)
            return e

def status(cid):
    with nft_storage.ApiClient(configuration) as api_client:
        storage = nft_storage_api.NFTStorageAPI(api_client)
        try:
            return storage.status(cid, _check_return_type=False)
        except nft_storage.ApiException as e:
            print("Exception when calling nft_storage_utils.status(): %s\n" % e)
            return e

def getData(cid):
    try:
        url = f"https://ipfs.io/ipfs/{cid}?format=json"
        response = requests.get(url)
        data = get_minimize_data(response.json())
        # print(data)
        return data
    except nft_storage.ApiException as e:
        print("Exception when calling nft_storage_utils.getData(): %s\n" % e)
        return e
