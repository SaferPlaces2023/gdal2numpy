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

    def test_bbox(self):
        """
        test_read 
        """
        filetif = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Ambiental_Italy_FloodMap_Fluvial_20yr_v1_0.cog.tif"
        bbox = [44, 44.04, 12.00, 12.04]
        #bbox = [2242143, 4623539 , 2245687, 4630355]
        
        s_srs = GetSpatialRef(4326)
        s_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        t_srs = GetSpatialRef(3035)
        #t_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        

        transform = osr.CoordinateTransformation(s_srs, t_srs)
        bbox = Rectangle(*bbox)
        bbox.Transform(transform)
        bbox = list(bbox.GetEnvelope())
        #print(bbox)




        #bbox = [2242143, 4623539 , 2245687, 4630355]
        #data, gt, prj = GDAL2Numpy(filetif, bbox=bbox, load_nodata_as=0)
        #print(data.shape, gt, prj)


    # def test_cog(self):
    #     """
    #     test_cog: 
    #     """
    #     fileout = f"{workdir}/data/CLSA_LiDAR.cog.tif"
    #     GTiff2Cog(filetif, fileout)  
    #     self.assertTrue(os.path.exists(fileout))      


if __name__ == '__main__':
    unittest.main()



