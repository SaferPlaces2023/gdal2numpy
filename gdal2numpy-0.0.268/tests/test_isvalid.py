import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/data/CLSA_LiDAR.tif"
filetif = f"{workdir}/data/corrupted.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)


    def test_isvalid(self):
        """
        test_isvalid: 
        """
        self.assertTrue(IsValid(filetif))



if __name__ == '__main__':
    unittest.main()



