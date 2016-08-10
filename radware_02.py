#!/usr/bin/python3

import re
import json
import unittest
from urllib.request import urlopen

class AddresDetails(unittest.TestCase):
    # global address
    global key
    key = "AIzaSyB_rTS7FwwpAnHk3yzAhK9OmLUfuPCH_SU"

        # test whether the request address, given by the user via the command line is missing
    def test_check_if_request_address_is_empty(self):
        global address
        # the address takes the parameter which was givien in the command line by the user
        address = sys.argv[0:]
        # test whether it is only one parameter, it means that this is the script name and no parameter was given
        self.assertGreater(len(address),1,"no parameter was given")
        if len(address) > 1:
            address = sys.argv[1:]
            # convert list into one string
            address = "".join(address)
            address = address.strip()
            return address
        return None

    def test_check_if_address_is_too_short(self):
        address = (self.test_check_if_request_address_is_empty())
        address = address.split()
        address_length = len(address)
        self.assertGreater(address_length, 3, "partial address was given in parameter - output might become biased")

        # check the request result's status
    def test_geo_request_status_check(self,req_type_param=None):
        if req_type_param == None:
            url_address = re.sub(" ", "+", address)
            response = urlopen( \
                 "https://maps.googleapis.com/maps/api/geocode/json?address=" + url_address + "&key=" + key).read() \
                 .decode('utf-8')
        else:
            url_address  = re.sub(" ", "+", req_type_param)
            response = urlopen("https://maps.googleapis.com/maps/api/place/details/json?placeid=" + req_type_param + \
                                                       "&key=" + key).read().decode('utf-8')
        responseJson = json.loads(response)
        if responseJson.get("status") == "OK":
            self.assertEqual(responseJson.get("status"), "OK", "Query status OK")
            return responseJson
        else:
            return None

    @property
    def req_by_address(self):
        global place_id
        global address_result
        global lattitude1
        global langtitude1
        global address_result_list
        global input_address_list
        responseJson = self.test_geo_request_status_check()
        if responseJson is not None:
            address_result = responseJson.get("results")[0].get("formatted_address")
            place_id = responseJson.get("results")[0].get("place_id")
            location = responseJson.get("results")[0].get("geometry").get("location")
            lattitude1 = location.get('lat')
            langtitude1 = location.get('lng')
            # preparing the data for proprt comparison; remove unnecessary commas and dashes
            address_result_no_commas = re.sub("(,|-)"," ", address_result.lower())
            address_result_list = address_result_no_commas.split()
            input_address_no_commas= re.sub("(,|-)"," ", address.lower())
            input_address_list =input_address_no_commas.split()
            return [address_result, lattitude1, langtitude1, place_id, \
                    address_result_list, address, input_address_list]

        #compare search results by address against search results by place_id
    def test_request_by_PlacID(self):
        data_set = self.req_by_address
        # address_result = data_set[0]
        place_id = data_set[3]
        responseJson = self.test_geo_request_status_check(place_id)
        address_by_place_id = responseJson.get("result").get("adr_address")
        # the following code line cleans all unnecessary strings from the address in order
        # it will be comparable with the address result of the preceding function
        address_by_place_id = re.sub('(<|span|class|>|\/|\"|street-address|=|country-name|locality|" ")', "",
                                          address_by_place_id)
        address_by_place_id = " ".join(address_by_place_id.split())
        location = responseJson.get("result").get("geometry").get("location")
        lattitude = location.get('lat')
        langtitude = location.get('lng')
        place_id_result = responseJson.get("result").get("place_id")
        self.assertEqual((address_by_place_id, lattitude, langtitude),\
                         (address_result, lattitude1, langtitude1), \
                         'failed when compared query results, which uses an address as input against\
                          one which uses place_id as input ')
        return [address_by_place_id, lattitude, langtitude, place_id]


    def test_compare_input_request_to_output_results(self):
        # comparison betwen input address and the address result
        req_by_address_data_set = self.req_by_address
        address_result_list = req_by_address_data_set[4]
        for i in address_result_list:
            self.assertIn(i, input_address_list, "\n" + 'request address and result address comparison:\n' + \
                          "requested address: " + address + '\n' + "result address:    " + address_result)

    def test_compare_output_results_to_input_request(self):
        # reverse check
        for i in input_address_list:
            self.assertIn(i, address_result_list, "\n" + "result address and request address comparison:\n" + \
                          "result address: " + address_result + "\n"+"requestedaddress: " \
                          + address + "\n")


if __name__ == '__main__':
    import sys
    unittest.main(verbosity=2, argv=[sys.argv[0]])









