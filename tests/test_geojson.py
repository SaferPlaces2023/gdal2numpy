import os
import unittest
from gdal2numpy import *

workdir = justpath(__file__)

fileshp = f"{workdir}/geojson.shp"


class Test(unittest.TestCase):
    """
    Tests
    """
    def test_features(self):
        """
        test_raster: 
        """
        f1 = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [125.6, 10.1]
            },
            "properties": {
                "name": "Dinagat Islands",
                "level":  123,
                "level2": 2223333.333,
            }
        }

        f2 ={
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [125.6, 10.1]
            },
            "properties": {
                "name": "Haiti Islands",
                "level":  5478,
                "level2": 222.33,
            }
        }
        features = [f1, f2]
        ShapeFileFromGeoJSON(features, fileshp)

if __name__ == '__main__':
    unittest.main()



