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
from osgeo import ogr
from .filesystem import isshape


def OpenShape(fileshp):
    """
    OpenShape
    """
    return ogr.OpenShared(fileshp) if isshape(fileshp) else None


def GetFeatures(fileshp):
    """
    GetFeatures - get all features from file
    """
    ds = OpenShape(fileshp)
    if ds:
        return [feature for feature in ds.GetLayer()]
    return []


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
        if filter:
            return [field.GetName() for field in fields if ogr.GetFieldTypeName(field.GetType()) in filter]
        # return all
        return [field.GetName() for field in fields]
    return []


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
    for feature in GetFeatures(fileshp):
        value = feature.GetField(fieldname)
        if value is not None:
            minValue = min(value, minValue)
            maxValue = max(value, maxValue)
    return minValue, maxValue



