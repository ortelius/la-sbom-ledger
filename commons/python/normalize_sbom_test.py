from utils import *
from normalize_sbom import *

# Normalize data play book

f = open('./../../test/resource/sample_sbom_normalization.json')
data_1 = json.load(f)
json_data = normalize_sbom_json(data_1)
print(json_data)

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

