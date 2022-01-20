import requests
import csv
from bs4 import BeautifulSoup

from component import parameter as cp

"""
Freely adapted from the code from:
https://github.com/samapriya/gee_asset_manager_addon/blob/master/geeadd/app2script.py
"""


def jsext(asset):
    """read the content of the asset and export it as str"""

    # transform the asset link into a url
    url_asset = asset

    source = requests.get(url_asset)
    html_content = source.text

    soup = BeautifulSoup(html_content, "html.parser")

    output = ""
    for articles in soup.find_all("script"):
        if not articles.string == None and articles.string.strip().startswith("init"):
            url = articles.string.strip().split('"')[1]

            # stop if it's not a url
            if not url.startswith("https"):
                continue

            iscript = requests.get(url).json()
            pt = iscript["path"]

            output += "\n"
            output += (
                iscript["dependencies"][pt].encode("utf-8").decode("utf-8").strip()
            )

    return output


def save(code, path):
    """save the code in the appropriate file"""

    file = cp.result_dir / f"{path}.js"

    if file.is_file():
        raise ValueError("The file already exist")

    with file.open("w") as f:

        f.write(code)

    return file
