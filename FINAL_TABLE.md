# Final table: full four-algorithm single-core benchmark

## Girth only (T = g)

| Graph | (dv,dc) | g | n | N_g | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.722 | 0.413 | **0.148** | 0.786 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 17.902 | 4.133 | 1.660 | **1.495** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 69.197 | 4.303 | **2.100** | 13.323 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 3.862 | 1.120 | **0.399** | 0.527 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 126.763 | 23.483 | 8.931 | **2.977** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 936.634 | 22.943 | **10.835** | 74.735 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 57.797 | 2.082 | **0.909** | 4.094 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 31.589 | 1.838 | **0.969** | 4.573 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 83.637 | 11.556 | 6.386 | **5.102** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 53.246 | 2.293 | **1.248** | 6.653 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 89.950 | 3.128 | **2.559** | 12.298 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 1354.251 | 66.484 | **45.307** | 68.123 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 3651.259 | 151.502 | 106.561 | **48.380** | 10.13 |

## Multiple cycle lengths (g = 6; (dv,dc) = (3,4))

| Graph | n | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---:|---:|---|---:|---:|---:|
| B16r | 320 | 8 | (34,236) | 2.922 | **0.292** | 1.007 |
| B32r | 640 | 8 | (45,237) | 7.069 | **0.602** | 2.132 |
| B64r | 1280 | 10 | (45,208,718) | 62.548 | **2.810** | 26.371 |
| B128r | 2560 | 10 | (42,215,742) | 183.964 | **7.121** | 61.348 |

## Reproducibility

* CPU: AMD EPYC 7763 64-Core Processor; pinned logical CPU 0; Linux 6.17.0-1022-azure.
* Compiler: g++ 13.3.0; single thread; -std=c++17 -O3 -DNDEBUG.
* Graph generation and file loading excluded from timed regions.
* Deterministic timings are seven-run medians. Hybrid timing is mean of 100 runs (30 for the two Q graphs).
* All deterministic girth counts are checked against references; local Exact, KB and IMPA multi-length counts also agree with an independently implemented canonical simple-cycle DFS.
* Hybrid exact and standalone Exact use the same root kernel with no extra advance after either branch wins.
* The four random B-lifts use deterministic edge-permutations of the standard affine-incidence B base. These are synthetic benchmarks, not independently famous named LDPC codes.
* Input R/P edges are read from the public graph corpus at https://github.com/aarashahadiacademic-1/tanner-cycle-counting and are not copied into this repository. No older executable, source code or timing result is imported.
* Reproduce by running the GitHub Actions workflow 'Final benchmarks', or with REFERENCE_GRAPH_DIR pointed at a checkout of that graph corpus and python3 run_remaining.py.
