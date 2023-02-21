import unittest

from utils import *
from normalize_sbom import *


f = open('./../../test/resource/sample_sbom.json')
denormalized_data = json.load(f)
expected_normalized_data = ['ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm','ipfs://bafkreiezkbcsvmmskosikhwfgot6reopiu5yvx5zyu6xdjtonf3rvotzui']

class TestFuntionalCases(unittest.TestCase):

    def test_normalize(self):
        actual_normalized_data = normalize(denormalized_data)
        print(actual_normalized_data)
        self.assertTrue(actual_normalized_data != None)
        self.assertEqual(actual_normalized_data, expected_normalized_data)

    def test_de_normalize(self):
        actual_denormalized_data = de_normalize(expected_normalized_data)
        print(actual_denormalized_data)
        self.assertTrue(actual_denormalized_data != None)
        self.assertEqual(denormalized_data, actual_denormalized_data)

    def test_create_hash_code_after_sorting_key(self):
        response_from_unsorted = save('../../test/resource/un_sorted_key_sbom.json', 'file')
        print(response_from_unsorted)
        self.assertTrue(response_from_unsorted['ok'])
        
        sorted_sbom = {'abc': {'xyz': 'pqr'}, 'licenses': [{'abc': {'xyz': 'pqr'}, 'hash': 'undefined', 'license': [1.0, 4, 4556], 'repeate': {'abc': {'xyz': 'pqr'}, 'licenses': [{'abc': {'xyz': 'pqr'}, 'license': {'name': 'BSD-3-Clause'}}]}}]}

        response_from_sorted = save(sorted_sbom, 'json')
        self.assertTrue(response_from_sorted['ok'])

        self.assertEqual( response_from_unsorted['value']['cid'],  response_from_sorted['value']['cid'])

    def test_get_data_from_cid(self):
        response = getData("bafkreibcqaowdyb47fqzlsk5lsj74uhnu6gfqecpswv2m3kmw2cbkkq2be")
        self.assertEqual(response, '{"licenses":[{"license":{"name":"BSD-3-Clause"}}]}')

    def test_get_exception_when_saving_invalid_type_data(self):
        response = save({}, 'xml')
        self.assertRaises(Exception)

    def test_get_minimized_data_sorted_by_key(self):
        f = open('./../../test/resource/un_sorted_key_sbom.json')
        data_1 = json.load(f)
        parsedJsonString_1 = get_minimize_data(data_1)

        expected_json = {"abc":{"xyz":"pqr"},"licenses":[{"abc":{"xyz":"pqr"},"hash":"undefined","license":[1.0,4,4556],"repeate":{"abc":{"xyz":"pqr"},"licenses":[{"abc":{"xyz":"pqr"},"license":{"name":"BSD-3-Clause"}}]}}]}

        self.assertEqual(parsedJsonString_1, get_minimize_data(expected_json))


class TestNormalization(unittest.TestCase):

    def test_normalize_dict(self):
        denormalized_sample_data = {"Domain":{"name":"GLOBAL","_key":"ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe"},"_key":"ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm"}

        actual_normalized_data = normalize(denormalized_sample_data)
        print(actual_normalized_data)
        self.assertTrue(actual_normalized_data != None)
        self.assertEqual(actual_normalized_data, {'Domain': 'ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe', '_key': 'ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm'})


    def test_normalize_inner_list_of_dict(self):
        denormalized_sample_data = {"Domain":[{"name":"GLOBAL","_key":"ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe"}],"_key":"ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm"}

        actual_normalized_data = normalize(denormalized_sample_data)
        print(actual_normalized_data)
        self.assertTrue(actual_normalized_data != None)
        self.assertEqual(actual_normalized_data, {'Domain': ['ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe'], '_key': 'ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm'})

    def test_normalize_inner_dict_of_list(self):
        denormalized_sample_data = {'Domain': {'name': [{'Domain': {'name': 'GLOBAL', '_key': 'ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe'}, '_key': 'ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm'}], '_key': 'ipfs://bafkreig2wy2azfwdmiztgtzk6w4y4ogkgv7c73z3oxkszjdeeidns5ahbi'}}

        actual_normalized_data = normalize(denormalized_sample_data)
        print(actual_normalized_data)
        self.assertTrue(actual_normalized_data != None)
        self.assertEqual(actual_normalized_data, {'Domain': 'ipfs://bafkreig2wy2azfwdmiztgtzk6w4y4ogkgv7c73z3oxkszjdeeidns5ahbi'})

class TestDeNormalization(unittest.TestCase):

    def test_denormalize_dict(self):
        normalized_sample_data = {'Domain': 'ipfs://bafkreibogvzy2xbooigla4szw2vmf32jrdk2vktasxaq3ofterppafwlom'}

        actual_denormalized_data = de_normalize(normalized_sample_data)
        print(actual_denormalized_data)
        self.assertTrue(actual_denormalized_data != None)
        self.assertEqual(actual_denormalized_data, {'Domain': {'_key': 'ipfs://bafkreibogvzy2xbooigla4szw2vmf32jrdk2vktasxaq3ofterppafwlom', 'name': 'GLOBAL'}})


    def test_denormalize_inner_list_of_dict(self):
        normalized_sample_data = {'Domain': ['ipfs://bafkreibogvzy2xbooigla4szw2vmf32jrdk2vktasxaq3ofterppafwlom']}

        actual_denormalized_data = de_normalize(normalized_sample_data)
        print(actual_denormalized_data)
        self.assertTrue(actual_denormalized_data != None)
        self.assertEqual(actual_denormalized_data, {'Domain': [{'_key': 'ipfs://bafkreibogvzy2xbooigla4szw2vmf32jrdk2vktasxaq3ofterppafwlom', 'name': 'GLOBAL'}]})

    def test_denormalize_inner_dict_of_list(self):
        normalized_sample_data = {'Domain': 'ipfs://bafkreig2wy2azfwdmiztgtzk6w4y4ogkgv7c73z3oxkszjdeeidns5ahbi'}

        actual_denormalized_data = de_normalize(normalized_sample_data)
        print(actual_denormalized_data)
        self.assertTrue(actual_denormalized_data != None)
        self.assertEqual(actual_denormalized_data, {'Domain': {'name': [{'Domain': {'name': 'GLOBAL', '_key': 'ipfs://bafkreih3vbybn5o55rg2pufeacphemhimjoltfrgtqicrngmem5k44cjqe'}, '_key': 'ipfs://bafkreihcaehhl6k2ekd37dqaj6rqegdq5hcelr7ly4aupaenkqdm4wucfm'}], '_key': 'ipfs://bafkreig2wy2azfwdmiztgtzk6w4y4ogkgv7c73z3oxkszjdeeidns5ahbi'}})

if __name__ == '__main__':
    unittest.main()