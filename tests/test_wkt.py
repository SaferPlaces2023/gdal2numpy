import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/data/CLSA_LiDAR.tif"
fileshp = f"{workdir}/test_building.shp"

class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_wkt(self):
        """
        test_read 
        """
        #code = GetSpatialRef(fileshp)
        #print(code)

        filename = r"D:\Users\vlr20\Projects\GitHub\saferplaces\saferplaces-4.0\mnt\efs\projects\valluzzi@gmail.com\DigitalTwin_20240214\catania.tif"
        code = AutoIdentify(filename)
        print(code)


if __name__ == '__main__':
    unittest.main()



