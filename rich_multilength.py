#!/usr/bin/env python3
"""Cycle-rich low-degree near-girth benchmarks, using unchanged multilength.cpp.
Replaces the low-cycle-count illustrative rows after full exact-count agreement.
"""
from pathlib import Path
import csv,hashlib,json,os,subprocess
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
G=P/"graphs";G.mkdir(exist_ok=True)
exe=P/"multilength-final"
if not exe.exists():raise RuntimeError("run_remaining.py must compile multilength.cpp first")
# The cyclic affine incidence lifts have a shift of +1 on the first base edge.
# No changes to any of the benchmarked algorithm implementations.
cases=[("B128c",5,3,4,128),("B256c",5,3,4,256),
       ("B512c",5,3,4,512),("A128c",7,3,6,128),("A256c",7,3,6,256)]
rows=[]
for name,q,dv,dc,z in cases:
 base=[(x*q+y,a*q+(y-a*x)%q) for x in range(dc) for y in range(q) for a in range(dv)]
 path=G/(name+".edges")
 with path.open("w") as f:
  f.write(f"{dc*q*z} {dv*q*z} {len(base)*z}\n")
  for edge,(u,w) in enumerate(base):
   for i in range(z):
    j=(i+1)%z if edge==0 else i
    f.write(f"{u*z+i} {w*z+j}\n")
 result=subprocess.run([str(exe),str(path),"6","8","7"],
                       capture_output=True,text=True,timeout=900,check=True)
 x=json.loads(result.stdout)
 if x["g"]!=6 or x["T"]!=8 or len(x["N"])!=2 or x["n"]!=dc*q*z:
  raise RuntimeError("Malformed benchmark "+name)
 if min(x["N"])<1000:raise RuntimeError(f"{name}: not cycle-rich enough {x['N']}")
 record={"graph":name,"n":x["n"],"dv":dv,"dc":dc,"g":6,"T":8,
  "counts":";".join(map(str,x["N"])),"KB_ms":x["KB_ms"],
  "IMPA_ms":x["IMPA_ms"],"Exact_ms":x["Exact_ms"],
  "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
 rows.append(record);print("VERIFIED_RICH",json.dumps(record),flush=True)

with (P/"FINAL_MULTILENGTH.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (P/"FINAL_TABLE.csv").open(newline="") as f:
 girth=list(csv.DictReader(f))

def emphasize(values):
 values=[float(v) for v in values];mn=min(values)
 return [r"\textbf{"+f"{v:.2f}"+"}" if v==mn else f"{v:.2f}" for v in values]
head=[
r"\begin{table*}[t]",
r"\centering",
r"\caption{Runtime comparison for girth-only and multiple-cycle-length counting.",
r"Times are in milliseconds.}",
r"\label{tab:combined-exp}",
r"\footnotesize",
r"\setlength{\tabcolsep}{5pt}",
r"\begin{tabular}{lccrrlrrrrl}\hline",
r"Graph & $(d_v,d_c)$ & $g$ & $n$ & & Count(s) &",
r"KB~\cite{karimi2013} & IMPA~\cite{li2015} & Exact & Hybrid & MARE (\%)\\\hline",
r"\multicolumn{5}{l}{\emph{Girth only}} & $N_g$ & \multicolumn{5}{c}{}\\[1pt]\hline",
r"\noalign{\vskip 2pt}"]
for r in girth:
 vals=emphasize(r[k] for k in ("KB_ms","IMPA_ms","Exact_ms","Hybrid_ms"))
 mare=float(r["MARE_percent"])
 head.append(f"{r['graph']} & $({r['dv']},{r['dc']})$ & {r['g']} & {r['n']} & & {r['Ng']} & "+" & ".join(vals)+(" & 0 " if mare==0 else f" & {mare:.2f} ")+r"\\")
head += [
r"\hline",
r"\multicolumn{4}{l}{\emph{Multiple cycle lengths}} & $T$ &",
r"$(N_g,\ldots,N_T)$ & \multicolumn{5}{c}{}\\[1pt]\hline",
r"\noalign{\vskip 2pt}"]
for r in rows:
 vals=emphasize(r[k] for k in ("KB_ms","IMPA_ms","Exact_ms"))
 head.append(f"{r['graph']} & $({r['dv']},{r['dc']})$ & 6 & {r['n']} & 8 & $({r['counts'].replace(';',',')})$ & "+" & ".join(vals)+r" & & \\")
head += [r"\hline",r"\end{tabular}",r"\end{table*}"]
(P/"FINAL_TABLE.tex").write_text("\n".join(head)+"\n")
md=["# Final tables: girth and cycle-rich near-girth counting","","## Girth-only (T=g)",
"| Graph | (dv,dc) | g | n | Ng | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |",
"|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for r in girth:
 vals=[float(r[k]) for k in ("KB_ms","IMPA_ms","Exact_ms","Hybrid_ms")]
 md.append("| "+r["graph"]+" | ("+r["dv"]+","+r["dc"]+") | "+r["g"]+" | "+r["n"]+" | "+r["Ng"]+" | "+
           " | ".join(("**"+f"{v:.3f}"+"**") if v==min(vals) else f"{v:.3f}" for v in vals)+
           f" | {float(r['MARE_percent']):.2f} |")
md+=["","## Multiple cycle lengths: low degrees, large cycle counts (g=6,T=8)","",
"| Graph | (dv,dc) | n | (N6,N8) | KB (ms) | IMPA (ms) | Exact (ms) |",
"|---|---|---:|---|---:|---:|---:|"]
for r in rows:
 vals=[float(r[k]) for k in ("KB_ms","IMPA_ms","Exact_ms")]
 md.append(f"| {r['graph']} | ({r['dv']},{r['dc']}) | {r['n']} | ({r['counts'].replace(';',',')}) | "+
           " | ".join(("**"+f"{v:.3f}"+"**") if v==min(vals) else f"{v:.3f}" for v in vals)+" |")
md+=["","## Reproduction","","* All measurements are from one pinned CPU per complete run, g++ C++17 -O3 -DNDEBUG.",
"* Seven-run medians for deterministic counters; hybrid means from the girth-only benchmark.",
"* The girth-only Exact and Hybrid share an optimized root kernel.",
"* Each multiple-length Exact / KB / IMPA count vector agrees with the independent canonical simple-cycle DFS in multilength.cpp.",
"* Graphs are deterministic cyclic lifts of standard affine-incidence constructions, not standardized LDPC codes.",
"* Their full edge-list generation and benchmark commands are in rich_multilength.py.",
"* Results are empirical timing comparisons, not a claim of uniform algorithmic dominance."]
(P/"FINAL_TABLE.md").write_text("\n".join(md)+"\n")
print("SUCCESS: final table synchronized with 17 girth rows and five rich-cycle low-degree rows",flush=True)
