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
# Name:        gdalwarp.py
# Purpose:
#
# Author:      Luzzi Valerio, Lorenzo Borelli
#
# Created:     16/06/2021
# -------------------------------------------------------------------------------
import os
from osgeo import gdal, gdalconst
from .filesystem import juststem, tempfilename
from .module_ogr import SetGDALEnv, RestoreGDALEnv
from .module_open import OpenRaster

def reasampling_method(method):
    """
    reasampling_method translation form text to gdalconst
    """
    method = method.lower()
    if method == "near":
        return gdalconst.GRIORA_NearestNeighbour
    elif method == "bilinear":
        return gdalconst.GRIORA_Bilinear
    elif method == "cubic":
        return gdalconst.GRIORA_Cubic
    elif method == "cubicspline":
        return gdalconst.GRIORA_CubicSpline
    elif method == "lanczos":
        return gdalconst.GRIORA_Lanczos
    elif method == "average":
        return gdalconst.GRIORA_Average
    elif method == "rms":
        return gdalconst.GRIORA_RMS
    elif method == "mode":
        return gdalconst.GRIORA_Mode
    elif method == "gauss":
        return gdalconst.GRIORA_Gauss
    else:
        return gdalconst.GRIORA_Bilinear


def gdalwarp(filelist, fileout=None, dstSRS="", cutline="", cropToCutline=False, pixelsize=(0, 0), resampleAlg="near", format="GTiff"):
    """
    gdalwarp
    """

    gdal.SetConfigOption('CPLErrorHandling', 'silent')

    fileout = fileout if fileout else tempfilename(suffix=".tif")

    if format.lower() == "gtiff":
        co = ["BIGTIFF=YES", "TILED=YES", "BLOCKXSIZE=256", "BLOCKYSIZE=256", "COMPRESS=LZW"]
    elif format.lower() == "cog":
        co = ["BIGTIFF=YES", "COMPRESS=DEFLATE", "NUM_THREADS=ALL_CPUS"]
    else:
        co = []

    kwargs = {
        "format": format,
        "outputType": gdalconst.GDT_Float32,
        "creationOptions": co,
        "dstNodata": -9999,
        "resampleAlg": reasampling_method(resampleAlg),
        "multithread": True
    }

    if pixelsize[0] > 0 and pixelsize[1] != 0:
        kwargs["xRes"] = pixelsize[0]
        kwargs["yRes"] = abs(pixelsize[1])

    if dstSRS:
        kwargs["dstSRS"] = dstSRS

    if os.path.isfile(cutline):
        kwargs["cropToCutline"] = cropToCutline
        kwargs["cutlineDSName"] = cutline
        kwargs["cutlineLayer"] = juststem(cutline)

    SetGDALEnv()
    # inplace gdalwarp
    if fileout == filelist:
        fileout = OpenRaster(fileout, update=True)
    # ----
    gdal.Warp(fileout, filelist, **kwargs)
    RestoreGDALEnv()
    gdal.SetConfigOption('CPLErrorHandling', 'once')
    # ----------------------------------------------------------------------
    return fileout
