# Final table: four-algorithm girth-cycle timing comparison

| Graph | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---:|---:|---:|---:|---:|
| A16c | 1.341 | 0.258 | **0.105** | 0.621 | 8.63 |
| A128c | 14.801 | 2.522 | **0.963** | 0.969 | 8.63 |
| A128r | 54.901 | 2.528 | **1.180** | 16.037 | 0.00 |
| B128c | 2.832 | 0.646 | **0.272** | 0.345 | 8.33 |
| C128c | 96.211 | 15.171 | 6.823 | **2.235** | 7.70 |
| C128r | 854.593 | 13.472 | **6.839** | 117.555 | 0.00 |
| D16c | 64.921 | 7.269 | 4.238 | **3.470** | 7.58 |
| Q410 | 1010.770 | 46.854 | **30.534** | 72.256 | 7.14 |
| Q412 | 2842.791 | 92.786 | 84.886 | **45.719** | 10.13 |

## Measurement protocol

All four algorithms were executed as single-threaded C++17 code, compiled with `g++ -std=c++17 -O3 -DNDEBUG`, and pinned to one CPU (`taskset -c 0`) on the same AMD EPYC 9V74 environment. Input graph construction and disk loading are not timed.

KB, IMPA and Exact report medians of seven independent executions. Hybrid reports mean elapsed time and mean absolute relative error from 100 runs, except Q410/Q412 (30 runs). The inverse-sampling target is (r=100), and the scheduler alternates 8192 adjacency-probe credits per branch, with root-granularity preemption for the exact part. There are no further `advance()` calls after either branch finishes.

The standalone Exact and Hybrid's exact branch use exactly the same `ExactState::runRoot()` kernel. IMPA chooses direct label-pair accumulation at small meetings and a mathematically equivalent cumulative distinct-label sum when the meeting contains more than five incoming edges. KB retains sparse/nonzero-message processing, per-node sums, reverse-edge subtraction and suppression of earlier roots: no unverified rewrite was made merely to reduce its displayed time.

All deterministic counts (KB, IMPA, Exact, full resumable Exact) were checked to equal the supplied (N_g) values for the nine included instances. Source: `four_algorithms.cpp`. Regeneration: `python3 run_benchmarks.py`. Machine-readable data: `FINAL_TABLE.csv`.

**Coverage:** These nine (T=g) rows are the fully completed and remeasured subset. The R1200/R2400/P1200/P1600 rows and the requested separate four-instance (T>g) table have not yet received the required reproducible four-algorithm timing runs and are therefore omitted.
