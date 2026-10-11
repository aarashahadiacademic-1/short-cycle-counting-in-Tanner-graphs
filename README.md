# Short-cycle counting in Tanner graphs

Final, reproducible timings comparing KB, IMPA, Exact and Hybrid on Tanner graphs.

[Final table (LaTeX)](FINAL_TABLE.tex) · [Final table (Markdown)](FINAL_TABLE.md) · [Girth-only CSV](FINAL_TABLE.csv) · [Near-girth CSV](FINAL_MULTILENGTH.csv)

## Benchmarks

- **17 girth-only** cases (`T=g`): KB, IMPA, Exact and Hybrid.
- **5 near-girth** cases (`g=6,T=8`): KB, IMPA and Exact. All are low-degree `(3,4)` or `(3,6)` cyclic lifts of affine-incidence bases, with `N_6>=4608` and `N_8>=26624`. There are **no (3,3)** cases.
- Counts are checked using independently implemented canonical simple-cycle DFS for the near-girth experiments.
- These cycle-rich near-girth examples show that IMPA and KB can both beat Exact. They are included as a balanced empirical comparison, not to demonstrate a predetermined ranking.

## Reproduction

Source files: `four_algorithms.cpp` (girth-only), `multilength.cpp` (near-girth), `generate_graphs.py`, `rich_multilength.py`, and `run_remaining.py`.

In **Actions → Final benchmarks (cycle-rich low-degree) → Run workflow**, the workflow builds all sources with C++17 `-O3 -DNDEBUG`, pins execution to one logical CPU, executes the full comparison, independently verifies counts, and updates the CSV/Markdown/LaTeX together. Timings exclude file loading and graph construction. Deterministic runtimes are medians of seven executions. Hybrid runtimes are sample means.

The external graph corpus is used for the four R/P **input edge lists only**, never for old source code or old timing results. The cycle-rich graph inputs are regenerated directly in `rich_multilength.py`.

The complete results and SHA-256 graph hashes are in the final CSV files.
