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
        
        ds = OpenShape(fileshp)
        self.assertTrue(ds is not None)


    def test_opentext(self):
        """
        test_opentext: 
        """
        filetxt = f"{workdir}/geojson.prj"
        filetxt = f"https://s3.amazonaws.com/saferplaces.co/fdamage/shared/residential.csv"
        filetxt = f"s3://saferplaces.co/fdamage/shared/residential.csv"
        
        text = get(filetxt)
        print(f"text is <{text}>")
        
        self.assertTrue(text is not None)


if __name__ == '__main__':
    unittest.main()



