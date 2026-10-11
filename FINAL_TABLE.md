# Final tables: girth and cycle-rich near-girth counting

## Girth-only (T=g)
| Graph | (dv,dc) | g | n | Ng | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A16c | (3,6) | 6 | 672 | 2560 | 1.727 | 0.409 | **0.147** | 0.782 | 4.30 |
| A128c | (3,6) | 6 | 5376 | 20480 | 17.690 | 4.083 | 1.621 | **1.540** | 8.63 |
| A256c | (3,6) | 6 | 10752 | 40960 | 36.506 | 8.541 | 3.947 | **1.770** | 8.63 |
| A128r | (3,6) | 6 | 5376 | 176 | 68.793 | 4.375 | **2.062** | 13.333 | 0.00 |
| B128c | (3,4) | 6 | 2560 | 4608 | 3.853 | 1.115 | **0.390** | 0.510 | 8.33 |
| C128c | (4,8) | 6 | 11264 | 204928 | 113.976 | 22.763 | 8.950 | **2.964** | 7.70 |
| C256c | (4,8) | 6 | 22528 | 409856 | 278.783 | 55.339 | 19.169 | **3.188** | 7.70 |
| C512c | (4,8) | 6 | 45056 | 819712 | 650.039 | 116.821 | 42.886 | **3.580** | 7.70 |
| C128r | (4,8) | 6 | 11264 | 1590 | 916.379 | 22.822 | **10.707** | 72.700 | 0.00 |
| R1200 | (4,8) | 6 | 1200 | 1564 | 57.539 | 2.112 | **0.907** | 4.122 | 0.00 |
| R2400 | (3,6) | 6 | 2400 | 155 | 31.591 | 1.824 | **0.949** | 4.643 | 0.00 |
| D16c | (3,6) | 8 | 4992 | 57680 | 82.439 | 11.545 | 9.398 | **5.117** | 7.58 |
| D32c | (3,6) | 8 | 9984 | 115360 | 175.206 | 24.231 | 14.425 | **5.989** | 7.58 |
| P1200 | (3,6) | 8 | 1200 | 65 | 53.900 | 2.282 | **1.243** | 6.634 | 0.00 |
| P1600 | (3,4) | 10 | 1600 | 11 | 90.834 | 3.061 | **2.473** | 11.754 | 0.00 |
| Q410 | (3,4) | 10 | 40448 | 40448 | 1344.996 | 62.319 | **41.410** | 61.888 | 7.14 |
| Q412 | (3,4) | 12 | 36352 | 308992 | 3618.437 | 140.926 | 103.891 | **44.377** | 10.13 |

## Multiple cycle lengths: low degrees, large cycle counts (g=6,T=8)

| Graph | (dv,dc) | n | (N6,N8) | KB (ms) | IMPA (ms) | Exact (ms) |
|---|---|---:|---|---:|---:|---:|
| B128c | (3,4) | 2560 | (4608,26624) | 6.743 | **2.803** | 8.538 |
| B256c | (3,4) | 5120 | (9216,53248) | 15.062 | **6.063** | 19.890 |
| B512c | (3,4) | 10240 | (18432,106496) | 29.518 | **12.761** | 44.860 |
| A128c | (3,6) | 5376 | (20480,203904) | 31.151 | **12.861** | 72.323 |
| A256c | (3,6) | 10752 | (40960,407808) | 65.734 | **27.794** | 152.797 |

## Reproduction

* All measurements are from one pinned CPU per complete run, g++ C++17 -O3 -DNDEBUG.
* Seven-run medians for deterministic counters; hybrid means from the girth-only benchmark.
* The girth-only Exact and Hybrid share an optimized root kernel.
* Each multiple-length Exact / KB / IMPA count vector agrees with the independent canonical simple-cycle DFS in multilength.cpp.
* Graphs are deterministic cyclic lifts of standard affine-incidence constructions, not standardized LDPC codes.
* Their full edge-list generation and benchmark commands are in rich_multilength.py.
* Results are empirical timing comparisons, not a claim of uniform algorithmic dominance.
