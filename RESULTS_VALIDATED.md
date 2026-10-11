# Newly executed, independently computed cycle counts

2026-10-12. These are counts, **not** benchmarked comparison timings.
The original thirteen reference values were supplied by the author and used
only as equality tests against the freshly executed C++ girth counter.
No older measurements have been imported.

## Checked girth counts

| Instance | g | Computed N_g | Reference N_g | Match |
|---|---:|---:|---:|---|
| A16c | 6 | 2560 | 2560 | yes |
| A128c | 6 | 20480 | 20480 | yes |
| A128r | 6 | 176 | 176 | yes |
| B128c | 6 | 4608 | 4608 | yes |
| C128c | 6 | 204928 | 204928 | yes |
| C128r | 6 | 1590 | 1590 | yes |
| D16c | 8 | 57680 | 57680 | yes |
| Q410 | 10 | 40448 | 40448 | yes |
| Q412 | 12 | 308992 | 308992 | yes |

R1200, R2400, P1200, P1600 have not yet completed fresh
reproduction; no result for them is claimed.

## Four (3,4)-regular finite-affine-geometry lift examples

These are **new test cases**, not a claim that the four lifted graphs
are individually famous published LDPC benchmark codes. They are lifts of the
standard affine-incidence base B over F_5, with cyclic lift sizes
16, 32, 64, and 128. For the ordered base edge list, shift the first
base edge by 1 and leave all others unshifted.

| Instance | n | g | N6 | N8 | N10 |
|---|---:|---:|---:|---:|---:|
| B16c | 320 | 6 | 576 | 3328 | 9600 |
| B32c | 640 | 6 | 1152 | 6656 | 19200 |
| B64c | 1280 | 6 | 2304 | 13312 | 38400 |
| B128c | 2560 | 6 | 4608 | 26624 | 76800 |

The counts above were computed by a separately written canonical
simple-cycle DFS in src/fresh_multilength.cpp and not imported from
any prior timings table. It roots each cycle at its minimum variable
vertex and counts only one orientation, so NO further division is required.

## Outstanding work

The timing comparison Exact / KB / IMPA / Hybrid is **not measured**
here, and the requested optimized interleaved Hybrid has not yet been
implemented or validated. Do not use these counts as timing claims.
