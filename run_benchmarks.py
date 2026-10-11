#!/usr/bin/env python3
"""Rebuild nine graph instances and remeasure four algorithms on one CPU."""
import csv
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
CASES = [("A16c", 6), ("A128c", 6), ("A128r", 6),
         ("B128c", 6), ("C128c", 6), ("C128r", 6),
         ("D16c", 8), ("Q410", 10), ("Q412", 12)]
EXPECTED = [2560, 20480, 176, 4608, 204928, 1590,
            57680, 40448, 308992]

subprocess.run([sys.executable, str(HERE/"generate_graphs.py")], check=True)
subprocess.run(["g++", "-std=c++17", "-O3", "-DNDEBUG",
                str(HERE/"four_algorithms.cpp"), "-o",
                str(HERE/"benchmark")], check=True)
rows = []
for (name, g), correct in zip(CASES, EXPECTED):
    repetitions = 30 if name.startswith("Q") else 100
    output = subprocess.run(
        ["taskset", "-c", "0", str(HERE/"benchmark"),
         str(HERE/"graphs"/(name+".edges")), str(g), "7",
         str(repetitions)],
        check=True, text=True, capture_output=True).stdout
    record = json.loads(output)
    if record["Ng"] != correct or record["g"] != g:
        raise RuntimeError("Count mismatch for " + name)
    rows.append({"graph": name, **record})
    print(name, output.strip(), flush=True)
with (HERE/"reproduced_results.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("Saved reproduced_results.csv")
