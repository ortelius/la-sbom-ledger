# nft_storage_utils

This is a wrapper written over nft.storage python client to save and get the NFT data from NFT storage.


# The requirements

Python >= 3.6

Set nft.host and nft.API_KEY in la-sbom-ledger\setup.yml.

Steps to create your own test API_KEY
-   Login to https://nft.storage/
-   Create API Key from https://nft.storage/manage/


# Installation
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/nftstorage/python-client.git
```

# Usage

| API   | Input Parameter                   |Usage                                    | Output Response                       |
| ----- | --------------------------------- | --------------------------------------- | ------------------------------------- |
| save  | data: fileName or Json String     |Store the Nft Data on Nft Storage.  |The standard Ntf.Storage response Json |
|       | type: file or json as per data    |                                         |The standard Ntf.Storage response Json |
| check | cid                               |Check if a CID of an NFT is being stored by nft.storage.  |The standard Ntf.Storage response Json |
| status| cid                               | Get information for the stored CID  |The standard Ntf.Storage response Json |


## The standard Ntf.Storage response Json sample for /save

```json
{'ok': True,
 'value': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
           'created': '2022-10-18T17:09:47.802+00:00',
           'deals': [{'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13504117,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-21T12:17:30+00:00',
                      'dealExpiration': '2024-03-14T12:17:30+00:00',
                      'lastChanged': '2022-10-21T03:33:22.743022+00:00',
                      'miner': 'f01345523',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'active',
                      'statusText': 'containing sector active as of 2022-10-21 '
                                    '03:17:00 at epoch 2267194'},
                     {'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13508322,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-22T05:47:30+00:00',
                      'dealExpiration': '2024-03-15T05:47:30+00:00',
                      'lastChanged': '2022-10-22T06:31:27.575975+00:00',
                      'miner': 'f0214334',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'terminated',
                      'statusText': 'containing sector missed expected sealing '
                                    'epoch 2270375'}],
           'files': [],
           'name': 'Upload at 2022-10-22T09:52:44.092Z',
           'pin': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
                   'created': '2022-10-18T17:09:47.802+00:00',
                   'size': 133,
                   'status': 'pinned'},
           'scope': 'test-api-key-utkarsh',
           'size': 133,
           'type': 'image/*'}}
```

## The standard Ntf.Storage response Json sample for /check

```json
{'ok': True,
 'value': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
           'deals': [{'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13504117,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-21T12:17:30+00:00',
                      'dealExpiration': '2024-03-14T12:17:30+00:00',
                      'lastChanged': '2022-10-21T03:33:22.743022+00:00',
                      'miner': 'f01345523',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'active',
                      'statusText': 'containing sector active as of 2022-10-21 '
                                    '03:17:00 at epoch 2267194'},
                     {'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13508322,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-22T05:47:30+00:00',
                      'dealExpiration': '2024-03-15T05:47:30+00:00',
                      'lastChanged': '2022-10-22T06:31:27.575975+00:00',
                      'miner': 'f0214334',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'terminated',
                      'statusText': 'containing sector missed expected sealing '
                                    'epoch 2270375'}],
           'pin': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
                   'created': '2022-10-18T17:09:47.802+00:00',
                   'size': 133,
                   'status': 'pinned'}}}
```
## The standard Ntf.Storage response Json sample for /status
```json
{'ok': True,
 'value': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
           'created': '2022-10-18T17:09:47.802+00:00',
           'deals': [{'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13504117,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-21T12:17:30+00:00',
                      'dealExpiration': '2024-03-14T12:17:30+00:00',
                      'lastChanged': '2022-10-21T03:33:22.743022+00:00',
                      'miner': 'f01345523',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'active',
                      'statusText': 'containing sector active as of 2022-10-21 '
                                    '03:17:00 at epoch 2267194'},
                     {'batchRootCid': 'bafybeie4urjvyryrlc2bpbew5rn3cspwum66i65hjyubnbnk3wkpn3zfgu',
                      'chainDealID': 13508322,
                      'datamodelSelector': 'Links/42/Hash/Links/2/Hash/Links/0/Hash',
                      'dealActivation': '2022-10-22T05:47:30+00:00',
                      'dealExpiration': '2024-03-15T05:47:30+00:00',
                      'lastChanged': '2022-10-22T06:31:27.575975+00:00',
                      'miner': 'f0214334',
                      'pieceCid': 'baga6ea4seaqoqsrqmhnz3lu32emw5ix2z52crmetitgfhib6vcctjmvcnkgsydi',
                      'status': 'terminated',
                      'statusText': 'containing sector missed expected sealing '
                                    'epoch 2270375'}],
           'files': [],
           'name': 'Upload at 2022-10-22T09:52:44.092Z',
           'pin': {'cid': 'bafkreidtxc3ej6nhfnnxnjglw24mcnypz3y36camu3fey3kucgrkoelg7a',
                   'created': '2022-10-18T17:09:47.802+00:00',
                   'size': 133,
                   'status': 'pinned'},
           'scope': 'test-api-key-utkarsh',
           'size': 133,
           'type': 'image/*'}}
```

# Testing

## Visit nft_storage_utils_test.py for the unit tests

Go inside the directory to run test 
`cd .\commons\python\`

Now run the test file
`python .\nft_storage_utils_test.py`