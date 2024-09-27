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
        #os.chdir(workdir)
        #filedem = f"NASA_NASADEM_HGT_001_162324.tif"
        #filerain = f"s3://saferplaces.co/test/lidar_rimini_building_2_wd.tif"
        #fileclay = f"OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02_160807.tif"

        filerain = "tests/forecast_acc_6h_2024-09-18_00-00_13h-18h.tif"
        # filerain = "tests/forecast_acc_6h_3003.tif"
        # filerain = "tests/forecast_acc_6h_3857.tif"
        filedem =  "s3://saferplaces.co/Venezia/dtm_bacino3.bld.tif"
        #filedem =  "tests/dtm_bacino3.bld.tif"
        fileout = f"crop.tif"
        projWin = GetExtent(filedem)
        projWinSrs = "EPSG:3003"
        fileout = None # "ab/cropped.tif"
          
        fileout = gdal_translate(filerain, fileout=fileout, projwin=projWin, projwin_srs=projWinSrs, format="GTiff")
        print(fileout)
        self.assertTrue(isfile(fileout))

    

if __name__ == '__main__':
    unittest.main()



