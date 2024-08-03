import unittest
import requests
from remap_plate_info import VehicleStats


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.plate = 'SC06LMM'
        self.website = r'https://totalcarcheck.co.uk/FreeCheck?regno='
        self.vehicle_class = VehicleStats('SCO6LMM')

    def test_website(self):
        self.car_check = requests.get(self.website + self.plate)
        self.assertEqual(self.car_check.status_code, 200)  # add assertion here


if __name__ == '__main__':
    unittest.main()
