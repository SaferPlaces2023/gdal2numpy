import os
import unittest
import numpy as np
from gdal2numpy import *

workdir = justpath(__file__)
workdir = f"D:/Users/vlr20/Projects/GitHub/saferplaces/saferplaces-4.0/mnt/efs/projects/valluzzi@gmail.com/Congo2"

class Test(unittest.TestCase):
    """
    Tests
    """
    def test_gdal_translate(self):
        """
        test_gdal_translate  
        """
        os.chdir(workdir)
        filedem = f"NASA_NASADEM_HGT_001_162324.tif"
        filedem = f"s3://saferplaces.co/test/lidar_rimini_building_2_wd.tif"
        #fileclay = f"OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02_160807.tif"
        #projWin = [25.3137, -10.6103, 25.6596, -10.8433]
        projWin = [783785, 4885325 , 784795, 4886006]
        projWinSrs = "EPSG:32632"
        fileout = None # "ab/cropped.tif"
        
        fileout = gdal_translate(filedem, fileout=fileout, projwin=projWin)
        print(fileout)
        self.assertTrue(isfile(fileout))

    

if __name__ == '__main__':
    unittest.main()



