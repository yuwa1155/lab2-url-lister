#!/usr/bin/env python3
import sys

current_url = None
total = 0

# Hadoop sorts mapper output so identical URLs arrive together.
for line in sys.stdin:
    url, count = line.rstrip("\n").rsplit("\t", 1)
    count = int(count)

    if url == current_url:
        total += count
    else:
        if current_url is not None and total > 5:
            print(f"{current_url}\t{total}")
        current_url = url
        total = count

# Flush the final URL group.
if current_url is not None and total > 5:
    print(f"{current_url}\t{total}")
