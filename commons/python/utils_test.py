import json
from utils import *


# Minimize data test case

f = open('./../../test/resource/sample_sbom_1.json')
data_1 = json.load(f)
parsedJsonString_1 = get_minimize_data(data_1)
assert parsedJsonString_1 == '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}'

f = open('../../test/resource/sample_sbom_2.json')
data_2 = json.load(f)
parsedJsonString_2 = get_minimize_data(data_2)
assert parsedJsonString_2 == '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}'

data_3 = {'licenses': [{"license": {"name": "BSD-3-Clause"}}]}
parsedJsonString_3 = get_minimize_data(data_3)
assert parsedJsonString_3 == '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}'

