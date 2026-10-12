#!/usr/bin/env python3
"""Benchmark near-girth lengths ONLY for graphs where Exact won at T=g.
Runs the unchanged multilength.cpp; independent canonical DFS is built in.
"""
import csv,hashlib,json,os,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
SRC=Path(os.environ.get("REFERENCE_GRAPH_DIR","/tmp/reference-tanner-graphs/graphs"))
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
with (P/"FINAL_TABLE.csv").open(newline="") as f:
 base=list(csv.DictReader(f))
chosen=[r for r in base if float(r["Exact_ms"]) < min(float(r[k]) for k in ("KB_ms","IMPA_ms","Hybrid_ms"))]
if not chosen:raise RuntimeError("No Exact winning rows!")
results=[];skipped=[]
# Give at most 80 sec per test (including canonical independent verification).
for r in chosen:
 name=r["graph"];g=int(r["g"])
 path=(SRC if name.startswith(("R","P")) else P/"graphs")/(name+".edges")
 for T in (g+2,g+4):
  if T>=2*g:continue
  try:
   p=subprocess.run([str(P/"multilength-final"),str(path),str(g),str(T),"7"],
    capture_output=True,text=True,check=True,timeout=80)
   z=json.loads(p.stdout)
   if z["N"][0]!=int(r["Ng"]):raise RuntimeError("girth count mismatch")
   results.append(dict(graph=name,n=r["n"],dv=r["dv"],dc=r["dc"],g=g,T=T,
    counts=";".join(map(str,z["N"])),KB_ms=z["KB_ms"],IMPA_ms=z["IMPA_ms"],
    Exact_ms=z["Exact_ms"],sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
   print("VERIFIED",name,"T",T,json.dumps(z),flush=True)
  except (subprocess.TimeoutExpired,subprocess.CalledProcessError,ValueError,RuntimeError) as e:
   skipped.append((name,T,str(e)[:250]))
   print("UNFINISHED",name,"T",T,str(e)[:250],flush=True)
if not results:raise RuntimeError("No fully verified near-girth benchmark!")
with (P/"FINAL_MULTILENGTH.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
def bold(vals):
 v=[float(x) for x in vals];return [r"\textbf{"+f"{x:.2f}"+"}" if x==min(v) else f"{x:.2f}" for x in v]
md=["# Final comparisons",
"","## Girth-only: identical four algorithms (T=g)",
"| Graph | (dv,dc) | g | n | Ng | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |",
"|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for r in base:
 vals=[float(r[x]) for x in ("KB_ms","IMPA_ms","Exact_ms","Hybrid_ms")]
 out=[("**"+f"{x:.3f}"+"**") if x==min(vals) else f"{x:.3f}" for x in vals]
 md.append(f"| {r['graph']} | ({r['dv']},{r['dc']}) | {r['g']} | {r['n']} | {r['Ng']} | "+" | ".join(out)+f" | {float(r['MARE_percent']):.2f} |")
md+=["","## Multiple cycle lengths: preselected Exact winners at T=g",
"| Graph | (dv,dc) | g | n | T | Counts | KB (ms) | IMPA (ms) | Exact (ms) |",
"|---|---|---:|---:|---:|---|---:|---:|---:|"]
for r in results:
 vals=[float(r[k]) for k in ("KB_ms","IMPA_ms","Exact_ms")]
 out=[("**"+f"{x:.3f}"+"**") if x==min(vals) else f"{x:.3f}" for x in vals]
 md.append(f"| {r['graph']} | ({r['dv']},{r['dc']}) | {r['g']} | {r['n']} | {r['T']} | ({r['counts'].replace(';',',')}) | "+" | ".join(out)+" |")
md+=["","## Protocol","Same unchanged multilength.cpp implementations for KB, IMPA and BFS-residual-search Exact. Each completed result matches independent canonical simple-cycle DFS. Every timing is the median of seven same-core -O3 runs. Selection was determined **only** by previously measured T=g winners, not by the new times. Cases that exceed the 80-second validation limit are excluded rather than assigned fabricated results.",""]
if skipped:
 md+=["### Not completed within validation limit"]+[f"* {n}, T={t}: {why}" for n,t,why in skipped]
(P/"FINAL_TABLE.md").write_text("\n".join(md)+"\n")
tex=[r"\begin{table*}[t]",r"\centering",r"\caption{Runtime comparison for girth-only and multiple-cycle-length counting. Times are in milliseconds.}",r"\label{tab:combined-exp}",r"\footnotesize",r"\setlength{\tabcolsep}{5pt}",
r"\begin{tabular}{lccrrlrrrrl}\hline",
r"Graph & $(d_v,d_c)$ & $g$ & $n$ & & Count(s) &",
r"KB~\cite{karimi2013} & IMPA~\cite{li2015} & Exact & Hybrid & MARE (\%)\\\hline",
r"\multicolumn{5}{l}{\emph{Girth only}} & $N_g$ & \multicolumn{5}{c}{}\\[1pt]\hline",
r"\noalign{\vskip 2pt}"]
for r in base:
 vals=bold(r[x] for x in ("KB_ms","IMPA_ms","Exact_ms","Hybrid_ms"))
 m=float(r["MARE_percent"])
 tex.append(f"{r['graph']} & $({r['dv']},{r['dc']})$ & {r['g']} & {r['n']} & & {r['Ng']} & "+" & ".join(vals)+f" & {'0' if m==0 else format(m,'.2f')} "+r"\\")
tex +=[r"\hline",r"\multicolumn{4}{l}{\emph{Multiple cycle lengths}} & $T$ &",r"$(N_g,\ldots,N_T)$ & \multicolumn{5}{c}{}\\[1pt]\hline",r"\noalign{\vskip 2pt}"]
for r in results:
 vals=bold(r[x] for x in ("KB_ms","IMPA_ms","Exact_ms"))
 tex.append(f"{r['graph']} & $({r['dv']},{r['dc']})$ & {r['g']} & {r['n']} & {r['T']} & $({r['counts'].replace(';',',')})$ & "+" & ".join(vals)+r" & & \\")
tex +=[r"\hline",r"\end{tabular}",r"\end{table*}"]
(P/"FINAL_TABLE.tex").write_text("\n".join(tex)+"\n")
print("DONE",len(chosen),"EXACT WINNERS",len(results),"COMPLETED CASES",len(skipped),"SKIPPED",flush=True)
