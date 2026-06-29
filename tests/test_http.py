import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = "https://s3.us-east-1.amazonaws.com/saferplaces.co/packages/safer_rain/CLSA_LiDAR/CLSA_LiDAR.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)


    def test_http(self):
        """
        test_http:
        """
        dem, gt, prj = GDAL2Numpy(filetif)
        self.assertIsNotNone(dem)
        self.assertEqual(dem.shape, (1375, 1330))
        self.assertIsNotNone(gt)
        self.assertIsNotNone(prj)
        
if __name__ == '__main__':
    unittest.main()



