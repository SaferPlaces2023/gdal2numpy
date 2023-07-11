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

    
    def test_open(self):
        """
        test_open: 
        """
        fileshp = "s3://saferplaces.co/test/barrier.shp"
        
        #ds = OpenShape(fileshp)
        #self.assertTrue(ds is not None)


    def test_copy_schema(self):
        """
        test_copy_schema: 
        """
        fileshp = "s3://saferplaces.co/test/barrier.shp"
        fileout = "tests/barrier_schema.shp"
        
        FeatureSelection(fileshp, fileout, fids=[1])
        #self.assertTrue(GetFeatureCount(fileout) == 1)


if __name__ == '__main__':
    unittest.main()



