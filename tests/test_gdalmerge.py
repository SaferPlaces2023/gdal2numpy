import os,warnings
import unittest
from gdal2numpy import *

workdir = justpath(__file__)


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)



    def test_gdal_merge(self):
        """
        test_gdal_merge
        """
        #set_log_level(verbose=True,debug=True)
        
        file1 = f"{workdir}/12_2k_0015.tif"
        file2 = f"{workdir}/12_2k_0016.tif"
        fileout = f"{workdir}/12_2k_0015_0016.tif"

        wkdir = "c:\\users\\vlr20\\Downloads"
        file1 = f"{wkdir}/water_depth_bacino4.tif"
        file2 = f"{wkdir}/water_depth_bacino5.tif"
        fileout = f"{wkdir}/water_depth_bacino4_5.tif"
        fileout = gdal_merge([file1, file2], fileout)
        #gdal.BuildVRT(f"{wkdir}/tmp.vrt", [file1, file2], **{"srcNodata": -9999, "VRTNodata": -9999, "resampleAlg": "hello"})

if __name__ == '__main__':
    unittest.main()



