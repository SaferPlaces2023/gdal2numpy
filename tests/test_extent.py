import os
import unittest
import warnings
from gdal2numpy import *
from pyproj import Transformer
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


    def test_extent_from_file(self):
        """
        text_extent_from_file: 
        """
        filetif = f"{workdir}/LIDAR_REGIONE-VENETO_100601.tif"
        ext = GetExtent(filetif, "EPSG:4326")
        print("========================================")
        print(ext)
        self.assertTrue(True)




    # def test_extent(self):
    #     """
    #     test_extent: 
    #     """
        
    #     filer = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Ambiental_Italy_FloodMap_Fluvial_20yr_v1_0.cog.tif"
    #     #filer = "lidar_rimini_building_2.cog.tif"
    #     #ext = GetExtent([44, 12, 44.5,12.5], t_srs="EPSG:32633")
    #     #ext = GetExtent([12,44,12.5,44.5], t_srs="EPSG:32633")
    #     bbox = [12.1183605, 46.0362704, 12.3067003, 46.2335995]
    #     ext = GetExtent(bbox, t_srs="EPSG:3035")
    #     print(ext)

        

    #     # Define the original and target coordinate systems
    #     original_crs = 'EPSG:4326'  # WGS84
    #     target_crs = 'EPSG:3035'    # ETRS89 / LAEA Europe

    #     # Create a transformer object
    #     transformer = Transformer.from_crs(original_crs, target_crs)

    #     # Example coordinates (longitude, latitude)
    #     lon, lat = 12, 44  # Example: 12°E, 44°N

    #     # Transform the coordinates
    #     easting, northing = transformer.transform(lat, lon)

    #     # Print the transformed coordinates (X, Y)
    #     print(f"Easting (X): {easting}, Northing (Y): {northing}")
        


    
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


    # def test_transform_fluvial(self):
    #     file_fluvial = "https://s3.amazonaws.com/saferplaces.co/Ambiental/Fluvial/Italy_FloodMap_Fluvial_20yr_historical_v1_0.cog.tif"
    #     file_cropped = f"{workdir}/data/cropped.tif"
    #     minx,miny,maxx,maxy = (12.52962, 44.01098, 12.60526, 44.1151)

    #     ds = OpenRaster(file_fluvial)
    #     gt = ds.GetGeoTransform()
    #     ds=None
    #     print("gt:", gt)

    #     s_srs = GetSpatialRef("EPSG:4326")
    #     t_srs = GetSpatialRef("EPSG:3035")
        
    #     transformed_bbox = TransformBBOX((minx,miny,maxx,maxy),s_srs,t_srs)

    #     data, gt, prj = GDAL2Numpy(file_fluvial,bbox=transformed_bbox)
    #     Numpy2GTiff(data,gt,prj,fileout=file_cropped)

    #     self.assertTrue(os.path.exists(file_cropped))   


if __name__ == '__main__':
    unittest.main()



