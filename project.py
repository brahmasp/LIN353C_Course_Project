#!/usr/bin/env python3

import glob
import re

from collections import Counter

for filename in glob.glob('books/*.txt'):
    f = open(filename, 'r', encoding='utf8')
    text = f.read()
    #re_start = re.search(r'\*\*\* ?START OF THIS PROJECT GUTENBERG EBOOK .* ?\*\*\*',text)
    #re_end = re.search(r'\*\*\* ?END OF THIS PROJECT GUTENBERG EBOOK .* ?\*\*\*', text)
    re_start = re.search(r'\*\*\*\s?START.*\*\*\*', text)
    re_end = re.search(r'\*\*\*\s?END.*\*\*\*', text)

    text = text[re_start.span()[1] : re_end.span()[0]-1].strip()
    print(text[-100:])

    words = text.split()

    break
