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

        filerain = "s3://saferplaces.co/Venezia/COSMO-2I_tp/2024-09-18/00-00/forecast_acc_6h_2024-09-18_00-00_13h-18h.tif"
        filedem =  "s3://saferplaces.co/Venezia/dtm_bacino3.bld.tif"
        fileout = f"crop.tif"
        #projWin = [25.3137, -10.6103, 25.6596, -10.8433]
        projWin = [783785, 4885325 , 784795, 4886006]
        projWin = GetExtent(filedem)
        projWinSrs = "EPSG:3003"
        fileout = None # "ab/cropped.tif"
        print(projWin)
        
        fileout = gdal_translate(filerain, fileout=fileout, projwin=projWin, projwin_srs=projWinSrs, format="GTiff")
        print(fileout)
        self.assertTrue(isfile(fileout))

    

if __name__ == '__main__':
    unittest.main()



