# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2021 Luzzi Valerio
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
# Name:        module_features.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     31/12/2022
# -------------------------------------------------------------------------------
import numpy as np
import tempfile
from osgeo import ogr, osr
from .filesystem import isshape, isshape, md5sum
from .module_ogr import SameSpatialRef, GetSpatialRef
from .module_log import Logger
from .module_s3 import iss3, copy

def OpenShape(fileshp, exclusive=False):
    """
    OpenDataset
    """
    if not fileshp:
        ds = None
    elif isinstance(fileshp, str) and isshape(fileshp):
        Logger.info(f"Opening {fileshp}...")
        ds = ogr.Open(fileshp, exclusive)
    elif isinstance(fileshp, str) and iss3(fileshp) and fileshp.endswith(".shp"):
        ds = ogr.Open(copy(fileshp), exclusive)
    elif isinstance(fileshp, ogr.DataSource) and GetAccess(fileshp) >= exclusive:
        Logger.info(f"Dataset already open...")
        ds = fileshp
    elif isinstance(fileshp, ogr.DataSource) and GetAccess(fileshp) < exclusive:
        Logger.info(f"Change the open mode: Open({exclusive})")
        ds = ogr.Open(fileshp.GetName(), exclusive)
    else:
        ds = None
    return ds


def GetAccess(ds):
    """
    GetAccess - return the open mode exclusive or shared
    trying to create/delete a field
    """
    res = -1
    if ds:
        ogr.UseExceptions()
        try:
            layer = ds.GetLayer()
            layer.CreateField(ogr.FieldDefn("__test__", ogr.OFTInteger))
            j = layer.GetLayerDefn().GetFieldIndex("__test__")
            layer.DeleteField(j)
            res = 1
        except Exception as ex:
            Logger.error(ex)
            res = 0
        ogr.DontUseExceptions()
    return res


def GetFeatures(fileshp):
    """
    GetFeatures - get all features from file
    """
    ds = OpenShape(fileshp)
    if ds:
        return list(ds.GetLayer())
    return []


def GetFeatureCount(fileshp):
    """
    GetFeatureCount
    """
    n = -1
    ds = OpenShape(fileshp)
    if ds:
        n = ds.GetLayer(0).GetFeatureCount()
    return n


def GetFeatureByFid(fileshp, layername=0, fid=0):
    """
    GetFeatureByFid
    """
    feature = None
    ds = OpenShape(fileshp)
    if ds:
        layer = ds.GetLayer(layername)
        feature = layer.GetFeature(fid)
    ds = None
    return feature


def GetFieldNames(fileshp, filter=None):
    """
    GetFieldNames
    filter: one of Integer|Integer64|Real|String
    """
    ds = OpenShape(fileshp)
    if ds:
        defn = ds.GetLayer().GetLayerDefn()
        fields = [defn.GetFieldDefn(j) for j in range(defn.GetFieldCount())]
        if filter is not None:
            return [field.GetName() for field in fields if ogr.GetFieldTypeName(field.GetType()) in filter]
        # return all
        return [field.GetName() for field in fields]
    return []


def GetNumericFieldNames(fileshp):
    """
    GetNumericFieldNames
    """
    return GetFieldNames(fileshp, ["Integer", "Integer64", "Real"])


def GetValues(fileshp, fieldname):
    """
    GetValues - Get all values of field
    """
    if fieldname in GetFieldNames(fileshp):
        return [feature.GetField(fieldname) for feature in GetFeatures(fileshp)]
    return []


def GetRange(fileshp, fieldname):
    """
    GetRange - returns the min-max values
    """
    minValue, maxValue = np.Inf, -np.Inf
    if fieldname in GetFieldNames(fileshp, ["Integer", "Integer64", "Real"]):
        for feature in GetFeatures(fileshp):
            value = feature.GetField(fieldname)
            if value is not None:
                minValue = min(value, minValue)
                maxValue = max(value, maxValue)
    return minValue, maxValue


def FieldExists(fileshp, fieldname):
    """
    FieldExists
    """
    idx = -1
    ds = OpenShape(fileshp)
    closeOnExit = type(ds) != type(fileshp)
    if ds:
        layer = ds.GetLayer()
        # idx = -1
        idx = layer.GetLayerDefn().GetFieldIndex(fieldname)
        # layerdefn = layer.GetLayerDefn()
        # n = layerdefn.GetFieldCount()
        # for j in range(n):
        #    fielddefn = layerdefn.GetFieldDefn(j)
        #    if fielddefn.GetName().upper() == f"{fieldname}".upper():
        #        idx = j
        # Logger.info(f"searching field {fieldname}={idx}")
        ds = None if closeOnExit else ds
    return idx


def DeleteField(fileshp, fieldname):
    """
    DeleteField
    """
    res = False
    ds = OpenShape(fileshp, True)
    closeOnExit = type(ds) != type(fileshp)
    j = FieldExists(ds, fieldname)
    if j >= 0:
        Logger.debug(f"Deleting...{fieldname}({j})")
        ds.GetLayer().DeleteField(j)
        res = True
    ds = None if closeOnExit else ds
    return res


