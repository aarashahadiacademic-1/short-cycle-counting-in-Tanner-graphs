# Final table — completed single-core girth-only measurements

Only the **nine actually completed and independently checked** (T=g) instances appear here. Four additional requested cases (R1200, R2400, P1200, P1600) and the separate four-instance (T>g) comparison are not included because fresh four-way benchmark runs have not been completed for them.

| Graph | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |
|---|---:|---:|---:|---:|---:|
| A16c | 1.421 | 0.261 | **0.102** | 0.620 | 8.63 |
| A128c | 14.491 | 2.652 | 1.067 | **0.929** | 8.63 |
| A128r | 54.927 | 2.405 | **1.203** | 15.786 | 0 |
| B128c | 2.887 | 0.633 | **0.268** | 0.332 | 8.33 |
| C128c | 102.302 | 16.183 | 7.108 | **2.497** | 7.70 |
| C128r | 846.475 | 13.067 | **7.563** | 114.638 | 0 |
| D16c | 66.150 | 7.545 | 3.999 | **3.545** | 7.58 |
| Q410 | 1003.179 | 43.555 | **30.752** | 65.783 | 7.14 |
| Q412 | 2737.884 | 93.609 | 79.275 | **48.986** | 10.13 |

## Reproduction protocol

* AMD EPYC 9V74; Linux; single CPU pinned with `taskset -c 0`; C++17 compiled using `g++ -std=c++17 -O3 -DNDEBUG`.
* Identical input adjacency lists for all four implementations; graph loading and construction excluded from timed sections.
* KB, IMPA and Exact: median of 7 independent executions. Hybrid: mean wall-clock of 100 executions for the first seven rows, 30 executions for Q410 and Q412; MARE is the mean absolute relative error over the same runs.
* Inverse-sampling target (r=100), alternating work budgets of 8192 adjacency probes; the exact branch is resumable between completed roots. Once either branch completes, **neither branch is called again**. Exact alone and Hybrid's exact branch share the same optimized `ExactState::runRoot()` counting kernel.
* Deterministic outputs from KB, IMPA, standalone Exact, and the full resumable Exact were checked for exact equality with the supplied reference (N_g) on all listed inputs.
* Work-budget policy is part of the method and affects timings; a different allocation between the branches changes results. The hybrid is not claimed to be universally faster than Exact.
* Source: `four_algorithms.cpp`. Machine-readable values: `FINAL_TABLE.csv`.

**Scope:** This file is the finalized record of the nine completed (T=g) experiments, **not** a claim that the originally requested complete 13+4 comparison has been finished.
