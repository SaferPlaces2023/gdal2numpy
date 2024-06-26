import os
import json
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


    def test_xml(self):
        """
        test_xml: 
        """
        fileshp = "pourpoints.shp"
        fileqmd = "pourpoints2.qmd"
        data = parseXML(fileqmd)
        # text  = json.dumps(data, indent=4)
        # print(text)
        writeQMD(fileshp)
        self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()



