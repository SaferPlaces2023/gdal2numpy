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


    def test_isfile_s3(self):
        """
        test_isfile_s3: 
        """
        filetif = "s3://saferplaces.co/fdamage/shared/residential.csv"
        self.assertTrue(isfile(filetif))


    def test_isfile_http(self):
        """
        test_upload_s3: 
        """
        filetif = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Italy_FloodMap_Fluvial_100yr_historical_v1_0.cog.tif"
        self.assertTrue(israster(filetif))

    def test_isfile_shp(self):
        """
        test_upload_s3: 
        """
        fileshp = "s3://saferplaces.co/test/barrier.shp|barrier"
        self.assertTrue(isshape(fileshp))

    


if __name__ == '__main__':
    unittest.main()



