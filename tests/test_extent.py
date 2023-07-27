import os
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



    def test_extent(self):
        """
        test_extent: 
        """
        
        filer = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Ambiental_Italy_FloodMap_Fluvial_20yr_v1_0.cog.tif"
        #filer = "lidar_rimini_building_2.cog.tif"
        print(filer)
        ext = GetExtent(filer, t_srs=4326)
        print("ext is:", ext)
        minx, miny, maxx, maxy = ext
        r = Rectangle(miny,minx, maxy, maxx)
        print(r.ExportToWkb())
        

    
    # def test_extent_s3(self):
    #     """
    #     test_extent_s3: 
    #     """
        
    #     filer = "s3://saferplaces.co/test/CLSA_LiDAR.tif"
    #     copy(filetif, filer)
    #     ext1 = GetExtent(filetif)
    #     ext2 = GetExtent(filer)
    #     print("ext1 is:", ext1)
    #     print("ext2 is:", ext2)

   



if __name__ == '__main__':
    unittest.main()



