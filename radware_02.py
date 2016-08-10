#!/usr/bin/python3

#should run from the commandline via prameter, which is the address for search
#ex: python3 radware_02.py "20 Louis Marshall Tel Aviv-Yafo, Israel"
#The quatation are not necessary.


import re
import sys
import json
import unittest
from urllib.request import urlopen

class AddresDetails(unittest.TestCase):

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
            address = " ".join(address)
            return address
        return None


    def test_check_if_address_is_too_short(self):
        address = AddresDetails().test_check_if_request_address_is_empty()
        if address is not None:
            address = address.split()
            address_length = len(address)
            self.assertGreater(len(address),3,"partial address was given in the parameter output might become biased")


    def test_getAddress(self):
        global place_id
        address = AddresDetails().test_check_if_request_address_is_empty()
        address = re.sub(" ", "+", address)
        # request the address data by giving the address value - which was given by the user via the commandline
        response = urlopen( \
            "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key=" + key).read() \
            .decode('utf-8')
        responseJson = json.loads(response)
        full_address = responseJson.get("results")[0].get("formatted_address")
        place_id = responseJson.get("results")[0].get("place_id")
        location = responseJson.get("results")[0].get("geometry").get("location")
        lattitude = location.get('lat')
        langtitude = location.get('lng')
        # cleans unnecessary spaces
        full_address = " ".join(full_address.split())
        return [full_address, lattitude, langtitude, place_id]

    def test_getAddressByPlacID(self):
        # request the address data by giving the place_id value
        response = urlopen("https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + \
                           "&key=" + key).read().decode('utf-8')
        responseJson = json.loads(response)
        full_address_by_place_id = responseJson.get("result").get("adr_address")
        # the following code line cleans all unnecessary strings from the address in order
        # it will be comparable with the address result of the preceding function
        full_address_by_place_id = re.sub('(<|span|class|>|\/|\"|street-address|=|country-name|locality|" ")', "",
                                          full_address_by_place_id)
        full_address_by_place_id = " ".join(full_address_by_place_id.split())
        location = responseJson.get("result").get("geometry").get("location")
        lattitude = location.get('lat')
        langtitude = location.get('lng')
        return [full_address_by_place_id, lattitude, langtitude, place_id]

        # compare the two address which were drawn by the 2 previous functions
    def test_compare_Address_output(self):
        full_address = AddresDetails().test_getAddress()[0]
        full_address_by_place_id = AddresDetails().test_getAddressByPlacID()[0]
        # print(full_address)
        # print(full_address_by_place_id)
        self.assertEqual(full_address, full_address_by_place_id)

        # compare the two location data (langtitude and altitude) which were drawn by previous functions
    def test_compare_geo_location_output(self):
        geo_location_by_address = AddresDetails().test_getAddress()[1:3]
        geo_location_by_place_id = AddresDetails().test_getAddressByPlacID()[1:3]
        # print(geo_location_by_address)
        # print(geo_location_by_address)
        self.assertEqual(geo_location_by_address, geo_location_by_place_id)


if __name__ == '__main__':
    import sys
    unittest.main(verbosity=2, argv=[sys.argv[0]])









