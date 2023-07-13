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

    def test_extent(self):
        """
        test_upload_s3: 
        """
        filetif = f"{workdir}/lidar_rimini_building_2.tif"
        filer = "s3://ead.saferplaces.co/test/lidar_rimini_building_2.tif"
        ext1 = GetExtent(filetif)
        ext2 = GetExtent(filer)
        print("ext1 is:", ext1)
        print("ext2 is:", ext2)

   



if __name__ == '__main__':
    unittest.main()



