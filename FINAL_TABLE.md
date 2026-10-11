# Final table: KB, IMPA, Exact, and Hybrid (T = g)

| Graph | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---:|---:|---:|---:|---:|
| A16c | 1.433 | 0.301 | **0.097** | 0.800 | 4.30 |
| A128c | 14.347 | 2.459 | **1.096** | 1.234 | 8.63 |
| A128r | 54.378 | 2.438 | **1.128** | 11.486 | 0.00 |
| B128c | 2.782 | 0.629 | **0.251** | 0.444 | 8.33 |
| C128c | 97.669 | 16.168 | 5.874 | **3.155** | 7.70 |
| C128r | 874.293 | 16.453 | **8.295** | 79.531 | 0.00 |
| D16c | 73.748 | 7.344 | **4.149** | 5.729 | 7.58 |
| Q410 | 981.681 | 43.750 | **36.901** | 70.187 | 7.14 |
| Q412 | 2594.733 | 96.660 | 75.509 | **53.152** | 10.13 |

## Protocol and reproducibility

All four methods run in a single-threaded C++17 binary, compiled with `g++ -std=c++17 -O3 -DNDEBUG`, pinned to CPU 0 using `taskset -c 0` in the same AMD EPYC 9V74 environment. Graph generation and file loading are excluded from the timed interval. The three deterministic methods report the median of seven runs. Hybrid time and MARE are means over 100 independent runs (30 for Q410 and Q412), with inverse-sampling target `r = 100`.

**Implementation equivalence:** The original algorithms are preserved. The standalone Exact and the interleaved Hybrid's exact side share `ExactState::runRoot()`. It records each distinct meeting vertex once, avoiding a duplicate neighbor scan; it reuses BFS buffers. Hybrid's exact side yields only between roots and stops upon the first completed branch. KB retains sparse message propagation, vertex aggregation, reverse-edge subtraction and earlier-root suppression. IMPA uses direct label-pair counts for meetings with at most five incoming edges and equivalent cumulative label counts for larger meetings.

The exact counts of KB, IMPA, standalone Exact and complete resumable Exact agree with the reference `N_g` for every row. The benchmark schedule alternates 8192 adjacency-probe credits per side. The work-budget policy and stopping behavior are part of the reported hybrid configuration, not universally optimal.

**Reproduce:** Run `python3 run_benchmarks.py`. Sources: `four_algorithms.cpp` and `generate_graphs.py`. Numerical data: `FINAL_TABLE.csv`.

**Scope:** These are the nine fully measured girth-only cases. Four R/P examples and the separate `T>g` four-instance comparison have not been measured under this final protocol and are not represented here.


## Multiple lengths: completed (3,4)-regular benchmarks

These four independently generated random lifts of the affine-incidence B base
were run on the same pinned CPU. All reported cycle counts agree across
local-search Exact, KB, IMPA and independent canonical simple-cycle DFS.
Hybrid here is intentionally omitted: the hybrid estimator targets girth cycles,
not simultaneous multi-length cycle counts.

| Graph | n | g | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---:|---|---:|---:|---:|
| B16r | 320 | 6 | 8 | (34,236) | 3.344 | **0.187** | 0.795 |
| B32r | 640 | 6 | 8 | (45,237) | 6.639 | **0.369** | 1.824 |
| B64r | 1280 | 6 | 10 | (45,208,718) | 49.866 | **2.721** | 18.323 |
| B128r | 2560 | 6 | 10 | (42,215,742) | 155.624 | **3.852** | 40.187 |

These are synthetic lifts of a well-known affine-incidence construction,
not four individually famous standardized LDPC codes. Times are medians of
seven C++17 -O3 executions with CPU affinity fixed; graph construction and
loading excluded. The exact counter uses the BFS-arm / residual-DFS method,
not the canonical DFS used solely to validate its answer.
Source: `multilength.cpp`. Data: `FINAL_MULTILENGTH.csv`.

**Complete 13-row remeasurement:** the automated `run_remaining.py` script
reads the original R/P graph *inputs* from the external public graph repository
without importing its old implementations or timing results. This script has
not yet produced a verified full 13-row file. Therefore no R/P timings are
listed as completed here.
