#!/usr/bin/env python3
"""Append 4 independently validated near-girth measurements."""
from pathlib import Path
import csv,hashlib,json,os,random,subprocess
P=Path(__file__).resolve().parent
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
cases=[("F5-32r",5,3,4,32,(43,231)),("F5-64r",5,3,4,64,(32,266)),
       ("F7-64r",7,3,4,64,(31,211)),("G7-64r",7,3,6,64,(168,1653))]
folder=P/"graphs";folder.mkdir(exist_ok=True)
binary=P/"multilength-final"
if not binary.is_file():raise RuntimeError("run_remaining.py must run first")
extra=[]
for name,q,dv,dc,z,expected in cases:
 base=[(x*q+y,a*q+(y-a*x)%q) for x in range(dc) for y in range(q) for a in range(dv)]
 rng=random.Random(20261012+10000*q+100*dv+dc+z)
 graph=folder/(name+".edges")
 with graph.open("w") as f:
  f.write(f"{dc*q*z} {dv*q*z} {len(base)*z}\n")
  for u,w in base:
   perm=list(range(z));rng.shuffle(perm)
   for i,j in enumerate(perm):f.write(f"{u*z+i} {w*z+j}\n")
 p=subprocess.run([str(binary),str(graph),"6","8","7"],
                  capture_output=True,text=True,check=True,timeout=300)
 x=json.loads(p.stdout)
 if tuple(x["N"])!=expected or x["n"]!=dc*q*z:
  raise RuntimeError(f"{name}: validation mismatch {x}")
 record=dict(graph=name,n=x["n"],dv=dv,dc=dc,g=6,T=8,
   counts=";".join(map(str,x["N"])),KB_ms=x["KB_ms"],
   IMPA_ms=x["IMPA_ms"],Exact_ms=x["Exact_ms"],
   sha256=hashlib.sha256(graph.read_bytes()).hexdigest())
 extra.append(record);print("FINAL_CHECKED",json.dumps(record),flush=True)
file=P/"FINAL_MULTILENGTH.csv"
with file.open(newline="") as f:rows=list(csv.DictReader(f))
names={r["graph"] for r in extra}
rows=[r for r in rows if r["graph"] not in names]+extra
with file.open("w",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]))
 writer.writeheader();writer.writerows(rows)
added=[]
for x in extra:
 vals=[float(x[k]) for k in ("KB_ms","IMPA_ms","Exact_ms")]
 win=min(vals);fm=[("**"+f"{v:.3f}"+"**") if v==win else f"{v:.3f}" for v in vals]
 added.append(f"| {x['graph']} | {x['n']} | 8 | ({x['counts'].replace(';',',')}) | "+" | ".join(fm)+" |")
file=P/"FINAL_TABLE.md";md=file.read_text()
a,b=md.split("## Reproducibility",1)
a="\n".join(line for line in a.split("\n") if not any(line.startswith("| "+name+" |") for name in names))
note=("These four prospective affine-incidence random lifts were selected after "
 "a parameter scan. Exact beats KB on these cases, but not IMPA. "
 "Their complete reproducible construction appears in append_multi.py; "
 "the independent canonical simple-cycle DFS checks all counts.\n\n")
file.write_text(a.rstrip()+"\n"+"\n".join(added)+"\n\n## Reproducibility\n\n"+note+b.lstrip("\n"))
file=P/"FINAL_TABLE.tex";tex=file.read_text()
tex="\n".join(line for line in tex.split("\n") if not any(line.startswith(name+" &") for name in names))
if "\\hline\n\\end{tabular}" not in tex:raise RuntimeError("TeX layout unexpected")
texrows=[]
for x in extra:
 vals=[float(x[k]) for k in ("KB_ms","IMPA_ms","Exact_ms")]
 fm=[(r"\textbf{"+f"{v:.2f}"+"}") if v==min(vals) else f"{v:.2f}" for v in vals]
 counts=x["counts"].replace(";",",")
 texrows.append(f"{x['graph']} & $({x['dv']},{x['dc']})$ & 6 & {x['n']} & 8 & $({counts})$ & "+" & ".join(fm)+r" & & \\")
tex=tex.replace("\\hline\n\\end{tabular}","\n".join(texrows)+"\n\\hline\n\\end{tabular}")
file.write_text(tex)
print("FINISHED: 17 girth rows and 8 multiple-length rows",flush=True)
