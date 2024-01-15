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

    def test_localip(self):
        """
        test_localip: 
        """
        myip = local_ip()
        print(myip)
        self.assertTrue(myip is not None)


    def test_whatsmyip(self):
        """
        test_whatsmyip: 
        """
        myip = whatsmyip()
        print(myip)
        self.assertTrue(myip is not None)



if __name__ == '__main__':
    unittest.main()



