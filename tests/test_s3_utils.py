import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/CLSA_LiDAR.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)


    def test_download_s3(self):
        """
        test_s3: 
        """
        fileshp = copy("s3://saferplaces.co/test/barrier.shp")
        print("fileshp is:", fileshp)
        self.assertTrue(os.path.exists(fileshp))

    



if __name__ == '__main__':
    unittest.main()



