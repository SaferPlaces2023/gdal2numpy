# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2022 Luzzi Valerio
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        rain.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     28/02/2022
# -------------------------------------------------------------------------------
import numpy as np
from osgeo import gdal, gdalconst
from osgeo import ogr


def RasterizeLike(file_shp, file_dem, file_tif="", dtype=None, burn_fieldname="", z_value=None, nodata=None):
    """
    RasterizeLike
    """
    dtypeOf = {
        'Float32': np.float32,
        'Float64': np.float64,
        'CFloat32': np.float32,
        'CFloat64': np.float64,
        'Byte': np.uint8,
        'Int16': np.int16,
        'Int32': np.int32,
        'UInt16': np.uint16,
        'UInt32': np.uint32,
        # ---
        np.int16: gdal.GDT_Int16,
        np.uint16: gdal.GDT_UInt16,
        np.int32: gdal.GDT_Int32,
        np.uint32: gdal.GDT_UInt32,
        np.float32: gdal.GDT_Float32,
        np.float64: gdal.GDT_Float64,

    }
    dataset = gdal.Open(file_dem, gdalconst.GA_ReadOnly)
    vector = ogr.OpenShared(file_shp)
    if dataset and vector:
        band = dataset.GetRasterBand(1)
        m, n = dataset.RasterYSize, dataset.RasterXSize
        gt, prj = dataset.GetGeoTransform(), dataset.GetProjection()
        nodata = band.GetNoDataValue() if nodata is None else nodata
        dtype = dtypeOf[dtype] if dtype else band.DataType
        _, px, _, _, _, py = gt

        # Open the data source and read in the extent
        layer = vector.GetLayer()

        # Create the destination data source
        CO = ["BIGTIFF=YES", "TILED=YES", "BLOCKXSIZE=256", "BLOCKYSIZE=256", 'COMPRESS=LZW'] if file_tif else []
        format = "GTiff" if file_tif else "MEM"
        driver = gdal.GetDriverByName(format)
        target_ds = driver.Create(file_tif, n, m, 1, dtype, CO)
        if gt is not None:
            target_ds.SetGeoTransform(gt)
        if prj is not None:
            target_ds.SetProjection(prj)
        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(nodata)
        band.Fill(nodata)

        # Rasterize
        if burn_fieldname:
            gdal.RasterizeLayer(target_ds, [1], layer, options=["ATTRIBUTE=%s" % (burn_fieldname.upper())])
        elif z_value is not None:
            gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[z_value])
        else:
            gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[1])

        data = band.ReadAsArray(0, 0, n, m)
        # data[data==nodata] = np.nan

        dataset, vector, target_ds = None, None, None
        return data, gt, prj

    print("file <%s> or <%s> does not exist!" % (file_shp, file_dem))
    return None, None, None
