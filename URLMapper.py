#!/usr/bin/env python3
import re
import sys

# Extract every double-quoted href value on each input line.
pattern = re.compile(r'\bhref="([^"]*)"')

for line in sys.stdin:
    for url in pattern.findall(line):
        if url:
            print(f"{url}\t1")
