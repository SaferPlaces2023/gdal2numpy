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
# Name:        module_MetaData.py
# Purpose:
#
# Author:      Luzzi Valerio, Lorenzo Borelli
#
# Created:
# -------------------------------------------------------------------------------
import os
import numpy as np
from osgeo import gdal, gdalconst
from .filesystem import forceext, israster, isshape, filetojson, jsontofile
from .module_GDAL2Numpy import GDAL2Numpy
from .module_Numpy2GTiff import Numpy2GTiff


def GetRasterShape(filename):
    """
    GetRasterShape
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        m, n = ds.RasterYSize, ds.RasterXSize
        return m, n
    return 0, 0


def GetNoData(filename):
    """
    GetNoData
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        band = ds.GetRasterBand(1)
        no_data = band.GetNoDataValue()
        data, band, ds = None, None, None
        return no_data
    return None


def SetNoData(filename, nodata):
    """
    SetNoData
    """
    dataset = gdal.Open(filename, gdalconst.GA_Update)
    if dataset:
        band = dataset.GetRasterBand(1)
        nodata = band.SetNoDataValue(nodata)
        data, band, dataset = None, None, None
    return None


def GDALFixNoData(filename, format="GTiff", nodata=-9999):
    """
    GDALFixNoData
    """
    if os.path.isfile(filename):
        data, gt, prj = GDAL2Numpy(filename, load_nodata_as=nodata)
        data[abs(data) >= 1e10] = nodata
        Numpy2GTiff(data, gt, prj, filename, format=format, save_nodata_as=nodata)
        return filename
    return False


def GetMinMax(filename):
    """
    GetMinMax
    """
    data, _, _ = GDAL2Numpy(filename)
    return np.nanmin(data), np.nanmax(data)


def GetMetaData(filename):
    """
    GetMetaData - get metadata from filename
    :param filename: the pathname
    :return: returns a dictionary with metadata
    """
    if israster(filename):
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            m, n = ds.RasterYSize, ds.RasterXSize
            band = ds.GetRasterBand(1)
            gt = ds.GetGeoTransform()
            wkt = ds.GetProjection()
            meta = ds.GetMetadata()
            nodata = band.GetNoDataValue()
            minx, px, _, maxy, _, py = gt
            maxx = minx + n * px
            miny = maxy + m * py
            miny, maxy = min(miny, maxy), max(miny, maxy)
            ds = None
            return {
                "m": m,
                "n": n,
                "px": px,
                "py": py,
                "wkt": wkt,
                "nodata": nodata,
                "extent": [minx, miny, maxx, maxy],
                "metadata": meta
            }
    elif isshape(filename):
        filemeta = forceext(filename, "mta")
        return filetojson(filemeta)

    return {}


def GetTag(filename, tagname, band=0):
    """
    GetTag - get a tag in metadata of the file or of the band if specified
    """
    if israster(filename):
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            if not band:
                metadata = ds.GetMetadata()
            elif 0 < band <= ds.RasterCount:
                metadata = ds.GetRasterBand(band).GetMetadata()
            else:
                metadata = {}
            if tagname in metadata:
                ds = None
                return metadata[tagname]
            ds = None
    elif isshape(filename):
        filemeta = forceext(filename, "mta")
        meta = filetojson(filemeta)
        if meta and "metadata" in meta and tagname in meta["metadata"]:
            return meta["metadata"][tagname]

    return None


def SetTag(filename, tagname, tagvalue="", band=0):
    """
    SetTag - set a tag in metadata of the file or of the band if specified
    """
    if israster(filename):
        ds = gdal.Open(filename, gdalconst.GA_Update)
        if ds:
            if tagname:
                if not band:
                    metadata = ds.GetMetadata()
                    metadata[tagname] = f"{tagvalue}"
                    ds.SetMetadata(metadata)
                elif 0 < band <= ds.RasterCount:
                    metadata = ds.GetRasterBand(band).GetMetadata()
                    metadata[tagname] = f"{tagvalue}"
                    ds.GetRasterBand(band).SetMetadata(metadata)
            ds.FlushCache()
            ds = None

    elif isshape(filename):
        filemeta = forceext(filename, "mta")
        meta = filetojson(filemeta)
        meta = meta if meta else {"metadata": {}}
        if "metadata" in meta:
            meta["metadata"][tagname] = tagvalue
            jsontofile(meta, filemeta)
