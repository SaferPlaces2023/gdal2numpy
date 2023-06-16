import os
import unittest
from gdal2numpy import *

workdir = justpath(__file__)

fileshp = f"{workdir}/OSM_BUILDINGS_091244.shp"
filedem = f"{workdir}/COPERNICUS.30.tif"
fileout = forceext(fileshp, "tif")

class Test(unittest.TestCase):
    """
    Tests
    """
    def test_rasterize_like(self):
        """
        test_raster: 
        """
        #def RasterizeLike(fileshp, filedem, file_tif="", dtype=None, burn_fieldname="", \
        #          z_value=None, factor=1.0, nodata=None):
        dem, _, _ = GDAL2Numpy(filedem, load_nodata_as=np.nan)
        data, _, _  = RasterizeLike(fileshp, filedem, burn_fieldname="height", nodata=0)
        self.assertEqual(data.shape, dem.shape)

    def test_rasterlike(self):
        """
        test_rasterlike  
        """
        filetif = f"{workdir}/OSM_BUILDINGS_091244R.tif"
        filetpl = f"{workdir}/COPERNICUS.30.tif"
        fileout = forceext(filetif, "30.tif")
        RasterLike(filetif, filetpl, fileout, resampleAlg="near", format="GTiff")
        self.assertEqual(GetPixelSize(fileout), GetPixelSize(filetpl))

if __name__ == '__main__':
    unittest.main()



