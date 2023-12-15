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
from .filesystem import juststem, tempfilename, listify
from .module_Numpy2GTiff import GTiff2Cog
from .module_ogr import SetGDALEnv, RestoreGDALEnv, GetEPSG
from .module_open import OpenRaster
from .module_s3 import *


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

    # In case of s3 fileout must be a s3 path
    # fileout = fileout if fileout else tempfilename(suffix=".tif")
    # s3://saferplaces.co/test.tif -> saferplaces.co, test.tif
    if iss3(fileout):
        _, filetmp = get_bucket_name_key(fileout)
        filetmp = tempname4S3(filetmp)
    else:
        filetmp = tempfilename(prefix="gdalwarp_", suffix=".tif")

    # assert that the folder exists
    os.makedirs(justpath(filetmp), exist_ok=True)

    #  copy s3 file to local
    filelist_tmp = []
    filelist = listify(filelist)
    for filename in filelist:
        if iss3(filename):
            filename = copy(filename, tempfilename(
                prefix="s3_", suffix=".tif"))
        filelist_tmp.append(filename)
    # ----------------------------------------------------------------------

    co = ["BIGTIFF=YES",
          "TILED=YES",
          "BLOCKXSIZE=256",
          "BLOCKYSIZE=256",
          "COMPRESS=LZW"]

    kwargs = {
        "format": "GTiff",
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
        dstSRS = GetEPSG(dstSRS)
        kwargs["dstSRS"] = dstSRS

    if isfile(cutline):
        kwargs["cropToCutline"] = cropToCutline
        kwargs["cutlineDSName"] = cutline
        kwargs["cutlineLayer"] = juststem(cutline)

    # SetGDALEnv()
    # inplace gdalwarp
    if fileout is None and len(filelist) > 0:
        fileout = filelist[0]
        # ds = OpenRaster(filetmp, update=True)
        # filetmp = ds

    gdal.Warp(filetmp, filelist_tmp, **kwargs)

    Logger.debug(f"gdalwarp: converting to {filetmp}")

    if format.lower() == "cog":
        # inplace conversion
        GTiff2Cog(filetmp)

    Logger.debug(f"gdalwarp: move {filetmp} to {fileout}")
    move(filetmp, fileout)

    #RestoreGDALEnv()
    gdal.SetConfigOption('CPLErrorHandling', 'once')
    # ----------------------------------------------------------------------
    return fileout
