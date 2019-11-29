#-------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2020 Valerio for Gecosistema S.r.l.
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
# Name:        module.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:
#-------------------------------------------------------------------------------
import os,sys,math
import gdal,gdalconst
import numpy as np

def GetPixelSize(filename):
    """
    GetPixelSize
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        gt = dataset.GetGeoTransform()
        _, px, _, _, _, py = gt
        dataset = None
        return (px,py)
    return (0,0)

def GetRasterShape(filename):
    """
    GetRasterShape
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(1)
        m,n = dataset.RasterYSize,dataset.RasterXSize
        return (m,n)
    return (0,0)

def GetExtent(filename):
    """
    GetExtent
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        "{xmin} {ymin} {xmax} {ymax}"
        m,n  = dataset.RasterYSize,dataset.RasterXSize
        gt = dataset.GetGeoTransform()
        xmin,px,_,ymax,_,py = gt
        xmax = xmin + n*px
        ymin = ymax + m*py
        ymin,ymax = min(ymin,ymax),max(ymin,ymax)
        dataset=None
        return (xmin, ymin, xmax, ymax )
    return (0,0,0,0)

def GetSpatialReference(filename):
    """
    GetSpatialReference
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
       return dataset.GetProjection()
    return None

def GetNoData(filename):
    """
    GetNoData
    """
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        data, band, dataset = None, None, None
        return nodata
    return None

def GDAL2Numpy(pathname, band=1, dtype='', load_nodata_as = np.nan):
    """
    GDAL2Numpy
    """
    dataset = gdal.Open(pathname, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(band)
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()
        nodata = band.GetNoDataValue()
        bandtype = gdal.GetDataTypeName(band.DataType)

        wdata = band.ReadAsArray(0, 0, cols, rows)

        # translate nodata as Nan
        if not wdata is None:

            # Output datatype
            if dtype and dtype != bandtype:
                wdata = wdata.astype(dtype, copy=False)

            if bandtype in ('Float32', 'Float64', 'CFloat32', 'CFloat64'):
                if not nodata is None and abs(nodata) > 3.4e38:
                    wdata[abs(wdata) > 3.4e38] = load_nodata_as
                elif not nodata is None:
                    wdata[wdata == nodata] = load_nodata_as
            elif bandtype in ('Byte', 'Int16', 'Int32', 'UInt16', 'UInt32', 'CInt16', 'CInt32'):
                #wdata = wdata.astype("Float32", copy=False)
                if nodata != load_nodata_as:
                    wdata[wdata == nodata] = load_nodata_as

        band = None
        dataset = None
        return (wdata, geotransform, projection)
    print("file %s not exists!" % (pathname))
    return (None, None, None)

def Numpy2GTiff(arr, geotransform, projection, filename, save_nodata_as=-9999):
    """
    Numpy2GTiff
    """
    if isinstance(arr, np.ndarray):
        rows, cols = arr.shape
        if rows > 0 and cols > 0:
            dtype = str(arr.dtype)
            if dtype in ["uint8"]:
                fmt = gdal.GDT_Byte
            elif dtype in ["uint16"]:
                fmt = gdal.GDT_UInt16
            elif dtype in ["uint32"]:
                fmt = gdal.GDT_UInt32
            elif dtype in ["float32"]:
                fmt = gdal.GDT_Float32
            elif dtype in ["float64"]:
                fmt = gdal.GDT_Float64
            else:
                fmt = gdal.GDT_Float64

            CO = ["BIGTIFF=YES", "TILED=YES", "BLOCKXSIZE=256", "BLOCKYSIZE=256", 'COMPRESS=LZW']
            driver = gdal.GetDriverByName("GTiff")
            dataset = driver.Create(filename, cols, rows, 1, fmt, CO)
            if (geotransform != None):
                dataset.SetGeoTransform(geotransform)
            if (projection != None):
                dataset.SetProjection(projection)
            dataset.GetRasterBand(1).SetNoDataValue(save_nodata_as)
            dataset.GetRasterBand(1).WriteArray(arr)
            # ?dataset.GetRasterBand(1).ComputeStatistics(0)
            dataset = None
            return filename
    return None