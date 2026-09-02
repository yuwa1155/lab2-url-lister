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

URLCount was executed through SSH on the Dataproc master node.
Both measured configurations used one e2-standard-2 master,
e2-standard-2 workers, and 100 GB boot disks in us-central1-a.
The same two Wikipedia input files in HDFS and the same Python
mapper and reducer were used for both runs. The reducer count
was explicitly fixed at one.

| Workers | Elapsed time (seconds) | Output records |
| --- | ---: | ---: |
| 2 | 67.396 | 10 |
| 4 | 59.509 | 10 |

Elapsed time is the Bash time command's real value for the complete
Hadoop Streaming submission, including submission and scheduling
overhead. Cluster creation, scaling, and file transfers were excluded.

The four-worker run took 7.887 seconds less, an approximately 11.7%
reduction in elapsed time, or a 1.13x speedup. Doubling the worker
count did not halve the runtime. Both jobs launched 10 map tasks
and one reduce task. Additional workers can execute more map tasks
concurrently, but job startup, scheduling, shuffle, and the single
reducer limit the benefit for this small input.

Each configuration was measured once. These results demonstrate
the observed runtimes, rather than a statistically established
performance improvement. Cache state, data locality, and scheduling
variation may also affect the comparison.

Both jobs completed successfully and produced 10 output records.
A diff comparison confirmed that the two output files were identical.

Saved evidence:
- results/dataproc-2workers-100gb.log
- results/dataproc-4workers-100gb.log
- results/dataproc-2workers-100gb-output.txt
- results/dataproc-4workers-100gb-output.txt

An earlier run with default disk sizes took 65.744 seconds.
It is excluded from this comparison because expansion encountered
a disk quota limit. The cluster was recreated with 100 GB disks,
and both worker configurations were then measured with that setup.

## Resources and assistance

- The course lab README, Makefile, and starter code.
- ChatGPT assisted with the Python implementation, Makefile changes,
  testing commands, debugging guidance, and this writeup.
