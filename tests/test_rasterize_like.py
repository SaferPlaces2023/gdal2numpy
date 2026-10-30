import os
import unittest
import numpy as np
from gdal2numpy import *

workdir = justpath(__file__)


class Test(unittest.TestCase):
    """
    Tests
    """
  
    def test_rasterlike(self):
        """
        test_rasterlike  
        """
        filedem = f"s3://saferplaces.co/packages/gdal2numpy/rasterlike/lidar-rer4_11.53.01.tif"
        fileobm = f"s3://saferplaces.co/packages/gdal2numpy/rasterlike/OVERTURE_BUILDINGS_11.55.05.geojson"
        
        fileout = tempfilename("tmp_", ".tif")
        RasterizeLike(fileobm, filedem, fileout=fileout, z_value=10)
        self.assertTrue(os.path.exists(fileout))       
        self.assertEqual(GetRasterShape(filedem), GetRasterShape(fileout))
        self.assertTrue(SameSpatialRef(filedem, fileout))    

        if os.path.exists(fileout):
            os.unlink(fileout)

        print(f"Rasterized output saved to {fileout}")
        

if __name__ == '__main__':
    unittest.main()



