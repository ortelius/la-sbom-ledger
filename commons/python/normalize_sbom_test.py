from utils import *
from normalize_sbom import *


# Normalize data play book
f = open('./../../test/resource/sample_sbom.json')
data = json.load(f)
normalized_data = normalize(data)
# print(normalized_data)
assert str(normalized_data["purl"]) == 'pkg:pypi/click@7.1.2'
assert str(normalized_data["details"]) == 'ipfs://bafkreidmsjgxlcf4xk5xej6vquzscij75n7ur5bnhitefwz7ijuzmdmohm'
assert str(normalized_data["licenses"]) == '[\'ipfs://bafkreihfljjoqq3axkn6aw4iw5bqz4vaeemfunm5iauyfee2laslvgjdtq\']'

# Transpose method
f = open('./../../test/resource/sample_sbom.json')
data = json.load(f)
wrapped_data = encode_into_cid(data)
# print(wrapped_data)
assert str(wrapped_data["hashes"]) == '[\'ipfs://bafkreiemykbq2qp5swpzke5e3vpzb7ym776nq7i5ixlhbg6fmht4z7jqlq\', \'ipfs://bafkreidoydt6m7aqtfmij63hchaf6i3flxhphtoe5sps2qsd5nngexenia\']'
assert str(wrapped_data["licenses"]) == '[\'ipfs://bafkreihfljjoqq3axkn6aw4iw5bqz4vaeemfunm5iauyfee2laslvgjdtq\']'
assert str(wrapped_data["meta"]) == 'ipfs://bafkreibzgrwkfk63gfvwq7gdieadyqk7ngp3jv6fn7hhlchzmzaf4anktq'


f = open('./../../test/resource/sample_sbom.json')
data = json.load(f)
cid = convert_object_to_cid(encode_into_cid(data))
assert cid == 'ipfs://bafkreiambdxmzt5gpfw5pjdywvhp2x2komebu2bxmdh5sq7bdd6midmhhi'

# Un-wrap NFT
f = open('./../../test/resource/wraped_nft.json')
data = json.load(f)
unwrapped_data = decode_into_json(data)
assert str(unwrapped_data["hashes"]) == '[{\'alg\': \'MD5\', \'content\': \'b4233221cacc473acd422a1d54ff4c41\'}, {\'alg\': \'SHA-256\', \'content\': \'dacca89f4bfadd5de3d7489b7c8a566eee0d3676333fbb50030263894c38c0dc\'}]'
assert str(unwrapped_data["licenses"]) == '[{\'license\': [{\'license\': {\'name\': \'BSD-3-Clause\'}}]}]'
assert str(unwrapped_data["modified"]) == '{\'type\': \'library\'}'


