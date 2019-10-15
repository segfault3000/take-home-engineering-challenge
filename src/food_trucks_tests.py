import unittest
import food_trucks


class FoodTrucksTest(unittest.TestCase):
    def test_lookup(self):
        ft = food_trucks.FoodTrucks("./rqzj-sfat.geojson")
        ret = ft.suggest()

        self.assertIsNotNone(ret)


if __name__ == '__main__':
    unittest.main(buffer=True)

