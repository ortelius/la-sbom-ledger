from nft_storage_utils import *

response = save('../../test/resource/sample_sbom_1.json', 'file')
print(response)
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreidxuo3gms7zxtdl5dnrhjtbzql4jm622kywkdaddocba5y5ekmuz4'

response = save('../../test/resource/sample_sbom_2.json', 'file')
print(response)
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreidxuo3gms7zxtdl5dnrhjtbzql4jm622kywkdaddocba5y5ekmuz4'

josn_dict = {
    "licenses": [
        {
            "license": {
                "name": "BSD-3-Clause"
            }
        }
    ]
}
response = save(josn_dict, 'json')
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be'

response = check('bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be')
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be'

response = status(
    'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be')
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be'

response = save(josn_dict, 'xml')
assert type(response) == Exception

response = getData("bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be")
assert response == '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}'
