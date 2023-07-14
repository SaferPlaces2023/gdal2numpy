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

    def test_cog(self):
        """
        test_cog: 
        """
        fileout = f"{workdir}/data/CLSA_LiDAR.cog.tif"
        GTiff2Cog(filetif, fileout)  
        self.assertTrue(os.path.exists(fileout))      


if __name__ == '__main__':
    unittest.main()



