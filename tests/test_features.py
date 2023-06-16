import unittest
from gdal2numpy import *

fileshp = f"{justpath(__file__)}/OSM_BUILDINGS_091244.shp"
class TestFeatures(unittest.TestCase):
    """
    Tests for the TestFeatures function
    """

    def test_get_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        result = GetFieldNames(fileshp)
        self.assertEqual(result, ['FID', 'height', 'descr', 'val', 'mit'])


    def test_get_numeric_fieldnames(self):
        """
        test_get_fieldnames: test that the function returns the correct field names
        """
        result = GetNumericFieldNames(fileshp)
        self.assertEqual(result, ['FID', 'height', 'val', 'mit'])


    def test_get_range(self):
        """
        test_get_range: test that the function returns the correct range
        """
        result = GetRange(fileshp, "height")
        self.assertEqual(result, (2.5, 10.0))


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
        self.assertTrue(SameSpatialRef(fileshp, "EPSG:4326"))

    def test_transform(self):
        """
        test_transform: test that the function returns the correct features
        """
        filetmp = Transform(fileshp, "EPSG:3857")
        self.assertTrue(SameSpatialRef(filetmp, "EPSG:3857"))
        self.assertEqual(GetFeatureCount(filetmp), GetFeatureCount(fileshp))
        os.remove(filetmp)


if __name__ == '__main__':
    unittest.main()



