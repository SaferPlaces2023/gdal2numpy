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
from .filesystem import *

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

def GDAL2Numpy(filename, band=1, dtype=np.float32, load_nodata_as = np.nan):
    """
    GDAL2Numpy
    """
    t0 = now()
    dtypeOf = {'Float32':np.float32,
                 'Float64':np.float64,
                 'CFloat32':np.float32,
                 'CFloat64':np.float64,
                 'Byte':np.uint8,
                 'Int16':np.int16,
                 'Int32':np.int32,
                 'UInt16':np.uint16,
                 'UInt32':np.uint32,
                 'CInt16':np.int16,
                 'CInt32':np.int32
    }
    dataset = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if dataset:
        band = dataset.GetRasterBand(band)
        cols = dataset.RasterXSize
        rows = dataset.RasterYSize
        geotransform = dataset.GetGeoTransform()
        projection = dataset.GetProjection()
        nodata = band.GetNoDataValue()
        bandtype = dtypeOf[gdal.GetDataTypeName(band.DataType)]
        wdata = band.ReadAsArray(0, 0, cols, rows)

        # translate nodata as Nan
        if not wdata is None:

            if not np.isnan(load_nodata_as):
                print("fixing nodata with:%s"%load_nodata_as)
                wdata[np.isnan(wdata)] = load_nodata_as

            # Output datatype
            if dtype and dtype != bandtype:
                print("fixing % with:%s" % (bandtype,dtype))
                wdata = wdata.astype(dtype, copy=False)

            if bandtype  == np.float32:
                nodata = np.float32(nodata)
                if not nodata is None and np.isinf(nodata):
                    print("fixing inf with:%s" % (load_nodata_as))
                    wdata[np.isinf(wdata)] = load_nodata_as
                elif not nodata is None:
                    print("fixing nodata with:%s" % (load_nodata_as))
                    wdata[wdata == nodata] = load_nodata_as


            elif bandtype == np.float64:
                nodata = np.float64(nodata)
                if not nodata is None and np.isinf(nodata):
                    print("fixing inf with:%s" % (load_nodata_as))
                    wdata[np.isinf(wdata)] = load_nodata_as
                elif not nodata is None:
                    print("fixing nodata with:%s" % (load_nodata_as))
                    wdata[wdata == nodata] = load_nodata_as
            elif bandtype in (np.uint8, np.int16, np.uint16, np.int32, np.uint32):
                if nodata != load_nodata_as:
                    print("fixing nodata with:%s" % (load_nodata_as))
                    wdata[wdata == nodata] = load_nodata_as

        band = None
        dataset = None
        print("Reading <%s> in %ss."%(justfname(filename), total_seconds_from(t0)))
        return (wdata, geotransform, projection)
    print("file %s not exists!" % (filename))
    return (None, None, None)

def Numpy2GTiff(arr, geotransform, projection, filename, save_nodata_as=-9999):
    """
    Numpy2GTiff
    """
    GDT = {
        'uint8': gdal.GDT_Byte,
        'uint16': gdal.GDT_UInt16,
        'uint32': gdal.GDT_UInt32,
        'int16': gdal.GDT_Int16,
        'int32': gdal.GDT_Int32,

        'float32': gdal.GDT_Float32,
        'float64': gdal.GDT_Float64
    }

    if isinstance(arr, np.ndarray):
        rows, cols = arr.shape
        if rows > 0 and cols > 0:
            dtype = str(arr.dtype).lower()
            fmt = GDT[dtype] if dtype in GDT else gdal.GDT_Float64

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

def Numpy2AAIGrid(data, geotransform, projection, filename, save_nodata_as=-9999, format=" %.5g"):
    """
    Numpy2AAIGrid
    """
    ## projection is not used
    (x0, pixelXSize, rot, y0, rot, pixelYSize) = geotransform
    (rows, cols) = data.shape
    data = np.where(np.isnan(data),save_nodata_as,data)
    stream = open(filename, "w")
    stream.write("ncols         %d\r\n" % (cols))
    stream.write("nrows         %d\r\n" % (rows))
    stream.write("xllcorner     %d\r\n" % (x0))
    stream.write("yllcorner     %d\r\n" % (y0 + pixelYSize * rows))
    stream.write("cellsize      %f\r\n" % (pixelXSize))
    stream.write("NODATA_value  %d\r\n" % (save_nodata_as))
    template = (format * cols) + "\r\n"
    for row in data:
        line = template % tuple(row.tolist())
        stream.write(line)
    stream.close()
    return filename

def Numpy2Gdal(data, geotransform, projection, filename, save_nodata_as=-9999):
    """
    Numpy2Gdal
    """
    ext = os.path.splitext(filename)[1][1:].strip().lower()
    mkdirs(justpath(filename))
    if ext == "tif" or ext == "tiff":
        return Numpy2GTiff(data, geotransform, projection, filename, save_nodata_as)
    elif ext == "asc":
        return Numpy2AAIGrid(data, geotransform, projection, filename, save_nodata_as)
    else:
        return ""