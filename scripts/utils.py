import re

def is_valid_kanji(kanji: str):
    """
    Returns whether a character is a valid Kanji or radical.

    Includes characters under BMP ideographs, EXT A, EXT B, EXT C-F, CJK Compatibility Ideographs, and radicals.

    The ``kanji`` parameter should be a single character or ``is_valid_kanji()`` will return ``False``.

    :param kanji: The kanji character
    :type kanji: str
    :return: Validity
    :rtype: bool
    """

    KANJI_RE = re.compile(
        r'['
        r'\U00004E00-\U00009FFF'        # CJK Unified Ideographs
        r'\U00003400-\U00004DBf'        # CJK Unified Ideographs Extension A
        r'\U00020000-\U0002A6DF'        # CJK Unified Ideographs Extension B
        r'\U0000F900-\U0000FAFF'        # CJK Compatibility Ideographs
        r'\U00002E80-\U00002EFF'        # CJK Radicals Supplement
        r']+'
    )
    
    if len(kanji) != 1 or not re.fullmatch(KANJI_RE, kanji):
        print(f"{kanji} is not a valid kanji.")
        return False
    
    return True