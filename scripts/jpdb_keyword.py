# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import requests
import time

from utils import read_JSON, write_JSON

BASE_URL = "https://jpdb.io/kanji/"


def request_page(kanji, max_attempts = 3) -> str | None:
    url = BASE_URL + kanji

    result = None
    attempts = 0

    while result is None and attempts < max_attempts:
        req = requests.get(url)

        if req.status_code == 200:
            result = req
        else:
            time.sleep(.5)
        
        attempts += 1
        
    return result


def main():
    for path in os.scandir("./data/kanji/"):
        data = read_JSON(path)

        kanji = data["kanji"]

        result = request_page(kanji)
        
        print(result)


        time.sleep(.5)
        return


if __name__ == "__main__":
    main()