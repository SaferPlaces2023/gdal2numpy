import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

fileshp = f"{workdir}/data/OSM_BUILDINGS_091244.shp"
filetif = f"{workdir}/data/CLSA_LiDAR.tif"
filedem = f"{workdir}/data/COPERNICUS.30.tif"

class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)


    def test_raster(self):
        """
        test_raster: 
        """
        data, _, _ = GDAL2Numpy(filetif, load_nodata_as=np.nan)
        self.assertEqual(data.shape, (1375, 1330))


    def test_pixel_size(self):
        """
        test_pixel_size:
        """
        #self.assertEqual((filedem), (22.0,30.9))
        pass


    def test_cog(self):
        """
        test_cog: 
        """
        fileout = forceext(filetif, "cog.tif")
        data, gt, prj = GDAL2Numpy(filetif, load_nodata_as=np.nan)
        Numpy2GTiff(data, gt, prj, fileout, save_nodata_as=-9999, format="COG", metadata={"UM": "meters", "type": "DTM"})
        cog, _, _ = GDAL2Numpy(fileout, load_nodata_as=np.nan)

        self.assertEqual(GetMetaData(fileout)["metadata"]["type"], "DTM")
        self.assertEqual(GetMetaData(fileout)["metadata"]["UM"], "meters")
        self.assertEqual(data.shape, cog.shape)
        os.remove(fileout)


if __name__ == '__main__':
    unittest.main()



