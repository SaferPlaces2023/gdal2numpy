import os
import unittest
import warnings
from gdal2numpy import *
from osgeo import osr, ogr, gdal
workdir = justpath(__file__)

filetif = f"{workdir}/data/Rimini4326.tif"


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
        test_upload_s3: 
        """
        
        # filer = "s3://saferplaces.co/test/CLSA_LiDAR.tif"
        # copy(filetif, filer)
        ext1 = GetExtent(filetif, t_srs="EPSG:32633")
        ext2 = GetExtent(filetif)
        self.assertTrue(ext1 != ext2)


    def test_transform_fluvial(self):
        file_fluvial = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Ambiental_Italy_FloodMap_Fluvial_20yr_v1_0.cog.tif"
        file_cropped = f"{workdir}/data/cropped.tif"
        minx,miny,maxx,maxy = (12.52962, 44.01098, 12.60526, 44.1151)
        s_srs = GetSpatialRef("EPSG:4326")
        t_srs = GetSpatialRef("EPSG:3035")
        
        transformed_bbox = TransformBBOX((minx,miny,maxx,maxy),s_srs,t_srs)

        data, gt, prj = GDAL2Numpy(file_fluvial,bbox=transformed_bbox)
        Numpy2GTiff(data,gt,prj,fileout=file_cropped)

        self.assertTrue(os.path.exists(file_cropped))   


if __name__ == '__main__':
    unittest.main()



