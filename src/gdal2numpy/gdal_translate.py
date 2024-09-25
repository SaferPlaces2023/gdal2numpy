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
# Author:      Luzzi Valerio
#
# Created:     25/09/2024
# -------------------------------------------------------------------------------import os
import os
from osgeo import gdal
from .filesystem import tempfilename, listify, now, total_seconds_from, justpath
from .module_Numpy2GTiff import GTiff2Cog
from .module_s3 import move, iss3, get_bucket_name_key, tempname4S3
from .module_log import Logger
from .module_ogr import AutoIdentify


def gdal_translate(filetif, fileout=None, projwin=None, projwin_srs=None, format="GTiff"):
    """
    gdal_translate: gdal_translate a raster file
    """
    t0 = now()
    gdal.SetConfigOption('CPLErrorHandling', 'silent')

    # In case of s3 fileout must be a s3 path
    # fileout = fileout if fileout else tempfilename(suffix=".tif")
    # s3://saferplaces.co/test.tif -> saferplaces.co, test.tif
    if fileout is None:
        filetmp = tempfilename(prefix="gdalwarp_", suffix=".tif")
        fileout = filetmp
    elif iss3(fileout):
        _, filetmp = get_bucket_name_key(fileout)
        filetmp = tempname4S3(filetmp)
    else:
        filetmp = tempfilename(prefix="gdalwarp_", suffix=".tif")

    # assert that the folder exists
    os.makedirs(justpath(filetmp), exist_ok=True)

    projwin = listify(projwin) if projwin else None
    projwin_srs = AutoIdentify(projwin_srs) if projwin_srs else None

    co = [
        "BIGTIFF=YES",
        "TILED=YES",
        "BLOCKXSIZE=512",
        "BLOCKYSIZE=512",
        "COMPRESS=LZW",
        "NUM_THREADS=ALL_CPUS"]

    kwargs = {
        "format": "GTiff",
        "creationOptions": co,
        "projWin": projwin,
        "projWinSRS": projwin_srs,
        "stats": True
    }

    gdal.Translate(filetmp, filetif, **kwargs)

    if format.lower() == "cog":
        # inplace conversion
        t1 = now()
        GTiff2Cog(filetmp)
        Logger.debug(f"GTiff2Cog: converted {filetmp}  in {total_seconds_from(t1)} s.")

    Logger.debug(f"gdalwarp: move {filetmp} to {fileout}")
    move(filetmp, fileout)

    # RestoreGDALEnv()
    gdal.SetConfigOption('CPLErrorHandling', 'once')
    Logger.debug(f"gdalwarp: completed in {total_seconds_from(t0)} s.")
    # ----------------------------------------------------------------------
    return fileout
