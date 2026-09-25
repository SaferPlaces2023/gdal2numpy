import os
import unittest
import numpy as np
from gdal2numpy import *

workdir = justpath(__file__)
workdir = f"D:/Users/vlr20/Projects/GitHub/saferplaces/saferplaces-4.0/mnt/efs/projects/valluzzi@gmail.com/Catania"
fileclay = "OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02_173830.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def test_s3(self):
        """
        test_rasterlike  
        """

        filerain = "s3://saferplaces.co/Venezia/ICON_2I_SURFACE_PRESSURE_LEVELS_tp/2026-09-09/00:00/accumulated_forecasts/forecast_acc_12h_2026-09-09_00-00_08h-19h.tif"
        filedem =  "s3://saferplaces.co/Venezia/dtm_bacino5.bld.tif"
        fileout =  "/tmp/crop.tif"
        
        fileout = RasterLike(filerain, filedem, fileout, format="GTiff", nodata=-9999)
        
        self.assertTrue(os.path.exists(fileout))
        self.assertEqual(GetPixelSize(fileout), GetPixelSize(filedem))
        self.assertEqual(GetSpatialRef(fileout).ExportToProj4(), GetSpatialRef(filedem).ExportToProj4())


if __name__ == '__main__':
    unittest.main()



