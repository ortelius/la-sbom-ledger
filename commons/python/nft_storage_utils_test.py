from nft_storage_utils import *

response = save('../../test/resource/sample_sbom_1.json', 'file')
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be'

response = save('../../test/resource/sample_sbom_2.json', 'file')
assert response['ok'] == True
assert response['value']['cid'] == 'bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be'

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
