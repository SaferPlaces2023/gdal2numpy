import os
import unittest
import warnings
from gdal2numpy import *

workdir = justpath(__file__)

filetif = f"{workdir}/CLSA_LiDAR.tif"


class Test(unittest.TestCase):
    """
    Tests
    """
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)


    def test_load_from_s3(self):
        """
        test_s3: 
        """
        data, _, _ = GDAL2Numpy("https://s3.amazonaws.com/saferplaces.co/lidar-rer-100m.tif", load_nodata_as=np.nan)
        self.assertEqual(data.shape, (1458, 3616))


    def test_save_on_s3(self):
        """
        test_save_on_s3: 
        """
        data, gt, prj = GDAL2Numpy(filetif, load_nodata_as=np.nan)
        
        fileout = "s3://saferplaces.co/test/test.tif"
        Numpy2GTiff(data, gt, prj, fileout, save_nodata_as=-9999, format="GTiff")
        self.assertTrue(s3_exists(fileout))



if __name__ == '__main__':
    unittest.main()



