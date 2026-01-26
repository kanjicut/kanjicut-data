# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Run this script to create the initial JSON files for each kanji. 
# Kanji are sourced from KanjiVG at https://github.com/KanjiVG/kanjivg

import requests
import zipfile
import io
import os

KANJIVG_LATEST_RELEASE = "https://api.github.com/repos/KanjiVG/kanjivg/releases/latest"

def main():
    # Use GitHub Rest API to retrieve the latest KanjiVG release
    response = requests.get(KANJIVG_LATEST_RELEASE, headers={
        "Accept": "application/vnd.github.v3+json"
    })

    if response.status_code != 200:
        print(f"Attempting to retrieve the latest releases resulted in a status code of {response.status_code}. Aborting process.")
        return
    
    # Index the first release (kanjivg-all) and get its download URL
    latest_json = response.json()

    download_url = latest_json["assets"][0]["browser_download_url"]
    
    # Download the ZIP file
    response = requests.get(download_url)

    if response.status_code != 200:
        print(f"Attempting to download the latest release resulted in a status code of {response.status_code}. Aborting process.")
        return
    
    # Open the ZIP file
    with zipfile.ZipFile(io.BytesIO(response.content)) as kanjivg_zip:
        for file_path in kanjivg_zip.namelist():
            with kanjivg_zip.open(file_path) as file:
                contents = file.read()

                # Convert from hexcode to char
                
                if os.path.exists(f"./kanji/{kanji}"):
                    print("Path exists! Yipee")

if __name__ == "__main__":
    main()
