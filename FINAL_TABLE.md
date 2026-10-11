# Final table: full four-algorithm single-core benchmark

## Girth only (T = g)

| Graph | (dv,dc) | g | n | N_g | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.831 | 0.423 | **0.147** | 0.785 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 17.683 | 4.072 | 1.652 | **1.487** | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 36.555 | 8.494 | 4.033 | **1.735** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 68.321 | 4.305 | **2.066** | 13.281 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 3.808 | 1.112 | **0.386** | 0.474 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 112.747 | 22.973 | 8.826 | **2.979** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 277.125 | 51.348 | 19.299 | **3.228** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 688.188 | 130.244 | 44.285 | **3.704** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 912.339 | 22.349 | **10.912** | 73.224 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 56.926 | 2.068 | **0.916** | 4.132 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 31.610 | 1.836 | **0.989** | 4.658 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 82.587 | 11.448 | 6.187 | **5.091** | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 175.296 | 24.285 | 14.500 | **5.997** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 53.626 | 2.298 | **1.256** | 6.763 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 90.897 | 3.079 | **2.575** | 11.763 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 1344.920 | 65.197 | **41.851** | 63.545 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 3639.371 | 144.683 | 102.097 | **44.780** | 10.13 |

## Multiple cycle lengths (g = 6; (dv,dc) = (3,4))

| Graph | n | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---|---:|---:|---:|
| B16r | 320 | 8 | (34,236) | 2.953 | **0.292** | 1.014 |
| B32r | 640 | 8 | (45,237) | 7.118 | **0.612** | 2.138 |
| B64r | 1280 | 10 | (45,208,718) | 62.974 | **2.869** | 26.406 |
| B128r | 2560 | 10 | (42,215,742) | 180.902 | **6.777** | 66.082 |
| F5-32r | 640 | 8 | (43,231) | 7.174 | **0.607** | 2.162 |
| F5-64r | 1280 | 8 | (32,266) | 18.259 | **1.381** | 4.469 |
| F7-64r | 1792 | 8 | (31,211) | 29.342 | **2.098** | 6.730 |
| G7-64r | 2688 | 8 | (168,1653) | 186.542 | **7.016** | 35.301 |

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
