import get_minimize_data from './utils.mjs'

import data_1  from "../../test/resource/sample_sbom_1.json" assert {type: 'json'}
import data_2  from "../../test/resource/sample_sbom_2.json" assert {type: 'json'}

var data_3 = {
    "licenses": [
        {
            "license": {
                "name": "BSD-3-Clause"
            }
        }
    ]
}

var parsedJsonString_1 = get_minimize_data(data_1);
var parsedJsonString_2 = get_minimize_data(data_2);
var parsedJsonString_3 = get_minimize_data(data_3);

var requiredJsonString = '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}';

console.log(parsedJsonString_1 == requiredJsonString);
console.log(parsedJsonString_2 == requiredJsonString);
console.log(parsedJsonString_3 == requiredJsonString);
