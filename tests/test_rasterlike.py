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
    def test_rasterlike_3857(self):
        """
        test_rasterlike  
        """
        epsg= 3857
        os.chdir(workdir)
        filedem = f"catania-{epsg}.tif"
        #fileclay = f"OpenLandMap_SOL_SOL_CLAY-4326.tif"
        fileout = f"clay-{epsg}.tif"
        
        fileout = RasterLike(fileclay, filedem, fileout, format="GTiff")
        
        self.assertTrue(os.path.exists(fileout))
        self.assertEqual(GetPixelSize(fileout), GetPixelSize(filedem))
        self.assertEqual(GetSpatialRef(fileout).ExportToProj4(), GetSpatialRef(filedem).ExportToProj4())
        #self.assertEqual(GetExtent(fileout), GetExtent(filedem))

    def test_rasterlike_32633(self):
        """
        test_rasterlike  
        """
        epsg= 32633
        os.chdir(workdir)
        filedem = f"catania-{epsg}.tif"
        #fileclay = f"OpenLandMap_SOL_SOL_CLAY-4326.tif"
        fileout = f"clay-{epsg}.tif"
        
        fileout = RasterLike(fileclay, filedem, fileout, format="GTiff")
        
        self.assertTrue(os.path.exists(fileout))
        self.assertEqual(GetPixelSize(fileout), GetPixelSize(filedem))
        self.assertEqual(GetSpatialRef(fileout).ExportToProj4(), GetSpatialRef(filedem).ExportToProj4())
    
    def test_rasterlike_3004(self):
        """
        test_rasterlike  
        """
        epsg= 3004
        os.chdir(workdir)
        filedem = f"catania-{epsg}.tif"
        #fileclay = f"OpenLandMap_SOL_SOL_CLAY-4326.tif"
        fileout = f"clay-{epsg}.tif"
        
        fileout = RasterLike(fileclay, filedem, fileout, format="GTiff")
        
        self.assertTrue(os.path.exists(fileout))
        self.assertEqual(GetPixelSize(fileout), GetPixelSize(filedem))
        self.assertEqual(GetSpatialRef(fileout).ExportToProj4(), GetSpatialRef(filedem).ExportToProj4())

if __name__ == '__main__':
    unittest.main()



