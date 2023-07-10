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
import json
import os
import tempfile
import hashlib
from .module_log import Logger

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


def juststem(pathname):
    """
    juststem
    """
    pathname = os.path.basename(pathname)
    (root, ext) = os.path.splitext(pathname)
    return root


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


def justext(pathname):
    """
    justext
    """
    pathname = os.path.basename(normpath(pathname))
    (_, ext) = os.path.splitext(pathname)
    return ext.lstrip(".")


def forceext(pathname, newext):
    """
    forceext
    """
    (root, _) = os.path.splitext(normpath(pathname))
    pathname = root + ("." + newext if len(newext.strip()) > 0 else "")
    return normpath(pathname)


def israster(pathname):
    """
    israster
    """
    return pathname and os.path.isfile(pathname) and justext(pathname).lower() in ("tif",)


def isshape(pathname):
    """
    isshape
    """
    return pathname and os.path.isfile(pathname) and justext(pathname).lower() in ("shp",)


def mkdirs(pathname):
    """
    mkdirs - create a folder
    """
    try:
        if os.path.isfile(pathname):
            pathname = justpath(pathname)
        os.makedirs(pathname, exist_ok=True)
    except:
        pass
    return os.path.isdir(pathname)


def tempdir(name=""):
    """
    tempdir
    :return: a temporary directory
    """
    foldername = normpath(tempfile.gettempdir() + "/" + name)
    os.makedirs(foldername, exist_ok=True)
    return foldername


def tempfilename(prefix="", suffix=""):
    """
    return a temporary filename
    """
    return tempfile.gettempdir() + "/" + datetime.datetime.strftime(now(), f"{prefix}%Y%m%d%H%M%S%f{suffix}")


def strtofile(text, filename, append=False):
    """
    strtofile
    """
    try:
        flag = "a" if append else "w"
        if isinstance(text, (str,)):
            text = text.encode("utf-8")
        if isinstance(text, (bytes,)):
            flag += 'b'
        mkdirs(justpath(filename))
        with open(filename, flag) as stream:
            if text:
                stream.write(text)
    except Exception as ex:
        Logger.error(ex)
        return ""
    return filename


def jsontofile(obj, filename):
    """
    jsontofile
    """
    return strtofile(json.dumps(obj), filename)


def filetostr(filename):
    """
    filetostr
    """
    try:
        with open(filename, "r", encoding="utf-8") as stream:
            return stream.read()
    except:
        return None


def filetojson(filename):
    """
    filetojson
    """
    try:
        with open(filename, "r", encoding="utf-8") as stream:
            return json.load(stream)
    except Exception as ex:
        Logger.error(ex)
        return None
    

def md5text(text):
    """
    md5text - Returns the md5 of the text
    """
    if text is not None:
        hashcode = hashlib.md5()
        if isinstance(text, (bytes, bytearray)):
            hashcode.update(text)
        else:
            hashcode.update(text.encode("utf-8"))
        return hashcode.hexdigest()
    return None


def md5sum(filename):
    """
    md5sum - returns themd5 of the file
    """
    if os.path.isfile(filename):
        f = open(filename, mode='rb')
        d = hashlib.md5()
        while True:
            buf = f.read(4096)
            if not buf:
                break
            d.update(buf)
        f.close()
        res=  d.hexdigest()
        return res
    else:
        return ""