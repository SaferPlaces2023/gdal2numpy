# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------
import math

import numpy as np
from osgeo import gdal, gdalconst
from osgeo import ogr, osr

from .filesystem import *


def Rectangle(minx, miny, maxx, maxy):
    """
    Rectangle
    """
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minx, miny)
    ring.AddPoint_2D(maxx, miny)
    ring.AddPoint_2D(maxx, maxy)
    ring.AddPoint_2D(minx, maxy)
    ring.AddPoint_2D(minx, miny)
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


def Extent(bbox, s_srs=False, t_srs=False):
    """
    Extent
    """

    if s_srs and t_srs:
        s_srs = GetSpatialRef(s_srs)
        t_srs = GetSpatialRef(t_srs)
        transform = osr.CoordinateTransformation(s_srs, t_srs)

        print("EPSGTreatsAsLatLong:", s_srs.EPSGTreatsAsLatLong())

        p1 = ogr.Geometry(ogr.wkbPoint)
        p2 = ogr.Geometry(ogr.wkbPoint)
        if s_srs.IsGeographic() or s_srs.EPSGTreatsAsLatLong():
            p1.AddPoint(bbox[1], bbox[0])
            p2.AddPoint(bbox[3], bbox[2])
        else:
            p1.AddPoint(bbox[0], bbox[1])
            p2.AddPoint(bbox[2], bbox[3])

        p1.Transform(transform)
        p2.Transform(transform)

        if t_srs.IsGeographic() or t_srs.EPSGTreatsAsLatLong():
            return p1.GetY(), p1.GetX(), p2.GetY(), p2.GetX()
        else:
            return p1.GetX(), p1.GetY(), p2.GetX(), p2.GetY()

    return tuple(bbox)


def GetPixelSize(filename):
    """
    GetPixelSize
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        gt = ds.GetGeoTransform()
        _, px, _, _, _, py = gt
        ds = None
        return px, py
    return 0, 0


def GetRasterShape(filename):
    """
    GetRasterShape
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        band = ds.GetRasterBand(1)
        m, n = ds.RasterYSize, ds.RasterXSize
        return m, n
    return 0, 0


def GetExtent(filename):
    """
    GetExtent
    """
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        "{xmin} {ymin} {xmax} {ymax}"
        m, n = ds.RasterYSize, ds.RasterXSize
        gt = ds.GetGeoTransform()
        xmin, px, _, ymax, _, py = gt
        xmax = xmin + n * px
        ymin = ymax + m * py
        ymin, ymax = min(ymin, ymax), max(ymin, ymax)
        ds = None
        return xmin, ymin, xmax, ymax
    return 0, 0, 0, 0


def GetSpatialRef(filename):
    """
    GetSpatialRef
    """
    if isinstance(filename, osr.SpatialReference):
        srs = filename

    elif isinstance(filename, int):
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(filename)

    elif isinstance(filename, str) and filename.lower().startswith("epsg:"):
        code = int(filename.split(":")[1])
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(code)

    elif isinstance(filename, str) and os.path.isfile(filename) and filename.lower().endswith(".shp"):
        ds = ogr.OpenShared(filename)
        if ds:
            srs = ds.GetLayer().GetSpatialRef()
        ds = None

    elif isinstance(filename, str) and os.path.isfile(filename) and filename.lower().endswith(".tif"):
        ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
        if ds:
            wkt = ds.GetProjection()
            srs = osr.SpatialReference()
            srs.ImportFromWkt(wkt)
        ds = None
    else:
        srs = osr.SpatialReference()
    return srs


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


