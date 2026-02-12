import os
import unittest
import warnings
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


    def test_copy(self):
        """
        test_copy
        """
        src = "https://s3.us-east-1.amazonaws.com/saferplaces.co/Directed/data-fabric-rwl2/barriers/df677def4d712fddececa32bfc23939a/barriers.geojson"
        src = "https://p5mtvmq5v0.execute-api.us-east-1.amazonaws.com/api/features/barriers.geojson"
        dst = f"{workdir}/barriers.geojson"
        copy(src, dst)
        assert(os.path.isfile(dst))

if __name__ == '__main__':
    unittest.main()



