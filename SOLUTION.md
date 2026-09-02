# Lab 2: URL Count

## Implementation

This solution uses Python 3 and Hadoop Streaming.

URLMapper.py reads standard input line by line and uses the regular
expression `\bhref="([^"]*)"` to extract double-quoted href values.
It finds multiple links on the same line and emits each nonempty
value followed by a tab and 1. Links are counted exactly as written;
relative links and fragment links are included.

Hadoop groups and sorts mapper output by URL. URLReducer.py adds
the counts for each URL and outputs only totals greater than 5.
It also outputs the final group when the input ends.

Filtering must happen after all counts for a URL are combined.
For example, a URL appearing 3 times in each of two mapper inputs
has a total of 6 and must be included. Filtering each partial count
would incorrectly discard it. For this reason, URLReducer.py is
not used as a combiner.

## Requirements and execution

Requirements: Python 3, Hadoop with its Streaming JAR, and make.
The provided input preparation also requires curl.
Running the original Java WordCount requires a JDK.

On CSEL, Hadoop 3.3.6 was used:

```bash
make prepare
make run
make urlstream
```

The output directory must not already exist. To choose a new one:

```bash
make urlstream URL_OUTPUT=url-output-new
```

The Makefile's STREAM_JAR variable can be overridden if Hadoop is
installed at a different location.

## CSEL validation

The original Java WordCount and the Python URLCount Streaming job
both completed successfully.

The local pipeline was also tested:

```bash
cat input/file01 input/file02 | python3 URLMapper.py | LC_ALL=C sort | python3 URLReducer.py
```

Its output matched the sorted Hadoop output exactly using diff.
The Hadoop counters reported 2,457 mapper output records,
1,973 distinct URL groups, and 10 final output records.

The saved output is in results/csel-url-count.txt.
Counts depend on the downloaded versions of the Wikipedia pages.

## Dataproc timing comparison

Pending: run URLCount with one master and two workers, then with
one master and four workers. Record the actual elapsed times and
compare the results using the same input data.

## Resources and assistance

- The course lab README, Makefile, and starter code.
- ChatGPT assisted with the Python implementation, Makefile changes,
  testing commands, debugging guidance, and this writeup.