def GDAL2Numpy(filename, band=1, dtype=np.float32, load_nodata_as=np.nan, bbox=[], verbose=False):
    """
    GDAL2Numpy
    """
    t0 = now()
    data_type_of = {
        'Float32': np.float32,
        'Float64': np.float64,
        'CFloat32': np.float32,
        'CFloat64': np.float64,
        'Byte': np.uint8,
        'Int16': np.int16,
        'Int32': np.int32,
        'UInt16': np.uint16,
        'UInt32': np.uint32,
        'CInt16': np.int16,
        'CInt32': np.int32
    }
    filename = "/vsicurl/" + filename if filename and filename.lower().startswith("http") else filename
    ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
    if ds:
        band = ds.GetRasterBand(band)
        m, n = ds.RasterYSize, ds.RasterXSize
        gt, prj = ds.GetGeoTransform(), ds.GetProjection()
        no_data = band.GetNoDataValue()
        band_type = data_type_of[gdal.GetDataTypeName(band.DataType)]

        if not bbox:
            data = band.ReadAsArray(0, 0, n, m)
        else:
            x0, px, r0, y0, r1, py = gt
            X0, Y0, X1, Y1 = bbox

            # calcutate starting indices
            j0, i0 = int((X0 - x0) / px), int((Y1 - y0) / py)
            cols, rows = math.ceil((X1 - X0) / px), math.ceil(abs(Y1 - Y0) / abs(py))

            # index-safe
            j0, i0 = min(max(j0, 0), n - 1), min(max(i0, 0), m - 1)
            cols = min(max(cols, 0), n)
            rows = min(max(rows, 0), m)

            # re-arrange gt
            k = math.floor((X0 - x0) / px)
            h = math.floor((Y1 - y0) / py)
            gt = x0 + k * px, px, r0, y0 + h * py, r1, py

            data = band.ReadAsArray(j0, i0, cols, rows)

        # translate no-data as Nan
        if data is not None:

            if not np.isnan(load_nodata_as):
                data[np.isnan(data)] = load_nodata_as

            # Output datatype
            if dtype and dtype != band_type:
                data = data.astype(dtype, copy=False)

            if band_type == np.float32:
                no_data = np.float32(no_data)
                if no_data is not None and np.isinf(no_data):
                    data[np.isinf(data)] = load_nodata_as
                elif no_data is not None:
                    data[data == no_data] = load_nodata_as

            elif band_type == np.float64:
                no_data = np.float64(no_data)
                if no_data is not None and np.isinf(no_data):
                    data[np.isinf(data)] = load_nodata_as
                elif no_data is not None:
                    data[data == no_data] = load_nodata_as

            elif band_type in (np.uint8, np.int16, np.uint16, np.int32, np.uint32):
                if no_data != load_nodata_as:
                    data[data == no_data] = load_nodata_as

        band = None
        ds = None
        if verbose:
            print("Reading <%s> in %ss." % (justfname(filename), total_seconds_from(t0)))
        return data, gt, prj
    print("file %s not exists!" % filename)
    return None, None, None


def Numpy2GTiff(arr, geotransform, projection, filename, format="GTiff", save_nodata_as=-9999):
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

            if format == "GTiff":
                CO = ["BIGTIFF=YES", "COMPRESS=LZW"]
            else:
                CO = []

            pathname, _ = os.path.split(filename)
            if pathname:
                os.makedirs(pathname, exist_ok=True)
            driver = gdal.GetDriverByName("GTiff")
            #driver = gdal.GetDriverByName(format)
            dataset = driver.Create(filename, cols, rows, 1, fmt, CO)
            if (geotransform != None):
                dataset.SetGeoTransform(geotransform)
            if (projection != None):
                dataset.SetProjection(projection)
            dataset.GetRasterBand(1).SetNoDataValue(save_nodata_as)
            dataset.GetRasterBand(1).WriteArray(arr)
            # ?dataset.GetRasterBand(1).ComputeStatistics(0)
            dataset = None

            if format=="COG":
                ds = gdal.Open(filename, gdalconst.GA_ReadOnly)
                kwargs = {"format": format}
                gdal.Translate(filename, ds, **kwargs)
            return filename
    return None


def Numpy2AAIGrid(data, geotransform, projection, filename, save_nodata_as=-9999, format=" %.5g"):
    """
    Numpy2AAIGrid
    """
    ## projection is not used
    (x0, pixelXSize, rot, y0, rot, pixelYSize) = geotransform
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
