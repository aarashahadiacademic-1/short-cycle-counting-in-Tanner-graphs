# Short-cycle counting in Tanner graphs

Reproducible **final tables** for the exact KB, IMPA and local-search Exact
cycle counters, and for the interleaved Hybrid girth-cycle estimator.

**[Final full tables](FINAL_TABLE.md)** · **[17 girth-only rows CSV](FINAL_TABLE.csv)** · **[4 multi-length rows CSV](FINAL_MULTILENGTH.csv)**

## Scope

* 17 Tanner graphs for `T=g`: four-way KB / IMPA / Exact / Hybrid comparison.
* Four `(3,4)` regular affine-incidence random lifts for `g=6`, `T=8` or `T=10`: three-way KB / IMPA / Exact comparison.
* All deterministic outputs independently cross-checked against the known
  cycle counts; multi-length results also checked using canonical simple-cycle DFS.
* C++17, `-O3`, single-threaded and pinned to the same CPU throughout
  each full experiment. Seven-run medians for deterministic counters; the
  Hybrid means and MARE use 100 runs, except 30 runs for Q410 and Q412.

## Files

* `four_algorithms.cpp` — KB, IMPA, Exact and Hybrid for `T=g`.
  Exact standalone and the Hybrid exact branch share one optimized root kernel.
* `multilength.cpp` — the local BFS/residual-search Exact method, KB and IMPA
  for `g <= T < 2g`, with independent canonical DFS verification.
* `generate_graphs.py` — deterministic generation of nine primary graph inputs.
* `run_remaining.py` — the complete one-CPU 17+4 benchmark runner.
* `.github/workflows/final-benchmarks.yml` — fully automated reproduction and
  publication of the checked final tables.

## Reproduce

Open **Actions → Final benchmarks → Run workflow**.
The workflow downloads only the four original R/P **input edge lists**
from the public <https://github.com/aarashahadiacademic-1/tanner-cycle-counting>
graph corpus at runtime; historical source implementations or timing
measurements are not copied into this repository.

For local execution, check out that public graph corpus and run
`REFERENCE_GRAPH_DIR=/path/to/old-repo/graphs python3 run_remaining.py`
on Linux with Python 3, g++ and CPU affinity support.

Timing values depend on the host processor. The CPU model, compiler settings,
input checksums, sample counts and the exact measured outputs are recorded
in the final tables and CSVs.
