# Final table: full four-algorithm single-core benchmark

## Girth only (T = g)

| Graph | (dv,dc) | g | n | N_g | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.322 | 0.283 | **0.105** | 0.684 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 13.950 | 2.521 | 1.028 | **1.024** | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 30.033 | 5.603 | 2.455 | **1.317** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 53.539 | 2.587 | **1.244** | 9.300 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 2.974 | 0.676 | **0.284** | 0.376 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 97.661 | 18.229 | 5.974 | **2.386** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 286.936 | 42.619 | 14.169 | **2.775** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 649.407 | 117.847 | 40.877 | **3.100** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 818.691 | 14.978 | **7.191** | 58.828 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 45.364 | 1.565 | **0.734** | 3.605 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 24.020 | 1.185 | **0.686** | 3.650 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 63.779 | 7.439 | 3.822 | **3.597** | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 144.190 | 18.346 | 9.058 | **4.709** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 41.377 | 1.553 | **0.938** | 5.860 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 66.339 | 1.950 | **1.893** | 9.820 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 929.199 | 46.049 | **33.652** | 89.242 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 2447.137 | 98.289 | 77.241 | **52.790** | 10.13 |

## Multiple cycle lengths (g = 6; (dv,dc) = (3,4))

| Graph | n | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---|---:|---:|---:|
| B16r | 320 | 8 | (34,236) | 2.412 | **0.200** | 0.674 |
| B32r | 640 | 8 | (45,237) | 5.758 | **0.412** | 1.442 |
| B64r | 1280 | 10 | (45,208,718) | 46.657 | **1.734** | 16.688 |
| B128r | 2560 | 10 | (42,215,742) | 135.530 | **3.906** | 38.022 |

## Reproducibility

* CPU: AMD EPYC 9V74 80-Core Processor; pinned logical CPU 0; Linux 6.17.0-1022-azure.
* Compiler: g++ 13.3.0; single thread; -std=c++17 -O3 -DNDEBUG.
* Graph generation and file loading excluded from timed regions.
* Deterministic timings are seven-run medians. Hybrid timing is mean of 100 runs (30 for the two Q graphs).
* All deterministic girth counts are checked against references; local Exact, KB and IMPA multi-length counts also agree with an independently implemented canonical simple-cycle DFS.
* Hybrid exact and standalone Exact use the same root kernel with no extra advance after either branch wins.
* The four random B-lifts use deterministic edge-permutations of the standard affine-incidence B base. These are synthetic benchmarks, not independently famous named LDPC codes.
* Input R/P edges are read from the public graph corpus at https://github.com/aarashahadiacademic-1/tanner-cycle-counting and are not copied into this repository. No older executable, source code or timing result is imported.
* Reproduce by running the GitHub Actions workflow 'Final benchmarks', or with REFERENCE_GRAPH_DIR pointed at a checkout of that graph corpus and python3 run_remaining.py.
