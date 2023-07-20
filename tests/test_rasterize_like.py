import os
import unittest
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
        filedem = f"s3://saferplaces.co/test/valerio.luzzi@gecosistema.com/test_dem_1689868333.tif"
        fileobm = f"s3://saferplaces.co/test/valerio.luzzi@gecosistema.com/test_building_1689868333.shp"
        fileout = f"{workdir}/out.tif"
        RasterizeLike(fileobm, filedem, fileout=fileout, z_value=10)
        #self.assertEqual(GetPixelSize(fileout), GetPixelSize(filetpl))

if __name__ == '__main__':
    unittest.main()



