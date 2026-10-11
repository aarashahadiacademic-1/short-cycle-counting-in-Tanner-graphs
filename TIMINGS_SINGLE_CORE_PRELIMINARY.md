# Fresh single-core timing experiment — preliminary (2026-10-12)

AMD EPYC 9V74; C++17, g++ -O3 -DNDEBUG; CPU affinity pinned to CPU 0 (`taskset -c 0`); graph loading excluded. KB/IMPA/Exact are seven-run medians; Hybrid time is the arithmetic mean, and MARE is over the stated number of independent trials. Interleaved inverse sampling uses r=100 and a resumable exact state, Q=1024 adjacency-probe credits per turn. No redundant `advance()` after a winner is declared. All deterministic counters (KB, IMPA, Exact, resumable exact) independently returned the same N_g in each shown row. **These are preliminary timings and should not be substituted into the submitted manuscript without full benchmarking verification.**

| Instance | KB ms | IMPA ms | Exact ms | Hybrid ms | MARE % | Hybrid runs |
|---|---:|---:|---:|---:|---:|---:|
| A16c | 1.464 | 0.251 | 0.101 | 0.982 | 8.63 | 100 |
| A128c | 15.199 | 2.703 | 1.024 | 1.591 | 8.63 | 100 |
| A128r | 60.321 | 3.041 | 1.165 | 23.511 | 0 | 100 |
| B128c | 2.899 | 0.647 | 0.267 | 0.54 | 8.33 | 100 |
| C128c | 103.552 | 17.369 | 6.849 | 3.687 | 7.7 | 100 |
| C128r | 866.491 | 13.52 | 7.394 | 153.999 | 0 | 100 |
| D16c | 66.656 | 8.034 | 4.216 | 4.741 | 7.58 | 100 |
| Q410 | 979.244 | 41.999 | 31.085 | 81.74 | 7.14 | 30 |
| Q412 | 2588.84 | 98.578 | 80.597 | 60.473 | 10.13 | 30 |

**Not measured:** R1200, R2400, P1200, P1600, and four multi-length (3,4) benchmarks with T=8 or T=10. These must be genuinely generated and benchmarked, not filled using previous manuscript data. The locally executed C++ benchmarking source is provided separately for inspection and must be uploaded to this repository after full reproducibility review.
