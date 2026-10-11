#!/usr/bin/env python3
"""Prospective parameter scan: DO NOT publish timings until reproduced."""
import itertools,random,subprocess,os,json,pathlib,csv
P=pathlib.Path(__file__).resolve().parent
os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
out=P/"candidate_graphs";out.mkdir(exist_ok=True)
subprocess.run(["g++","-std=c++17","-O3","-DNDEBUG",str(P/"multilength.cpp"),"-o",str(P/"candidate-counter")],check=True)
families=[(3,3,3),(5,3,3),(5,3,4),(7,3,4),(7,3,6)]
Zs=[1,2,4,8,16,32,64]
data=[]
for q,dv,dc in families:
 n=dc*q;m=dv*q
 base=[(x*q+y,a*q+(y-a*x)%q) for x in range(dc) for y in range(q) for a in range(dv)]
 for lift in Zs:
  for mode in (["cyclic"] if lift==1 else ["cyclic","random"]):
   for T in ([8,10] if lift<=16 else [8]):
    name=f"F{q}_{dv}{dc}_{lift}{mode[0]}_T{T}"
    path=out/(name+".edges")
    rng=random.Random(20261012+10000*q+100*dv+dc+lift)
    with path.open("w") as f:
     f.write(f"{n*lift} {m*lift} {len(base)*lift}\n")
     for j,(u,w) in enumerate(base):
      perm=list(range(lift))
      if mode=="random":rng.shuffle(perm)
      elif j==0:perm=[(i+1)%lift for i in range(lift)]
      for i,k in enumerate(perm):f.write(f"{u*lift+i} {w*lift+k}\n")
    try:
     proc=subprocess.run([str(P/"candidate-counter"),str(path),"6",str(T),"3"],capture_output=True,text=True,timeout=22)
     if proc.returncode:raise RuntimeError(proc.stderr.strip()[-150:])
     x=json.loads(proc.stdout)
     if x["N"][0]<=0:continue
     row={"graph":name,"q":q,"dv":dv,"dc":dc,"lift":lift,"mode":mode,"n":n*lift,"g":6,"T":T,
          "counts":x["N"],"KB_ms":x["KB_ms"],"IMPA_ms":x["IMPA_ms"],"Exact_ms":x["Exact_ms"],
          "speed_vs_IMPA":x["IMPA_ms"]/max(x["Exact_ms"],1e-9)}
     data.append(row)
     print("CANDIDATE",json.dumps(row,separators=(",",":")),flush=True)
    except Exception as e: print("SKIP",name,str(e)[:150],flush=True)
data.sort(key=lambda a:a["speed_vs_IMPA"],reverse=True)
print("TOP",json.dumps(data[:12]),flush=True)
with (P/"SCAN_ONLY.json").open("w") as f:json.dump(data,f,indent=2)
