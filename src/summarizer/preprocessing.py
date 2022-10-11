# Copyright 2022 NASK-PIB
# FIND TERMS AND CONDITIONS IN LICENSE FILE:
# github.com/ZILiAT-NASK/Summarizer/LICENSE

import re


def preprocess(text):
    flags = re.IGNORECASE | re.MULTILINE
    # word + optional number as line
    text = re.sub(r"^\s*\w+\.?[\s\.\divxcm]+$", "", text, flags=flags)
    text = re.sub(r"^\s*[\.\divxcm]+[\)\.:]?\s+", "", text, flags=flags)
    text = re.sub(r"^\s*\w\w?[\)\.:]", "", text, flags=flags)

    headers = "artykuł paragraf sekcja fragment".replace(' ', '|')
    shorts = "art parag frag".replace(' ', '|')
    text = re.sub(fr"^\s*({headers})\s*[\.\divxcm]+\s", "", text, flags=flags)
    text = re.sub(fr"^\s*({shorts})\.\s*[\.\divxcm]+\s", "", text, flags=flags)

    # Add . if line not ending with punct
    punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    text = re.sub(fr"([^{punct}])\s*$", "\g<1>.", text, flags=flags)
    text = re.sub(r"\s+", " ", text, flags=flags)
    text = re.sub(r"^\s", "", text, flags=flags)
    text = re.sub(r"\s$", "", text, flags=flags)
    return text
