# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2023 Luzzi Valerio
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
# Name:        module_flow.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     06/07/2023
# -------------------------------------------------------------------------------
import os
import json

from osgeo import ogr
from .module_ogr import GetSpatialRef


def infer_geometry_type(features):
    """
    infer_geometry_type
    """
    if features:
        first = features[0]
        geom = ogr.CreateGeometryFromJson(json.dumps(first["geometry"]))
        geom_type = geom.GetGeometryType()
        geom.Destroy()
        return geom_type
    return ogr.wkbUnknown


def infer_width(features, fieldname, default_width=6):
    """
    infer_width
    """
    width = default_width
    int_part = 0
    precision = 0
    coma = 0
    for feature in features:
        fieldvalue = feature["properties"][fieldname]
        if isinstance(fieldvalue, float) and "." in f"{fieldvalue}":
            coma = 1
            precision = max( len(f"{fieldvalue}".split(".")[-1]), precision)
        int_part = max( len(f"{fieldvalue}".split(".")[0]), int_part)

    width = int_part+coma+precision
    return width, precision


def infer_layerDefn(features):
    """
    infer_layerDefn
    """
    fields = []
    if features:
        first = features[0]
        for fieldname in first["properties"]:
            fieldvalue = first["properties"][fieldname]
            width, precision = infer_width(features, fieldname)

            # infer field type from value
            if isinstance(fieldvalue, int):
                fieldtype = ogr.OFTInteger
            elif isinstance(fieldvalue, float):
                fieldtype = ogr.OFTReal
            else:
                fieldtype = ogr.OFTString

            newfield = ogr.FieldDefn(fieldname, fieldtype)
            newfield.SetWidth(width)
            newfield.SetPrecision(precision)
            fields.append(newfield)
    return fields


def ShapeFileFromGeoJSON(features, fileshp="", t_srs=4326):
    """
    ShapeFileFromGeoJSON
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    fileshp = fileshp or os.path.join(os.path.dirname(__file__), "temp.shp")

    # detect geometry type from first feature
    if features:
        first = features[0]
        geom = ogr.CreateGeometryFromJson(json.dumps(first["geometry"]))
        geom_type = geom.GetGeometryType()
        geom.Destroy()
        
        # create spatial reference
        t_srs = GetSpatialRef(t_srs)

        # create shapefile
        # - if exists, delete
        if os.path.exists(fileshp):
            driver.DeleteDataSource(fileshp)

        # - create new shapefile
        ds = driver.CreateDataSource(fileshp)
        layer = ds.CreateLayer(fileshp, geom_type=geom_type, srs=t_srs)
        
        # create fields from first feature
        fields = infer_layerDefn(features)
        for field in fields:
            layer.CreateField(field)

        featureDefn = layer.GetLayerDefn()
        for feature in features:
            # Create the feature and set value
            geom = feature["geometry"]
            geom = ogr.CreateGeometryFromJson(json.dumps(geom))
            ogr_feature = ogr.Feature(featureDefn)
            ogr_feature.SetGeometry(geom)
            for field in fields:
                fieldname = field.GetName()
                ogr_feature.SetField(fieldname, feature["properties"][fieldname])

            layer.CreateFeature(ogr_feature)
            ogr_feature = None

        ds.Destroy()
