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


    # def test_gdalwarp(self):
    #     """
    #     test_gdalwarp: 
    #     """
    #     print("test_gdalwarp")
    #     filedem = f"{workdir}/lidar_rimini_building_2.tif"
    #     fileout = f"{workdir}/lidar_rimini_building_2.warp.tif"
    #     gdalwarp(filedem, fileout, dstSRS=3857)
    #     self.assertTrue(isfile(fileout))


    # def test_gdalwarp_inplace(self):
    #     """
    #     test_gdalwarp_inplace  
    #     """
    #     print("test_gdalwarp_inplace")
    #     filedem = f"{workdir}/lidar_rimini_building_2.warp.tif"
    #     gdalwarp(filedem, dstSRS=7791)
    #     srs = GetSpatialRef(filedem)
    #     srsTarget = GetSpatialRef(7791)
    #     self.assertTrue(srs.IsSame(srsTarget))    

    # def test_gdalwarp_s3(self):
    #     """
    #     test_gdalwarp_s3  
    #     """
    #     print("test_gdalwarp_s3")
    #     filedem = f"s3://saferplaces.co/lidar-rer-100m.tif"
    #     fileout = f"{workdir}/lidar-rer-100m.warp.tif"
    #     gdalwarp(filedem, fileout, dstSRS=7791, format="COG")
    #     self.assertTrue(isfile(fileout))


    # def test_gdalwarp_s3_2_s3(self):
    #     """
    #     test_gdalwarp_s3_2_s3  
    #     """
    #     print("test_gdalwarp_s3_2_s3")
    #     filedem = f"s3://saferplaces.co/lidar-rer-100m.tif"
    #     fileout = f"s3://saferplaces.co/lidar-rer-100m.warp.tif"
    #     gdalwarp(filedem, fileout, format="COG")
    #     self.assertTrue(isfile(fileout))


    def test_if_is_cog(self):
        """
        test_if_is_cog
        """
        print("test_if_is_cog")
        filedem = f"{workdir}/lidar-rer-100m.warp.tif"
        
        
        self.assertTrue(is_cog(filedem))


if __name__ == '__main__':
    unittest.main()



