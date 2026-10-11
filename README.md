# Short-cycle counting in Tanner graphs

This repository contains a **single-core, four-algorithm timing comparison**
for the nine fully measured Tanner graph instances with `T = g`.

**[Final timing table](FINAL_TABLE.md)** | **[CSV data](FINAL_TABLE.csv)**

## Files

- `four_algorithms.cpp` — KB, IMPA, Exact and interleaved Hybrid counting.
  The standalone exact counter and Hybrid exact branch use the *same*
  `ExactState::runRoot()` kernel; the Hybrid yields only between complete roots.
  No `step()`/advance call is made after either branch completes.
- `generate_graphs.py` — deterministic construction of all nine evaluated graphs.
- `run_benchmarks.py` — compilation, graph generation, pinned one-core timing,
  count checks and machine-readable CSV output.
- `FINAL_TABLE.md` and `FINAL_TABLE.csv` — measured results and protocol.

## Reproduce

Requires Linux, Python 3, g++ with C++17 and `taskset`.

```sh
python3 run_benchmarks.py
```

Compilation: `g++ -std=c++17 -O3 -DNDEBUG`; fixed CPU affinity:
`taskset -c 0`. Note that timings vary with the host CPU and system load.

**Scope:** Nine completed girth-only cases. Four R/P graphs and the
separate multi-length (`T>g`) comparison are not reported until fully
measured. Nothing has been filled in from prior timing tables.