def AddField(fileshp, fieldname, dtype=np.float32, width=-1, precision=-1, defaultValue=None, verbose=False):
    """
    AddField
    """
    NUMPY2OGR = {
        np.int8: {"dtype": ogr.OFTInteger, "width": 3, "precision": 0},
        np.int16: {"dtype": ogr.OFTInteger, "width": 5, "precision": 0},
        np.int32: {"dtype": ogr.OFTInteger, "width": 10, "precision": 0},
        np.int64: {"dtype": ogr.OFTInteger64, "width": 20, "precision": 0},
        np.uint8: {"dtype": ogr.OFTInteger, "width": 3, "precision": 0},
        np.uint16: {"dtype": ogr.OFTInteger, "width": 5, "precision": 0},
        np.uint32: {"dtype": ogr.OFTInteger, "width": 10, "precision": 0},
        np.uint64: {"dtype": ogr.OFTInteger64, "width": 20, "precision": 0},
        np.float16: {"dtype": ogr.OFTReal, "width": 10, "precision": 3},
        np.float32: {"dtype": ogr.OFTReal, "width": 19, "precision": 4},
        np.float64: {"dtype": ogr.OFTReal, "width": 24, "precision": 6},
        np.bool_: {"dtype": ogr.OFTInteger, "width": 1, "precision": 0},
        np.str_: {"dtype": ogr.OFTString, "width": 254, "precision": 0},
        np.unicode_: {"dtype": ogr.OFTString, "width": 254, "precision": 0},
        str: {"dtype": ogr.OFTString, "width": 254, "precision": 0},
    }
    res = False
    ds = OpenShape(fileshp, True)
    closeOnExit = type(fileshp) != type(ds)
    if ds:
        layer = ds.GetLayer()
        field = NUMPY2OGR[dtype] if dtype in NUMPY2OGR else {
            "dtype": ogr.OFTString, "width": 254, "precision": 0}
        width = width if width > 0 else field["width"]
        precision = precision if precision >= 0 else field["precision"]
        newfield = ogr.FieldDefn(fieldname, field["dtype"])
        newfield.SetWidth(width)
        newfield.SetPrecision(precision)
        if defaultValue is not None:
            newfield.SetDefault(f"{defaultValue}")

        # Check the field not exists
        j = FieldExists(ds, fieldname)
        fielddef = layer.GetLayerDefn().GetFieldDefn(j) if j >= 0 else None

        # Nessun cambiamento
        if fielddef and fielddef.GetType() == field["dtype"] \
                and fielddef.GetWidth() == width \
                and fielddef.GetPrecision() == precision:
            res = False
        # Stesso tipo o verso strighe
        elif fielddef and fielddef.GetType() == field["dtype"] or field["dtype"] == ogr.OFTString:
            Logger.info(
                f"Altering field definition of {fieldname}({width}:{precision})")
            layer.AlterFieldDefn(
                j, newfield, ogr.ALTER_TYPE_FLAG | ogr.ALTER_WIDTH_PRECISION_FLAG)
            res = True
        else:
            Logger.info(
                f"Creating a new field {fieldname}({width}:{precision})")
            layer.CreateField(newfield)
            res = True

        # setting the default value
        if res and defaultValue is not None:
            # layer.StartTransaction()
            for feature in layer:
                feature.SetField(fieldname, defaultValue)
                layer.SetFeature(feature)
            # layer.CommitTransaction()
        # ----

    ds = None if closeOnExit else ds
    return res


def Transform(fileshp, t_srs, fileout=None):
    """
    Transform - reproject the shapefile
    t_srs: target spatial reference Can be also a template filepath
    """
    if SameSpatialRef(fileshp, t_srs):
        Logger.debug("Nothing to do. The srs is the same.")
        return fileshp

    t_srs = GetSpatialRef(t_srs)
    t_code = f"{t_srs.GetAuthorityName(None)}_{t_srs.GetAuthorityCode(None)}"
    fileout = fileout if fileout else f"{tempfile.gettempdir()}/{md5sum(fileshp)}_{t_code}.shp"

    if isshape(fileout):
        Logger.debug(f"Using cached file:<{fileout}>...")
        return fileout

    ds = OpenShape(fileshp)
    if ds:
        layer = ds.GetLayer()

        # set spatial reference and transformation
        defn = layer.GetLayerDefn()
        s_srs = layer.GetSpatialRef()
        transform = osr.CoordinateTransformation(s_srs, t_srs)

        driver = ogr.GetDriverByName("Esri Shapefile")
        dw = driver.CreateDataSource(fileout)
        outlayer = dw.CreateLayer('', t_srs, defn.GetGeomType())

        # Copy each field
        for j in range(defn.GetFieldCount()):
            fielddefn = defn.GetFieldDefn(j)
            outlayer.CreateField(fielddefn)

        # Copy and transform each feature
        for feature in layer:
            transformed = feature.GetGeometryRef()
            transformed.Transform(transform)

            geom = ogr.CreateGeometryFromWkb(transformed.ExportToWkb())
            defn = outlayer.GetLayerDefn()
            new_feature = ogr.Feature(defn)
            for j in range(defn.GetFieldCount()):
                new_feature.SetField(j, feature.GetField(j))
            new_feature.SetGeometry(geom)
            outlayer.CreateFeature(new_feature)
            new_feature = None

        ds, dw = None, None
        return fileout
    return False
