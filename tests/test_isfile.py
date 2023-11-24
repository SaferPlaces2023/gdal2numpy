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
        test_upload_s3: 
        """
        filetif = "s3://saferplaces.co/ead-api/12.4888776/43.9788354/12.6488776/44.1388354/rain/ssps1.2.6/2/damage_rt2.shp"
        self.assertTrue(isfile(filetif))


    def test_isfile_http(self):
        """
        test_upload_s3: 
        """
        filetif = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Ambiental_Italy_FloodMap_Fluvial_20yr_v1_0.cog.tif"
        self.assertTrue(isfile(filetif))


    


if __name__ == '__main__':
    unittest.main()



