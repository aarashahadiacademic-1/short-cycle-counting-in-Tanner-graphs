#!/usr/bin/env python3
"""Full validated 13 + 4 comparison; never copies old algorithm implementations."""
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import sys

P = Path(__file__).resolve().parent
SRC = Path(os.environ.get("REFERENCE_GRAPH_DIR", "/tmp/reference-tanner-graphs/graphs"))
cases = [
 ("A16c",6,2560),("A128c",6,20480),("A128r",6,176),
 ("B128c",6,4608),("C128c",6,204928),("C128r",6,1590),
 ("R1200",6,1564),("R2400",6,155),
 ("D16c",8,57680),("P1200",8,65),
 ("P1600",10,11),("Q410",10,40448),("Q412",12,308992)
]
multi = [("B16r",16,8),("B32r",32,8),("B64r",64,10),("B128r",128,10)]
cpu = min(os.sched_getaffinity(0))
os.sched_setaffinity(0, {cpu})
print("Pinned CPU:", cpu, flush=True)
subprocess.run([sys.executable, str(P/"generate_graphs.py")], check=True)
for src, binary in [("four_algorithms.cpp","counter-final"),
                    ("multilength.cpp","multilength-final")]:
 subprocess.run(["g++","-std=c++17","-O3","-DNDEBUG",str(P/src),
                 "-o",str(P/binary)],check=True)
outdir=P/"graphs"
outdir.mkdir(exist_ok=True)
# Reference R/P edge lists are input data only; no historical code or output is copied.
for name, _, _ in cases:
 if name.startswith(("R","P")):
  source=SRC/(name+".edges")
  if not source.exists(): raise RuntimeError("Missing exact R/P graph input: "+str(source))
def digest(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()
def sample(path):
 with path.open() as f:
  n,m,e=map(int,f.readline().split())
 return n,m,e
results=[]
for name,g,expected in cases:
 graph=(SRC if name.startswith(("R","P")) else outdir)/(name+".edges")
 n,m,e=sample(graph)
 if e!=n*(e//n) or e!=m*(e//m): raise RuntimeError("degree mismatch")
 hrep=30 if name in ("Q410","Q412") else 100
 output=subprocess.run([str(P/"counter-final"),str(graph),str(g),"7",str(hrep)],
                       check=True,text=True,capture_output=True,timeout=900)
 data=json.loads(output.stdout)
 if data["Ng"]!=expected: raise RuntimeError(f"{name}: computed {data['Ng']} != {expected}")
 results.append(dict(graph=name,n=n,dv=e//n,dc=e//m,g=g,T=g,
  Ng=data["Ng"],KB_ms=data["KB_ms"],IMPA_ms=data["IMPA_ms"],
  Exact_ms=data["Exact_ms"],Hybrid_ms=data["Hybrid_ms"],
  MARE_percent=data["MARE_percent"],hybrid_reps=hrep,
  sha256=digest(graph)))
 print("CHECKED",name,data,flush=True)
q=5;dv=3;dc=4
base=[(x*q+y,a*q+(y-a*x)%q) for x in range(dc) for y in range(q) for a in range(dv)]
long=[]
for name,z,T in multi:
 rng=random.Random(20261012+z)
 path=outdir/(name+".edges")
 with path.open("w") as f:
  f.write(f"{20*z} {15*z} {len(base)*z}\n")
  for u,w in base:
   perm=list(range(z))
   rng.shuffle(perm)
   for i,j in enumerate(perm):
    f.write(f"{u*z+i} {w*z+j}\n")
 data=json.loads(subprocess.run([str(P/"multilength-final"),str(path),"6",str(T),"7"],
                                check=True,capture_output=True,text=True,timeout=600).stdout)
 if data["n"]!=20*z or data["g"]!=6 or len(data["N"])!=(T-6)//2+1:
  raise RuntimeError(name+": malformed result")
 long.append(dict(graph=name,n=20*z,dv=3,dc=4,g=6,T=T,
                  counts=";".join(str(x) for x in data["N"]),
                  KB_ms=data["KB_ms"],IMPA_ms=data["IMPA_ms"],
                  Exact_ms=data["Exact_ms"],sha256=digest(path)))
 print("CHECKED",name,data,flush=True)
def write_csv(path,items):
 with path.open("w",newline="") as f:
  writer=csv.DictWriter(f,fieldnames=items[0].keys());writer.writeheader();writer.writerows(items)
write_csv(P/"FINAL_TABLE.csv",results)
write_csv(P/"FINAL_MULTILENGTH.csv",long)
model="unknown CPU"
try:
 model=next(x.split(":",1)[1].strip() for x in Path("/proc/cpuinfo").read_text().splitlines()
            if x.lower().startswith("model name"))
except (OSError,StopIteration): pass
compiler=subprocess.run(["g++","-dumpfullversion"],capture_output=True,text=True).stdout.strip()
fmt=lambda v:f"{v:.3f}"
lines=["# Final table: full four-algorithm single-core benchmark","",
 "## Girth only (T = g)","",
 "| Graph | (dv,dc) | g | n | N_g | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |",
 "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for x in results:
 vals=[x[k] for k in ("KB_ms","IMPA_ms","Exact_ms","Hybrid_ms")]
 best=min(vals)
 times=[("**"+fmt(t)+"**") if t==best else fmt(t) for t in vals]
 lines.append(f"| {x['graph']} | ({x['dv']},{x['dc']}) | {x['g']} | {x['n']} | {x['Ng']} | "+" | ".join(times)+f" | {x['MARE_percent']:.2f} |")
lines+=["","## Multiple cycle lengths (g = 6; (dv,dc) = (3,4))","",
 "| Graph | n | T | (N6,N8[,N10]) | KB (ms) | IMPA (ms) | Exact (ms) |",
 "|---|---:|---:|---|---:|---:|---:|"]
for x in long:
 vals=[x[k] for k in ("KB_ms","IMPA_ms","Exact_ms")]
 best=min(vals)
 times=[("**"+fmt(t)+"**") if t==best else fmt(t) for t in vals]
 lines.append(f"| {x['graph']} | {x['n']} | {x['T']} | ({x['counts'].replace(';',',')}) | "+" | ".join(times)+" |")
lines+=["","## Reproducibility","",
 f"* CPU: {model}; pinned logical CPU {cpu}; Linux {platform.release()}.",
 f"* Compiler: g++ {compiler}; single thread; -std=c++17 -O3 -DNDEBUG.",
 "* Graph generation and file loading excluded from timed regions.",
 "* Deterministic timings are seven-run medians. Hybrid timing is mean of 100 runs (30 for the two Q graphs).",
 "* All deterministic girth counts are checked against references; local Exact, KB and IMPA multi-length counts also agree with an independently implemented canonical simple-cycle DFS.",
 "* Hybrid exact and standalone Exact use the same root kernel with no extra advance after either branch wins.",
 "* The four random B-lifts use deterministic edge-permutations of the standard affine-incidence B base. These are synthetic benchmarks, not independently famous named LDPC codes.",
 "* Input R/P edges are read from the public graph corpus at https://github.com/aarashahadiacademic-1/tanner-cycle-counting and are not copied into this repository. No older executable, source code or timing result is imported.",
 "* Reproduce by running the GitHub Actions workflow 'Final benchmarks', or with REFERENCE_GRAPH_DIR pointed at a checkout of that graph corpus and python3 run_remaining.py.",
 ""]
(P/"FINAL_TABLE.md").write_text("\n".join(lines))
print("COMPLETE: 13 girth-only + 4 multiple-length cases",flush=True)
