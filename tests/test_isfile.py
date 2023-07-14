import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/data/CLSA_LiDAR.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    def test_isfile(self):
        """
        test_upload_s3: 
        """
        filer = "s3://ead.saferplaces.co/test/lidar_rimini_building_2.tif"
        self.assertTrue(isfile(filetif))


   


if __name__ == '__main__':
    unittest.main()



