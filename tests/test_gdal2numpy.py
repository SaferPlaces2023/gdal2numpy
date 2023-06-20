import os
import unittest
import logging
from gdal2numpy import *

workdir = justpath(__file__)

fileshp = f"{workdir}/OSM_BUILDINGS_091244.shp"
filetif = f"{workdir}/CLSA_LiDAR.tif"
filedem = f"{workdir}/MINAMBIENTE_ITALY.tif"



class Test(unittest.TestCase):
    """
    Tests
    """
    def test_raster(self):
        """
        test_raster: 
        """
        mem_usage()
        data, _, _ = GDAL2Numpy(filedem, load_nodata_as=np.nan)
        print(f"Memory read:{data.size*4 / 1024**2} MB")
        mem_usage()

        

   


if __name__ == '__main__':
    unittest.main()



