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
# Name:        module_esri_shape.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     31/12/2022
# -------------------------------------------------------------------------------
import os
import re
import json
import pkgutil
from osgeo import ogr, osr
from .filesystem import justpath, listify, tempfilename, filetostr, forceext, md5text
from .module_open import OpenShape, OpenRaster
from .module_s3 import iss3, move, tempname4S3, isfile
from .module_log import Logger
from Levenshtein import distance


def AutoIdentify(wkt):
    """
    AutoIdentify
    """
    # get the file pe_hash_list.json from package data

    if isfile(wkt) and wkt.endswith(".tif"):
        wkt = OpenRaster(wkt).GetProjection()
    elif isfile(wkt) and isfile(forceext(wkt, "prj")):
        wkt = filetostr(forceext(wkt, "prj"))
    elif isinstance(wkt, osr.SpatialReference):
        wkt = wkt.ExportToWkt()
    elif isinstance(wkt, ogr.DataSource):
        layer = wkt.GetLayer()
        wkt = layer.GetSpatialRef().ExportToWkt()
    elif isinstance(wkt, ogr.Layer):
        wkt = wkt.GetSpatialRef().ExportToWkt()
    elif isinstance(wkt, ogr.Feature):
        wkt = wkt.GetGeometryRef().GetSpatialReference().ExportToWkt()
    elif isinstance(wkt, ogr.Geometry):
        wkt = wkt.GetSpatialReference().ExportToWkt()
    elif isinstance(wkt, str) and re.match(r'^.*?\:\d{4,5}$', wkt):
        return wkt
    elif isinstance(wkt, str) and wkt.startswith("GEOGCS") or wkt.startswith("PROJCS"):
        pass
    else:
        Logger.warning("The wkt is not a valid string or object")
        return None

    pe_hash_list = json.loads(pkgutil.get_data(
        __name__, "data/pe_hash_list.json").decode("utf-8"))
    pe_hash_list = pe_hash_list["CoordinateSystems"] if "CoordinateSystems" in pe_hash_list else {
    }
    code = pe_hash_list.get(md5text(wkt), None)

    # last chance to identify the wkt
    if not code:
        Logger.debug("2) Second chance to identify the wkt")
        spatial_res_sys_all = json.loads(pkgutil.get_data(
            __name__, "data/spatial_ref_sys_all.json").decode("utf-8"))
        spatial_res_sys_all = spatial_res_sys_all["CoordinateSystems"] if "CoordinateSystems" in spatial_res_sys_all else {
        }
        for authid, srs in spatial_res_sys_all.items():
            if srs["wkt"] == wkt or srs["proj4"] == wkt:
                code = authid
                break

    if not code:
        Logger.debug("2) Third chance to identify the wkt by the name")
        candidates = []
        for authid, srs in spatial_res_sys_all.items():
            if srs["name"] == osr.SpatialReference(wkt).GetName():
                candidates.append((authid, distance(srs["wkt"], wkt)))

        #  sort by distance
        candidates = sorted(candidates, key=lambda x: x[1])
        code = candidates[0][0] if len(candidates) > 1 else None

    return code


def CopySchema(fileshp, fileout=None):
    """
    CopySchema
    """
    dsr = OpenShape(fileshp, 0)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    fileout = fileout if fileout else tempfilename(suffix=".shp")
    filetmp = tempname4S3(fileout) if iss3(fileout) else fileout
    os.makedirs(justpath(filetmp), exist_ok=True)
    dsw = driver.CreateDataSource(filetmp)
    if dsr:
        layer1 = dsr.GetLayer()
        layer2 = dsw.CreateLayer(
            layer1.GetName(), layer1.GetSpatialRef(), layer1.GetGeomType())
        # Copying the old layer schema into the new layer
        defn = layer1.GetLayerDefn()
        for j in range(defn.GetFieldCount()):
            layer2.CreateField(defn.GetFieldDefn(j))
    dsr, dsw = None, None
    if iss3(fileout):
        move(filetmp, fileout)
    else:
        fileout = filetmp
    return fileout


def FeatureSelection(fileshp, fileout, fids=None):
    """
    FeatureSelection - Create a new shapefile filtering features
    """
    fileout = CopySchema(fileshp)
    dsr = OpenShape(fileshp, 0)
    dsw = ogr.Open(fileout, 1)
    if dsr and dsw:
        layer1 = dsr.GetLayer()
        layer2 = dsw.GetLayer()
        if fids:
            for fid in listify(fids):
                feature = layer1.GetFeature(int(fid))
                if feature:
                    layer2.CreateFeature(feature)
        else:
            for feature in layer1:
                layer2.CreateFeature(feature)
    dsr, dwr = None, None

    return fileout
