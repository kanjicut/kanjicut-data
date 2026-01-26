# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import requests
import zipfile
import io
import os
import json

from utils import is_valid_kanji

KANJIVG_LATEST_RELEASE = "https://api.github.com/repos/KanjiVG/kanjivg/releases/latest"
KANJIVG_HEX_PADDING = 5
KANJIVG_HEX_PADDING_CHAR = "0"

def get_kvg_index() -> dict[str, list[str]] | None:
    """
    Requests the KanjiVG index from the KanjiVG repository.

    :return: Dictionary of kanji and their file names or none
    :rtype: dict[str, list[str]] | None
    """

    response = requests.get("https://raw.githubusercontent.com/KanjiVG/kanjivg/refs/heads/master/kvg-index.json")

    if response.status_code != 200:
        print(f"Attempting to retrieve KanjiVG index results in {response.status_code}. Aborting process.")
        return
    
    return response.json()

def get_latest_kvg_release() -> zipfile.ZipFile | None:
    """
    Requests the latest GitHub release of KanjiVG.

    :return: KanjiVG Zip file
    :rtype: zipfile.Zipfile | None
    """

    response = requests.get(KANJIVG_LATEST_RELEASE, headers={
        "Accept": "application/vnd.github.v3+json"
    })

    if response.status_code != 200:
        print(f"Attempting to request the latest release resulted in a status code of {response.status_code}. Aborting process.")
        return
    
    # Index the first release (kanjivg-all) and get its download URL
    latest_json = response.json()

    download_url = latest_json["assets"][0]["browser_download_url"]
    
    # Download the ZIP file
    response = requests.get(download_url)

    if response.status_code != 200:
        print(f"Attempting to download the latest release zip file resulted in a status code of {response.status_code}. Aborting process.")
        return

    return zipfile.ZipFile(io.BytesIO(response.content))

def unicode_to_hex(kanji_char: str):
    """
    Converts a unicode kanji to a hexadecimal string as specified by KanjiVG.    

    The ``kanji_char`` parameter should be a single character or ``unicode_to_hex()`` will return ``None``.

    :param kanji_char: The kanji character
    :type kanji: str
    :return: Base 16 hexadecimal string left padded to five characters with zeros
    :rtype: str
    """

    if not is_valid_kanji(kanji_char):
        return
    
    code_point = ord(kanji_char)
    raw_hex = format(code_point, "x")
    padded_hex = raw_hex.rjust(KANJIVG_HEX_PADDING, KANJIVG_HEX_PADDING_CHAR)

    return padded_hex.lower()

def hex_to_unicode(kanji_hex: str):
    """
    Converts a hexadecimal string to a unicode kanji character.    

    The ``kanji_hex`` parameter must be a valid kanji otherwise ``unicode_to_hex()`` will return ``None``.

    :param kanji_hex: The base 16 hexadecimal string left padded to five characters with zeros
    :type kanji_hex: str
    :return: Unicode string
    :rtype: str
    """

    code_point = int(kanji_hex, 16)
    kanji_char = chr(code_point)

    if not is_valid_kanji(kanji_char):
        return

    return kanji_char
                  
def main():
    kvg_zip = get_latest_kvg_release()

    if not kvg_zip:
        return

    with kvg_zip as zip:
        for file_path in zip.namelist():
            # 5 digit hex
            if len(file_path) != len("kanji/") + KANJIVG_HEX_PADDING + len(".svg"):
                continue

            svg_file = zip.open(file_path)

            kanji_hex = svg_file.name.removeprefix("kanji/").removesuffix(".svg")
            kanji = hex_to_unicode(kanji_hex)

            if not kanji:
                continue
            
            path = f"./data/kanji/{kanji}.json"

            if not os.path.exists(path):
                print(f"Could not find {kanji}.json, closing the file and continuing.")
                svg_file.close()
                continue

            contents = svg_file.read()

            json_file = open(path, "r+")

            data = json.load(json_file)

            print(contents)
            data["svg"] = {contents}

            json_file.seek(0)
            json.dump(data, json_file, indent=4)

            json_file.close()
            svg_file.close()

if __name__ == "__main__":
    main()
