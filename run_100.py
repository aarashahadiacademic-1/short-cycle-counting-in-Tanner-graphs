#!/usr/bin/env python3
"""Full 17 graph four-algorithm one-hundred-trial mean benchmark.
Requires public R/P input edge lists in REFERENCE_GRAPH_DIR.
Only writes final tables after ALL 17 graphs pass independent exact-count checks.
"""
from pathlib import Path
import csv,hashlib,json,os,platform,subprocess,sys
P=Path(__file__).resolve().parent
SRC=Path(os.environ.get("REFERENCE_GRAPH_DIR","/tmp/reference-tanner-graphs/graphs"))
cpu=min(os.sched_getaffinity(0));os.sched_setaffinity(0,{cpu})
print("PINNED_CPU",cpu,flush=True)
subprocess.run([sys.executable,str(P/"generate_graphs.py")],check=True)
exe=P/"counter-100"
subprocess.run(["g++","-std=c++17","-O3","-DNDEBUG",str(P/"benchmark_100.cpp"),"-o",str(exe)],check=True)
with (P/"FINAL_TABLE.csv").open(newline="") as f:previous=list(csv.DictReader(f))
if len(previous)!=17:raise RuntimeError("Expected the fixed 17 graph list")
results=[]
for old in previous:
 name=old["graph"]
 p=(SRC if name.startswith(("R","P")) else P/"graphs")/(name+".edges")
 if not p.exists():raise RuntimeError("Missing graph input: "+str(p))
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if old["sha256"]!=h:raise RuntimeError("Graph SHA changed: "+name)
 output=subprocess.run([str(exe),str(p),old["g"],old["Ng"],"100"],
                       text=True,capture_output=True,timeout=1200,check=True)
 x=json.loads(output.stdout)
 if x["n"]!=int(old["n"]) or x["Ng"]!=int(old["Ng"]):raise RuntimeError("count or n mismatch")
 updated={k:old[k] for k in ("graph","n","dv","dc","g","T","Ng")}
 for method in ("KB","IMPA","Exact","Hybrid"):
  updated[method+"_ms"]=x[method+"_ms"]
 updated["MARE_percent"]=x["MARE_percent"]
 updated["hybrid_reps"]=100;updated["sha256"]=h
 for method in ("KB","IMPA","Exact","Hybrid"):
  updated[method+"_std_ms"]=x[method+"_std_ms"]
  updated[method+"_median_ms"]=x[method+"_median_ms"]
 updated["deterministic_reps"]=100
 updated["random_wins"]=x["random_wins"]
 results.append(updated)
 scores={m:updated[m+"_ms"] for m in ("KB","IMPA","Exact","Hybrid")}
 winner=min(scores,key=scores.get)
 print("VERIFIED_100",name,"winner",winner,"means",json.dumps(scores),"std",
       json.dumps({m:updated[m+"_std_ms"] for m in scores}),flush=True)

# No table mutations before this point. Preserve previously verified multi-length results.
with (P/"FINAL_MULTILENGTH.csv").open(newline="") as f:multi=list(csv.DictReader(f))
if not multi:raise RuntimeError("Expected verified multi-length results")
def fmt(x):return f"{float(x):.2f}"
def bold_mean(record,methods):
 values={m:float(record[m+"_ms"]) for m in methods}
 best=min(values,key=values.get)
 return ["\\textbf{"+fmt(values[m])+"}" if m==best else fmt(values[m]) for m in methods]
tex=[
r"\begin{table*}[t]",r"\centering",
r"\caption{Runtime comparison for girth-only and multiple-cycle-length counting. Girth-only times are means of 100 runs; multiple-length times are medians of seven runs. Times are in milliseconds.}",
r"\label{tab:combined-exp}",r"\footnotesize",r"\setlength{\tabcolsep}{5pt}",
r"\begin{tabular}{lccrrlrrrrl}\hline",
r"Graph & $(d_v,d_c)$ & $g$ & $n$ & & Count(s) &",
r"KB~\cite{karimi2013} & IMPA~\cite{li2015} & Exact & Hybrid & MARE (\%)\\\hline",
r"\multicolumn{5}{l}{\emph{Girth only}} & $N_g$ & \multicolumn{5}{c}{}\\[1pt]\hline",
r"\noalign{\vskip 2pt}"
]
methods=("KB","IMPA","Exact","Hybrid")
for x in results:
 v=bold_mean(x,methods)
 mare="0" if float(x["MARE_percent"])==0 else fmt(x["MARE_percent"])
 tex.append(f"{x['graph']} & $({x['dv']},{x['dc']})$ & {x['g']} & {x['n']} & & {x['Ng']} & "+
            " & ".join(v)+f" & {mare} "+r"\\")
