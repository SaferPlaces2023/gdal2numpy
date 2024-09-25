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
# Name:        rasterlike.py
# Purpose:
#
# Author:      Luzzi Valerio, Lorenzo Borelli
#
# Created:     16/06/2021
# -------------------------------------------------------------------------------
import os
import numpy as np
from .filesystem import tempfilename
from .module_ogr import SamePixelSize, SameSpatialRef, GetSpatialRef, GetExtent, SameExtent
from .module_ogr import ogr_remove, Rectangle, CreateRectangleShape, GetPixelSize
from .module_GDAL2Numpy import GDAL2Numpy
from .module_Numpy2GTiff import Numpy2GTiff
from .gdalwarp import gdalwarp
from .module_log import Logger
from .module_s3 import copy


def RasterLike(filetif, filetpl, fileout=None, resampleAlg="near", format="GTiff", verbose=False):
    """
    RasterLike: adatta un raster al raster template ( dem ) ricampionando, 
    riproiettando estendendo/clippando il file raster se necessario.
    """
    Logger.debug("0)RasterLike...")
    fileout = fileout if fileout else tempfilename(suffix=".tif")

    if SameSpatialRef(filetif, filetpl) and \
        SamePixelSize(filetif, filetpl, decimals=2) and \
            SameExtent(filetif, filetpl, decimals=3):
        Logger.debug("Files have the same srs, pixels size and extent!")
        fileout = filetif
        return fileout

    srs_tpl = GetSpatialRef(filetpl)
    # Tiff extent
    tif_minx, tif_miny, tif_maxx, tif_maxy = GetExtent(filetif, srs_tpl)
    # Template extent
    tpl_minx, tpl_miny, tpl_maxx, tpl_maxy = GetExtent(filetpl)
    # Template extent 10% larger
    delta = 0.1
    crp_minx, crp_miny, crp_maxx, crp_maxy = tpl_minx - delta * (tpl_maxx - tpl_minx), tpl_miny - delta * (
        tpl_maxy - tpl_miny), tpl_maxx + delta * (tpl_maxx - tpl_minx), tpl_maxy + delta * (tpl_maxy - tpl_miny)

    tif_rectangle = Rectangle(tif_minx, tif_miny, tif_maxx, tif_maxy)
    tpl_rectangle = Rectangle(tpl_minx, tpl_miny, tpl_maxx, tpl_maxy)
    # first coarse crop to speed up the process
    if tif_rectangle.Intersects(tpl_rectangle) and \
        tif_rectangle.GetArea()/tpl_rectangle.GetArea() > 4:
            file_rect = tempfilename(suffix=".shp")
            cropshape = CreateRectangleShape(crp_minx, crp_miny, crp_maxx, crp_maxy,
                                            srs=srs_tpl,
                                            fileshp=file_rect)
            file_warp0 = gdalwarp([filetif], cutline=cropshape,
                                cropToCutline=False, dstSRS=srs_tpl)
            ogr_remove(cropshape)
            Logger.debug(f"0e)gdalwarp...done {file_warp0}")
    else:
        file_warp0 = copy(filetif)

    Logger.debug("1)gdalwarp...")
    # Second warp to the template SRS and pixel size
    file_warp1 = tempfilename(suffix=".warp1.tif")
    file_warp1 = gdalwarp([file_warp0], fileout=file_warp1, dstSRS=srs_tpl,
                          pixelsize=GetPixelSize(filetpl, um=None),
                          resampleAlg=resampleAlg)
    Logger.debug(f"1a)gdalwarp...done {file_warp1}")
    tif_minx, tif_miny, tif_maxx, tif_maxy = GetExtent(file_warp1)
    tpl_minx, tpl_miny, tpl_maxx, tpl_maxy = GetExtent(filetpl)
    # create tif and template rectangles
    # to detect intersections
    tif_rectangle = Rectangle(tif_minx, tif_miny, tif_maxx, tif_maxy)
    tpl_rectangle = Rectangle(tpl_minx, tpl_miny, tpl_maxx, tpl_maxy)

    Logger.debug("1b)rectangle done")
    # Final Refinement of the crop
    if tif_rectangle.Intersects(tpl_rectangle):
        file_rect = tempfilename(suffix=".shp")
        demshape = CreateRectangleShape(tpl_minx, tpl_miny, tpl_maxx, tpl_maxy,
                                        srs=srs_tpl,
                                        fileshp=file_rect)
        Logger.debug("2b)gdalwarp...")
        gdalwarp([file_warp1], fileout, cutline=demshape, cropToCutline=True,
                 dstSRS=srs_tpl, pixelsize=GetPixelSize(filetpl, um=None), resampleAlg=resampleAlg, format=format)
        Logger.debug(f"2c)gdalwarp...done {fileout}")
        ogr_remove(file_rect)

    else:
        wdata, gt, prj = GDAL2Numpy(
            filetpl, band=1, dtype=np.float32, load_nodata_as=np.nan)
        wdata.fill(np.nan)
        Numpy2GTiff(wdata, gt, prj, fileout, format=format)

    os.unlink(file_warp0)
    os.unlink(file_warp1)
    return fileout if os.path.exists(fileout) else None
