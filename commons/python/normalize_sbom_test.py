from utils import *
from normalize_sbom import *

# Normalize data play book
f = open('./../../test/resource/sample_sbom.json')
data = json.load(f)
normalized_data = normalize(data)
print(normalized_data)


# Transpose method
f = open('./../../test/resource/sample_sbom.json')
data = json.load(f)
wrapped_data = wrap_to_nft(data)
print(wrapped_data)

# response = getData("bafkreifu26sd4estnvvhdfdpbo7d3uhporomde2s5tfjxubhroujxvpknu")
# print(json.loads(response))

# response = getData("bafkreibdufsv2jchm6sf3etpvfdin74lczia32qasj2an2da43mw432t2i")
# print(json.loads(response))

# response = getData("bafkreidoydt6m7aqtfmij63hchaf6i3flxhphtoe5sps2qsd5nngexenia")
# print(json.loads(response))

# response = getData("bafkreiemykbq2qp5swpzke5e3vpzb7ym776nq7i5ixlhbg6fmht4z7jqlq")
# print(json.loads(response))

# response = getData("bafkreicvt762evynfwf7hyplf5cssed6vud6mvzj6izob65n6whfv5yyru")
# print(json.loads(response))

