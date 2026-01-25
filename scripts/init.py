# Run this script to create the initial JSON files for each kanji. 
# Kanji are sourced from KanjiVG at https://github.com/KanjiVG/kanjivg

import requests
import re

def is_valid_kanji(kanji):
    KANJI_RE = re.compile(
        r'['
        r'\u3400-\u4dbf'                # Ext A
        r'\u4e00-\u9fff'                # BMP ideographs
        r'\U00020000-\U0002A6DF'        # Ext B
        r'\U0002A700-\U0002EBEF'        # Ext C–F
        r'\uF900-\uFAFF'                # CJK Compatibility Ideographs
        r'\u2E80-\u2EFF\u2F00-\u2FDF'   # Radicals
        r']+'
    )
    
    if len(kanji) != 1 or not re.fullmatch(KANJI_RE, kanji):
        print(f"{kanji} is not a valid kanji.")
        return False
    
    return True

def main():
    kvg_index = requests.get("https://raw.githubusercontent.com/KanjiVG/kanjivg/refs/heads/master/kvg-index.json").json()

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
