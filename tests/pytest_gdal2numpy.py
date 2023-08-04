
from gdal2numpy import *    

workdir = justpath(__file__)
filedem = f"{workdir}/data/CLSA_LiDAR.tif"

def test_read():
    """
    test_read: 
    """
    data, gt, prj = GDAL2Numpy(filedem, load_nodata_as=np.nan)
    assert data.shape == (1375, 1330)