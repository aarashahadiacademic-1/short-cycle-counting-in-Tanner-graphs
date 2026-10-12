# Cycle counting in Tanner graphs

Reproducible exact and hybrid cycle-counting benchmarks for LDPC Tanner graphs.

- [Final LaTeX table](FINAL_TABLE.tex)
- [Girth-only timings (CSV)](FINAL_TABLE.csv)
- [Multiple-length timings (CSV)](FINAL_MULTILENGTH.csv)
- [Complete results and methods](FINAL_TABLE.md)

## Scope

**Girth-only:** 17 benchmark Tanner graphs; KB, IMPA, Exact and Hybrid.

**Multiple lengths:** the preselected graphs for which Exact was fastest in an earlier `T=g` table, evaluated at `T=g+2` and, where feasible, `T=g+4`. The fixed cohort includes A16c, A128c, A128r, B128c, C128r, R1200, R2400, P1200, P1600 and Q410. Earlier measured rankings for borderline graphs can change slightly across runs. In particular, this is *not* a claim that Exact is the fastest at the longer lengths.

## Implementation and reproduction

The algorithm implementations are unchanged:

- `four_algorithms.cpp`: KB, IMPA, Exact and Hybrid for girth-only counting.
- `multilength.cpp`: KB, IMPA and BFS/residual-search Exact for all even cycle lengths up to `T`; verifies every reported count against independent canonical simple-cycle DFS.
- `generate_graphs.py`: deterministic graph construction.
- `run_remaining.py`: baseline 17-graph benchmark on a pinned CPU.
- `exact_winners_multilength.py`: fixed selected graph comparisons at `g+2` and `g+4`, using the same compiled algorithms.
- `.github/workflows/final-benchmarks.yml`: compiles and reruns all comparisons in GitHub Actions.

Compiler: `g++ -std=c++17 -O3 -DNDEBUG`, single thread. Deterministic runtimes are medians of 7 executions. Graph loading and construction are untimed. For unusually expensive independent checks a per-test 80-second limit applies; unfinished rows are explicitly omitted rather than assigned invented times.

Four R/P graph *input files* are retrieved from the separate reference graph corpus. No old algorithm implementations or old timing results are imported.
