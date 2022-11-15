# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2022 Valerio for Gecosistema S.r.l.
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
# Name:        module_Numpy2GTiff.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:
# -------------------------------------------------------------------------------
import os
import numpy as np
from osgeo import gdal
from .filesystem import justpath, mkdirs, tempfilename


def Numpy2GTiff(arr, gt, prj, fileout, format="GTiff", save_nodata_as=-9999, metadata=None):
    """
    Numpy2GTiff - Write a numpy array in  a GTiff file
    :param arr: the numpy array
    :param gt:  the geotransform array (x0, px, r0, y0, r1, py)
    :param prj: the proj4 string
    :param fileout: the output filename
    :param format: the format GTiff/COG/etc...
    :param save_nodata_as: the nodata
    :param metadata:
    :return: returns the pathname
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

            CO = []
            filetif = fileout
            if format == "GTiff":
                CO = ["BIGTIFF=YES", "TILED=YES", "BLOCKXSIZE=512", "BLOCKYSIZE=512", "COMPRESS=LZW"]
            else:
                filetif = tempfilename(suffix=".tif")

            # Create the path to fileout if not exists
            pathname, _ = os.path.split(fileout)
            if pathname:
                os.makedirs(pathname, exist_ok=True)

            # Create the output dataset
            driver = gdal.GetDriverByName("GTiff")
            ds = driver.Create(filetif, cols, rows, 1, fmt, CO)

            if gt is not None:
                ds.SetGeoTransform(gt)
            if prj is not None:
                ds.SetProjection(prj)
            if metadata is not None:
                ds.SetMetadata(metadata)
                # ds.GetRasterBand(1).SetMetadata(metadata) set metadata to the specified band
            ds.GetRasterBand(1).SetNoDataValue(save_nodata_as)
            ds.GetRasterBand(1).WriteArray(arr)

            if format != "GTiff":
                kwargs = {"format": format}
                gdal.Translate(fileout, ds, **kwargs)
                ds = None
                os.unlink(filetif)
                return fileout

            ds.FlushCache()
            ds = None

            return fileout
    return None


def Numpy2AAIGrid(data, gt, prj, filename, save_nodata_as=-9999, format=" %.5g"):
    """
    Numpy2AAIGrid
    """
    ## projection is not used
    (x0, pixelXSize, rot, y0, rot, pixelYSize) = gt
    (rows, cols) = data.shape
    data = np.where(np.isnan(data), save_nodata_as, data)
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


def Numpy2Gdal(data, gt, prj, filename, save_nodata_as=-9999):
    """
    Numpy2Gdal
    """
    ext = os.path.splitext(filename)[1][1:].strip().lower()
    mkdirs(justpath(filename))
    if ext == "tif" or ext == "tiff":
        return Numpy2GTiff(data, gt, prj, filename, save_nodata_as)
    elif ext == "asc":
        return Numpy2AAIGrid(data, gt, prj, filename, save_nodata_as)
    else:
        return ""
