# Final timing tables

## Girth only — arithmetic means of 100 runs for all four algorithms

| Graph | (dv,dc) | g | n | Ng | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.11 | 0.29 | **0.10** | 0.78 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 11.10 | 2.49 | **0.96** | 1.08 | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 28.98 | 5.95 | 2.64 | **1.68** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 21.74 | 2.80 | **1.24** | 9.06 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 2.14 | 0.75 | **0.31** | 0.42 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 114.56 | 19.29 | 5.50 | **2.96** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 315.52 | 45.00 | 15.91 | **4.82** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 1080.13 | 133.45 | 47.61 | **6.74** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 308.42 | 18.31 | **6.19** | 60.67 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 24.61 | 1.73 | **0.92** | 4.36 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 11.34 | 1.35 | **0.83** | 4.13 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 50.90 | 7.49 | **3.75** | 3.77 | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 116.52 | 18.24 | 8.60 | **4.85** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 32.01 | 1.77 | **0.99** | 6.80 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 51.23 | 2.23 | **2.11** | 11.38 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 723.96 | 42.74 | **29.19** | 80.06 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 2050.05 | 87.40 | 70.35 | **57.64** | 10.13 |

**Fastest counts among 17 rows:** KB 0, IMPA 0, Exact 11, Hybrid 6.

### Standard deviations across the 100 runs (milliseconds)

| Graph | KB SD | IMPA SD | Exact SD | Hybrid SD |
|---|---:|---:|---:|---:|
| A16c | 0.024 | 0.023 | 0.008 | 0.054 |
| A128c | 0.287 | 0.113 | 0.037 | 0.106 |
| A256c | 0.242 | 0.255 | 0.163 | 0.161 |
| A128r | 0.349 | 0.097 | 0.068 | 0.123 |
| B128c | 0.055 | 0.047 | 0.030 | 0.050 |
| C128c | 1.649 | 0.503 | 0.156 | 0.297 |
| C256c | 5.648 | 0.921 | 0.558 | 0.457 |
| C512c | 54.679 | 7.254 | 0.513 | 0.698 |
| C128r | 6.021 | 0.593 | 0.212 | 0.904 |
| R1200 | 0.702 | 0.054 | 0.027 | 0.116 |
| R2400 | 0.299 | 0.069 | 0.020 | 0.071 |
| D16c | 0.325 | 0.179 | 0.085 | 0.358 |
| D32c | 0.441 | 0.304 | 0.151 | 0.456 |
| P1200 | 0.612 | 0.086 | 0.069 | 0.190 |
| P1600 | 0.379 | 0.054 | 0.045 | 0.118 |
| Q410 | 4.469 | 0.926 | 0.472 | 8.141 |
| Q412 | 11.125 | 1.817 | 0.787 | 5.904 |

## Multiple cycle lengths — previous seven-run medians

| Graph | g | T | Counts | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---|---:|---:|---:|
| A16c | 6 | 8 | (2560,25488) | 2.95 | **1.27** | 6.83 |
| A16c | 6 | 10 | (2560,25488,133632) | 4.20 | **2.57** | 72.00 |
| A128c | 6 | 8 | (20480,203904) | 28.76 | **12.90** | 67.38 |
| A128c | 6 | 10 | (20480,203904,1069056) | 41.91 | **25.27** | 655.13 |
| A128r | 6 | 8 | (176,1709) | 463.67 | **15.96** | 92.45 |
| A128r | 6 | 10 | (176,1709,8987) | 1719.66 | **39.79** | 863.19 |
| B128c | 6 | 8 | (4608,26624) | 6.28 | **2.83** | 8.12 |
| B128c | 6 | 10 | (4608,26624,76800) | 8.77 | **4.67** | 42.19 |
| C128r | 6 | 8 | (1590,27488) | 7105.26 | **118.83** | 1372.75 |
| R1200 | 6 | 8 | (1564,24433) | 167.73 | **10.16** | 114.26 |
| R1200 | 6 | 10 | (1564,24433,409604) | 287.09 | **41.56** | 2317.71 |
| R2400 | 6 | 8 | (155,1212) | 174.78 | **6.68** | 37.71 |
| R2400 | 6 | 10 | (155,1212,9832) | 492.37 | **16.57** | 366.70 |
| P1200 | 8 | 10 | (65,10561) | 122.33 | **6.79** | 54.10 |
| P1200 | 8 | 12 | (65,10561,87882) | 198.04 | **21.56** | 529.98 |
| P1600 | 10 | 12 | (11,2998) | 202.13 | **8.06** | 40.73 |
| P1600 | 10 | 14 | (11,2998,21441) | 331.54 | **17.83** | 243.25 |
| Q410 | 10 | 12 | (40448,353920) | 3062.12 | **165.79** | 900.03 |

## Measurement protocol

* 100 randomized-order runs of each of KB, IMPA, Exact and Hybrid for every one of the 17 girth-only graphs. All four algorithms execute from the unchanged `four_algorithms.cpp` functions (KB's previously validated optimization included), compiled C++17 -O3 -DNDEBUG.
* Each run is pinned to one logical CPU. Means, not medians, appear in the upper table; standard deviations are retained alongside them in `FINAL_TABLE.csv`.
* Each of the 100 KB, IMPA and Exact counts per graph matched the verified `Ng`; Hybrid uses r=100 closures or exact fallback and 100 independent seeds.
* The earlier multiple-length experiments are unchanged and still report medians of seven runs, as labeled.
* All 17 measurements completed in the [GitHub Actions log](https://github.com/aarashahadiacademic-1/short-cycle-counting-in-Tanner-graphs/actions/runs/38189770807). Only table formatting failed after the measurements finished; numbers were recovered from the `VERIFIED_100` records.
* Input graph SHA-256 hashes are included in `FINAL_TABLE.csv`. Reproduction code: `benchmark_100.cpp`, `run_100.py`.

