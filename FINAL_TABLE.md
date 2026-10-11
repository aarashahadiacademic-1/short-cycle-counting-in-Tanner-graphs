# Final table: full four-algorithm single-core benchmark

## Girth only (T = g)

| Graph | (dv,dc) | g | n | N_g | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.728 | 0.417 | **0.148** | 0.787 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 17.871 | 4.086 | 1.643 | **1.530** | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 36.419 | 8.616 | 4.087 | **1.748** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 68.658 | 4.304 | **2.080** | 13.517 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 3.857 | 1.116 | **0.398** | 0.519 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 120.562 | 23.345 | 9.214 | **2.976** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 273.073 | 47.423 | 19.115 | **3.157** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 645.779 | 119.431 | 42.901 | **3.686** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 903.142 | 22.463 | **10.642** | 75.040 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 56.743 | 2.088 | **0.910** | 4.113 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 32.023 | 1.880 | **0.972** | 4.682 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 82.421 | 11.433 | 6.206 | **5.105** | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 176.506 | 24.568 | 14.554 | **6.018** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 53.217 | 2.261 | **1.256** | 6.731 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 91.715 | 3.138 | **2.396** | 12.401 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 1359.848 | 61.942 | **41.621** | 62.791 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 3663.500 | 149.050 | 101.890 | **44.488** | 10.13 |

## Multiple cycle lengths (g = 6; (dv,dc) = (3,4))

| Graph | n | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---|---:|---:|---:|
| B16r | 320 | 8 | (34,236) | 2.924 | **0.290** | 1.008 |
| B32r | 640 | 8 | (45,237) | 7.127 | **0.606** | 2.136 |
| B64r | 1280 | 10 | (45,208,718) | 63.265 | **2.845** | 26.310 |
| B128r | 2560 | 10 | (42,215,742) | 181.439 | **6.754** | 65.058 |
| F5-32r | 640 | 8 | (43,231) | 7.352 | **0.619** | 2.151 |
| F5-64r | 1280 | 8 | (32,266) | 18.856 | **1.396** | 4.454 |
| F7-64r | 1792 | 8 | (31,211) | 29.408 | **2.129** | 6.878 |
| G7-64r | 2688 | 8 | (168,1653) | 188.207 | **7.084** | 36.921 |

## Reproducibility

These four prospective affine-incidence random lifts were selected after a parameter scan. Exact beats KB on these cases, but not IMPA. Their complete reproducible construction appears in append_multi.py; the independent canonical simple-cycle DFS checks all counts.

* CPU: AMD EPYC 7763 64-Core Processor; pinned logical CPU 0; Linux 6.17.0-1022-azure.
* Compiler: g++ 13.3.0; single thread; -std=c++17 -O3 -DNDEBUG.
* Graph generation and file loading excluded from timed regions.
* Deterministic timings are seven-run medians. Hybrid timing is mean of 100 runs (30 for the two Q graphs).
* All deterministic girth counts are checked against references; local Exact, KB and IMPA multi-length counts also agree with an independently implemented canonical simple-cycle DFS.
* Hybrid exact and standalone Exact use the same root kernel with no extra advance after either branch wins.
* The four random B-lifts use deterministic edge-permutations of the standard affine-incidence B base. These are synthetic benchmarks, not independently famous named LDPC codes.
* Input R/P edges are read from the public graph corpus at https://github.com/aarashahadiacademic-1/tanner-cycle-counting and are not copied into this repository. No older executable, source code or timing result is imported.
* Reproduce by running the GitHub Actions workflow 'Final benchmarks', or with REFERENCE_GRAPH_DIR pointed at a checkout of that graph corpus and python3 run_remaining.py.
