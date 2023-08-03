import unittest
from gdal2numpy import *

fileshp = f"{justpath(__file__)}/data/pourpoints.shp"
class TestFeatures(unittest.TestCase):
    """
    Tests for the TestFeatures function
    """

    def test_get_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        result = GetFieldNames(fileshp)
        # pourpoints shape file fields
        self.assertEqual(result, ['bspot_id', 'type', 'cell_row', 'cell_col', 'bspot_dmax', 'bspot_area', 'bspot_vol', 'wshed_area', 'bspot_fumm'])


    def test_get_numeric_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        result = GetNumericFieldNames(fileshp)
        # pourpoints shape file numeric fields
        self.assertEqual(result, ['bspot_id','cell_row','cell_col','bspot_dmax','bspot_area','bspot_vol','wshed_area','bspot_fumm']) #['value_m2', 'mit_par', 'fdamage', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19']


    def test_get_range(self):
        """
        test_get_range: test that the function returns the correct range
        """
        result = GetRange(fileshp, "bspot_fumm")
        self.assertEqual(result, (0.24261598133745807, 1571.7536204216055))


    def test_get_features(self):
        """
        test_get_features: test that the function returns the correct features
        """
        result = GetFeatures(fileshp)
        n = GetFeatureCount(fileshp)
        self.assertEqual(len(result), n)

    def test_same_srs(self):
        """
        test_same_srs: test that the function returns the correct features
        """
        self.assertTrue(SameSpatialRef(fileshp, "EPSG:32633"))

    def test_transform(self):
        """
        test_transform: test that the function returns the correct features
        """
        fileout = f"{justpath(__file__)}/data/pourpoints_transformed.shp"
        Transform(fileshp, "EPSG:3857",fileout=fileout)
        
        self.assertTrue(SameSpatialRef(fileout, "EPSG:3857"))
        self.assertEqual(GetFeatureCount(fileout), GetFeatureCount(fileshp))
        os.remove(fileout)


if __name__ == '__main__':
    unittest.main()



