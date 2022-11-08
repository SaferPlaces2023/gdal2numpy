# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2019 Luzzi Valerio 
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
# Name:        filesystem.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     16/12/2019
# -------------------------------------------------------------------------------

import datetime
import os
import tempfile


def now():
    """
    now
    :return: returns the time in ms
    """
    return datetime.datetime.now()


def total_seconds_from(t):
    """
    total_seconds_from
    :param t: the time in ms
    :return: return the timedelta in ms from now es now()-t
    """
    return (datetime.datetime.now() - t).total_seconds()


def normpath(pathname):
    """
    normpath
    """
    if not pathname:
        return ""
    return os.path.normpath(pathname.replace("\\", "/")).replace("\\", "/")


def justpath(pathname, n=1):
    """
    justpath
    """
    for j in range(n):
        (pathname, _) = os.path.split(normpath(pathname))
    if pathname == "":
        return "."
    return normpath(pathname)


def justfname(pathname):
    """
    justfname - returns the basename
    """
    return normpath(os.path.basename(normpath(pathname)))


def forceext(pathname, newext):
    """
    forceext
    """
    (root, _) = os.path.splitext(normpath(pathname))
    pathname = root + ("." + newext if len(newext.strip()) > 0 else "")
    return normpath(pathname)


def mkdirs(pathname):
    """
    mkdirs - create a folder
    """
    try:
        if os.path.isfile(pathname):
            pathname = justpath(pathname)
        os.makedirs(pathname)
    except:
        pass
    return os.path.isdir(pathname)


def tempfilename(prefix="", suffix=""):
    """
    return a temporary filename
    """
    return tempfile.gettempdir() + "/" + datetime.datetime.strftime(now(), f"{prefix}%Y%m%d%H%M%S%f{suffix}")
