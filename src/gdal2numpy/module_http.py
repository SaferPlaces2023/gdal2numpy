import os
import socket
import requests
import ssl
import json
import urllib.request
from urllib.parse import quote

from .module_log import Logger

def hostname():
    """
    hostname
    """
    return socket.gethostname()


def local_ip():
    """
    get_ip -
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        res = s.getsockname()[0]
    except socket.error:
        res = "127.0.0.1"
    finally:
        s.close()
    return res


def whatsmyip():
    """
    whatsmyip
    """
    uris = ["https://checkip.amazonaws.com",
            "https://ifconfig.co/ip", 
            "https://ipinfo.io/ip", 
            "https://icanhazip.com",
            "https://api.ip.sb/ip", 
            "https://api.ipify.org"]
    for uri in uris:
        try:
            return requests.get(uri, timeout=5).text.strip()
        except requests.exceptions.RequestException:
            continue
    return None


def http_exists(url):
    """
    http_exists use requests
    """
    if isinstance(url, str) and url.startswith("http"):
        try:
            r = requests.head(url, timeout=5)
            return r.status_code == 200
        except Exception as ex:
            Logger.warning(ex)
    return False


def http_get(url, headers={}, mode="text"):
    """
    http_get use requests
    """
    if url and isinstance(url, str) and url.startswith("http"):
        try:
            with requests.get(url, headers=headers, timeout=5) as response:
                if response.status_code == 200:
                    if mode == "json":
                        return response.json()
                    elif mode == "text":
                        return response.text
                    return response.content
        except requests.exceptions.RequestException as ex:
            #print(ex)
            Logger.error(ex)
    return None


def http_download(url, filename=None, headers=None):
    """
    http_download use requests
    """
    if url and isinstance(url, str) and url.startswith("http"):
        try:
            with requests.get(url, headers=headers, stream=True, timeout=5) as response:
                if response.status_code == 200:
                    if filename:
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        return filename
                    return response.content
        except requests.exceptions.RequestException as ex:
            #print(ex)
            Logger.error(ex)
    return None


def nominatim_search(query):
    """
    nominatim_search
    """
    if query:
        city = quote(query)
        url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json&limit=1&polygon_text=1"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
        for attempt in range(3):
            try:
                with requests.get(url, headers=headers, timeout=30) as response:
                    if response.status_code == 200:
                        geojson = response.json()
                        return geojson[0] if len(geojson) > 0 else None
                    elif response.status_code in (429, 503, 504):
                        import time
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        Logger.error(f"nominatim_search: HTTP {response.status_code}")
                        break
            except requests.exceptions.Timeout:
                Logger.warning(f"nominatim_search: timeout (attempt {attempt + 1}/3)")
            except requests.exceptions.RequestException as ex:
                Logger.error(ex)
                break
    return None