tex += [r"\hline",r"\multicolumn{4}{l}{\emph{Multiple cycle lengths}} & $T$ &",
        r"$(N_g,\ldots,N_T)$ & \multicolumn{5}{c}{}\\[1pt]\hline",r"\noalign{\vskip 2pt}"]
for x in multi:
 v=bold_mean(x,("KB","IMPA","Exact"))
 tex.append(f"{x['graph']} & $({x['dv']},{x['dc']})$ & {x['g']} & {x['n']} & {x['T']} & $({x['counts'].replace(';',',')})$ & "+
            " & ".join(v)+r" & & \\")
tex += [r"\hline",r"\end{tabular}",r"\end{table*}"]

lines=["# Final timing tables","",
"## Girth-only: all four algorithms, means of 100 interleaved runs","",
"| Graph | (dv,dc) | g | n | Ng | KB (ms) | IMPA (ms) | Exact (ms) | Hybrid (ms) | MARE (%) |",
"|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
wins={m:0 for m in methods}
for x in results:
 v=[float(x[m+"_ms"]) for m in methods]
 winner=methods[v.index(min(v))];wins[winner]+=1
 cells=[("**"+fmt(x[m+"_ms"])+"**") if m==winner else fmt(x[m+"_ms"]) for m in methods]
 lines.append(f"| {x['graph']} | ({x['dv']},{x['dc']}) | {x['g']} | {x['n']} | {x['Ng']} | "+" | ".join(cells)+f" | {fmt(x['MARE_percent'])} |")
lines+=["",f"**Winners (out of 17):** KB {wins['KB']}; IMPA {wins['IMPA']}; Exact {wins['Exact']}; Hybrid {wins['Hybrid']}.",
"","### Across-run standard deviations (ms)","",
"| Graph | KB SD | IMPA SD | Exact SD | Hybrid SD |",
"|---|---:|---:|---:|---:|"]
for x in results:
 lines.append(f"| {x['graph']} | "+" | ".join(fmt(x[m+"_std_ms"]) for m in methods)+" |")
lines+=["","## Multiple cycle lengths (existing verified results: medians of seven runs)","",
"| Graph | g | T | Counts | KB (ms) | IMPA (ms) | Exact (ms) |",
"|---|---:|---:|---|---:|---:|---:|"]
for x in multi:
 v=[float(x[m+"_ms"]) for m in ("KB","IMPA","Exact")]
 cells=[("**"+fmt(x[m+"_ms"])+"**") if y==min(v) else fmt(x[m+"_ms"]) for y in v]
 lines.append(f"| {x['graph']} | {x['g']} | {x['T']} | ({x['counts'].replace(';',',')}) | "+" | ".join(cells)+" |")
lines+=["","## Reproducibility and interpretation","",
f"* CPU: {next((s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.lower().startswith('model name')),'unknown')}; pinned logical CPU {cpu}.",
"* C++17 -O3 -DNDEBUG, one CPU, 100 randomized-order paired blocks for all four algorithms.",
"* All 1700 KB / IMPA / Exact counts match the reference per algorithm; 100 Hybrid estimates per graph with r=100.",
"* Timing values in the upper half are arithmetic means, not medians. Standard deviations and medians are in FINAL_TABLE.csv.",
"* Lower half retains earlier verified 7-run medians; it was NOT remeasured under the 100-run protocol.",
"* Input graph SHA-256 checks and a fixed set of 17 graphs prevent silent benchmark changes.",
"* The benchmark uses exactly the current four_algorithms.cpp, included in benchmark_100.cpp.",
""]
# Atomic update after all validation
def atomic_write(path,text):
 tmp=path.with_name(path.name+".new")
 tmp.write_text(text)
 tmp.replace(path)
import io
f=io.StringIO();w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
atomic_write(P/"FINAL_TABLE.csv",f.getvalue())
atomic_write(P/"FINAL_TABLE.tex","\n".join(tex)+"\n")
atomic_write(P/"FINAL_TABLE.md","\n".join(lines)+"\n")
print("COMPLETE",len(results),"100-block graphs, winner counts",wins,flush=True)
