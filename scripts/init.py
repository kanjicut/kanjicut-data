# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import requests

from kanjivg import get_kvg_index
from utils import is_valid_kanji

def main():
    """
    Creates the initial JSON files for each kanji.

    This script does not need to be ran more than once unless completely rebuilding the data.
    """

    if not os.path.exists("data/kanji/"):
        os.mkdir("data/kanji/")

    if not os.path.exists("data/keywords/"):
        os.mkdir("data/keywords/")

    response = requests.get("https://raw.githubusercontent.com/KanjiVG/kanjivg/refs/heads/master/kvg-index.json")

    if response.status_code != 200:
        print(f"Attempting to retrieve KanjiVG index results in {response.status_code}. Aborting process.")
        return
    
    kvg_index = get_kvg_index()

    for kanji in kvg_index:

        if is_valid_kanji(kanji):
            try:
                open(f"./data/kanji/{kanji}.json", "x")
            except FileExistsError:
                print(f"{kanji}.json already exists and was not created.")
            except:
                print(f"Error when creating {kanji}.json.")

if __name__ == "__main__":
    main()
