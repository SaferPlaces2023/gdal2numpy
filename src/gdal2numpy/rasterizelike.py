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
from .module_features import GetNumericFieldNames, Transform
from .module_s3 import copy, iss3
from .module_log import Logger

dtypeOf = {
    'Float32': np.float32,
    'Float64': np.float64,
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

def RasterizeLike(fileshp, filedem, fileout="", dtype=None, burn_fieldname="", \
                  z_value=None, factor=1.0, nodata=None):
    """
    RasterizeLike - Rasterize a shapefile like a raster file
    """
    gdal.SetConfigOption("SHAPE_RESTORE_SHX", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")

    filedem = copy(filedem) if iss3(filedem) else filedem
    print("filedem is:", filedem)
    fileshp = copy(fileshp) if iss3(fileshp) else fileshp
    print("fileshp is:", fileshp)
    fileshp = Transform(fileshp, filedem)
    print("fileshp is:", fileshp)
    print("=====================================")

    dataset = gdal.Open(filedem, gdalconst.GA_ReadOnly)
    vector = ogr.OpenShared(fileshp)
    if dataset and vector:
        band = dataset.GetRasterBand(1)
        m, n = dataset.RasterYSize, dataset.RasterXSize
        gt, prj = dataset.GetGeoTransform(), dataset.GetProjection()
        nodata = band.GetNoDataValue() if nodata is None else nodata
        dtype = dtypeOf[dtype] if dtype else band.DataType

        # Open the data source and read in the extent
        layer = vector.GetLayer()

        # Create the destination data source
        options = ["BIGTIFF=YES", "TILED=YES",
              "BLOCKXSIZE=256", "BLOCKYSIZE=256", 
              "COMPRESS=LZW"] if fileout else []
        format = "GTiff" if fileout else "MEM"
        driver = gdal.GetDriverByName(format)
        target_ds = driver.Create(fileout, n, m, 1, dtype, options)
        if gt is not None:
            target_ds.SetGeoTransform(gt)
        if prj is not None:
            target_ds.SetProjection(prj)
        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(nodata)
        band.Fill(nodata)

        fieldnames = GetNumericFieldNames(fileshp)
        # Rasterize
        if factor == 0.0:
            # if factor is 0 then burn 0, may be this does not have much sense
            gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[0.0])
        elif burn_fieldname and burn_fieldname in fieldnames and factor==1.0:
            # if factor is 1 then burn the field value
            gdal.RasterizeLayer(target_ds, [1], layer, options=[f"ATTRIBUTE={burn_fieldname.upper()}"])
        elif burn_fieldname and burn_fieldname in fieldnames and factor!=1.0:
            # if factor is not 1 then burn the field value multiplied by factor
            # in case of fieldname we have to pre multiply the each feature value by factor
            # To not modify the original layer we have to copy it in memory
            memds = ogr.GetDriverByName("Memory").CopyDataSource(vector, "tmp")
            layercpy = memds.GetLayer()
            for feature in layercpy:
                feature.SetField(burn_fieldname, feature.GetField(burn_fieldname) * factor)
                layercpy.SetFeature(feature)
            gdal.RasterizeLayer(target_ds, [1], layercpy, options=["ATTRIBUTE=%s" % (burn_fieldname.upper())])
            memds, layercpy = None, None
        elif z_value is not None:
            # in case we hav not fieldname we burn the z_value
            gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[z_value*factor])
        else:
            # in all other cases we burn 1
            gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[1])

        data = band.ReadAsArray(0, 0, n, m)

        dataset, vector, target_ds = None, None, None
        return data, gt, prj

    Logger.error(f"file <{fileshp}> or <{filedem}> does not exist!")
    return None, None, None
