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
from .module_ogr import SamePixelSize, SameSpatialRef, GetSpatialRef, GetExtent, SameExtent, GetPixelSize, ogr_remove, \
    Rectangle, CreateRectangleShape
from gdal2numpy import GDAL2Numpy, Numpy2GTiff
from .gdalwarp import gdalwarp


def RasterLike(filetif, filetpl, fileout=None, resampleAlg="near", format="GTiff", verbose=False):
    """
    RasterLike: adatta un raster al raster template ( dem ) ricampionando, riproiettando estendendo/clippando il file raster se necessario.
    """
    if SameSpatialRef(filetif, filetpl) and SamePixelSize(filetif, filetpl, decimals=2) and SameExtent(filetif, filetpl,
                                                                                                       decimals=3):
        fileout = filetif
        return fileout

    # printv("1)gdalwarp...", verbose)
    file_warp1 = tempfilename(suffix=".warp1.tif")
    file_warp1 = gdalwarp([filetif], fileout=file_warp1, dstSRS=GetSpatialRef(filetpl), pixelsize=GetPixelSize(filetpl),
                          resampleAlg=resampleAlg, format=format)

    tif_minx, tif_miny, tif_maxx, tif_maxy = GetExtent(file_warp1)
    tpl_minx, tpl_miny, tpl_maxx, tpl_maxy = GetExtent(filetpl)
    # create tif and template rectangles
    # to detect intersections
    tif_rectangle = Rectangle(tif_minx, tif_miny, tif_maxx, tif_maxy)
    tpl_rectangle = Rectangle(tpl_minx, tpl_miny, tpl_maxx, tpl_maxy)

    # printv('rectangle done', verbose)
    if tif_rectangle.Intersects(tpl_rectangle):
        # printv('intersection', verbose)
        file_rect = tempfilename(suffix=".shp")
        spatialRefSys = GetSpatialRef(filetpl)
        demshape = CreateRectangleShape(tpl_minx, tpl_miny, tpl_maxx, tpl_maxy,
                                        srs=spatialRefSys,
                                        fileshp=file_rect)
        # printv("2)gdalwarp...", verbose)
        gdalwarp([file_warp1], fileout, cutline=demshape, cropToCutline=True,
                 dstSRS=GetSpatialRef(filetpl), pixelsize=GetPixelSize(filetpl), resampleAlg=resampleAlg, format=format)

        ogr_remove(file_rect)

    else:
        wdata, gt, prj = GDAL2Numpy(filetpl, band=1, dtype=np.float32, load_nodata_as=np.nan,
                                    verbose=False)
        wdata.fill(np.nan)
        Numpy2GTiff(wdata, gt, prj, fileout, format=format)

    os.unlink(file_warp1)

    return fileout if os.path.exists(fileout) else None
