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

    def test_rasterize_like1(self):
        """
        test_raster: 
        """
        #def RasterizeLike(fileshp, filedem, file_tif="", dtype=None, burn_fieldname="", \
        #          z_value=None, factor=1.0, nodata=None):
        fileshp = f"{workdir}/data/Rimini/barrier.shp"
        filedem = f"{workdir}/data/Rimini/MINAMBIENTE_ITALY_173447.bld.tif"
        fileout = f"{workdir}/data/Rimini/barrier1.tif"
        dem, _, _   = GDAL2Numpy(filedem, load_nodata_as=np.nan)
        data, _, _  = RasterizeLike(fileshp, filedem, fileout=None, burn_fieldname="height", nodata=0)
    
        print(np.unique(data))

        self.assertTrue(np.size(data) > 0)
        self.assertEqual(data.shape, dem.shape)


    # def test_rasterize_like2(self):
    #     """
    #     test_raster: 
    #     """
    #     #def RasterizeLike(fileshp, filedem, file_tif="", dtype=None, burn_fieldname="", \
    #     #          z_value=None, factor=1.0, nodata=None):
    #     fileshp = f"{workdir}/OSM_BUILDINGS_091244.shp"
    #     filedem = f"{workdir}/COPERNICUS.30.tif"
    #     fileout = f"{workdir}/OSM_BUILDINGS_091244R.tif"
    #     dem, _, _   = GDAL2Numpy(filedem, load_nodata_as=np.nan)
    #     data, _, _  = RasterizeLike(fileshp, filedem, fileout=fileout, nodata=0)

    #     print(np.unique(data))
    

    # def test_gdalwarp(self):
    #     """
    #     test_rasterlike  
    #     """
    #     filetif = f"s3://saferplaces.co/test/valerio.luzzi@gecosistema.com/test_landuse_1689924689.tif"
    #     fileout = f"s3://saferplaces.co/test/valerio.luzzi@gecosistema.com/test_landuse.tif"
    #     gdalwarp(filetif, fileout, dstSRS="EPSG:4326")
    #     self.assertTrue(isfile(fileout))


if __name__ == '__main__':
    unittest.main()



