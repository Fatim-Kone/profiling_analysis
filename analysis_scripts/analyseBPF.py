import numpy as np
import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict

jobs_n = [1 2 4 6]
mode = ["h", "l"]
prbs = [50, 100, 200, 250]
iters = [2, 6, 4, 8, 10]
tracefiles = ["cqi_trace_Ujwal_01012023_1.txt", "cqi_trace_Ujwal_01012023_2.txt",  "cqi_trace_Ujwal_triangular_01062023_1.txt", "out_mac_realistic_spin_cqi.txt", "cqi_car_20mph_3min.txt", "random_1.txt"]
mcs = [0, 4, 5, 10, 11, 19, 20, 27]
concurs = [2, 4, 8, 12, 0]
plt.style.use('grayscale')

parsed_dist = defaultdict()
parsed_shared = defaultdict()

def parse_pid(line):
    match = re.search(r'pid=(\w+)', line)
    if match:
        return int(match.group(1))
    return None

def parse_worker(line):
    match = re.search(r'worker=([^\s]+)', line)
    if match:
        return match.group(1)
    return None
    
def parse_func(line):
    line = re.sub(r'\[unknown\];', '', line)
    line = re.sub(r'\[unknown\]', '', line)
    line = line.replace("(anonymous namespace)", "")
    line = line.replace("non-virtual thunk to ", "")
    line = re.sub(r'void ', '', line)
    match = re.search(r'func=([^(<]+)', line)
    if match:
        return match.group(1)
    return None

def parse_count(line):
    match = re.search(r'count=(\d+\.?\d*)', line)
    if match:
        return float(match.group(1))
    return None

def parse_time(line):
    match = re.search(r't=(\d+\.?\d*)us', line)
    if match:
        return float(match.group(1))
    return None

def parse_logs(onLog, offLog, experiment, load, dist):
    parsed_logs = defaultdict(lambda: defaultdict(int))
    with open(onLog, 'r') as f:
        for line in f:
            if "Total Samples" in line:
                line = line.strip()
                entry = line.split()
                parsed_logs["onCPU"]["totalSamples"] = int(entry[2])
            else:
                line = line.strip()
                worker = parse_worker(line)
                pid = parse_pid(line)
                func = parse_func(line)
                count = parse_count(line)
                parsed_logs["onCPU"][(pid, func)] += count 
            
    with open(offLog, 'r') as f:
        for line in f:
            line = line.strip()
            seperate = line.split()
            worker = parse_worker(line)
            pid = parse_pid(line)
            func = parse_func(line)
            t = parse_time(line)
            if func != None:
                parsed_logs["offCPU"][(worker, pid, func)] = t 

    if dist == "shared":
        parsed_shared[experiment] = parsed_logs
    else:
        parsed_dist[experiment] = parsed_logs
    
def topOffCPUFunc(logs, load, dist):
    top = defaultdict(lambda: defaultdict(float))
    for experiment, entries in logs.items():
        offCPU = entries["offCPU"]
        for (worker, pid, func), time in offCPU.items():
            if "main_pool" in worker:
                top[experiment][func] += time
    
    for experiment, entries in top.items():
        m, j = experiment.split("w")
        j = int(j.split('_')[0])
        mode = "Software"
        if m == "h":
            mode = "Hardware"
        print(f"\n{load} Load {dist} Cores: {j} {mode} DU{'s' if int(j) > 1 else ''}")
        sorted_times = sorted(entries.items(), key=lambda x: x[1], reverse=True)

        for i, (func, time) in enumerate(sorted_times[:30], 1):
            print(f"{i}. {func} - {time/int(j):.2f} s")

def topOnCPUFunc(logs, load, dist):
    top = defaultdict(lambda: defaultdict(float))
    for experiment, entries in logs.items():
        onCPU = entries["onCPU"]
        totalSamples = entries["onCPU"].pop("totalSamples", None)
        top[experiment]["totalSamples"] = totalSamples
        for (pid, func), count in onCPU.items():
            top[experiment][func] += count
    
    for experiment, entries in top.items():
        totalSample = entries.pop("totalSamples", None)
        m, j = experiment.split("w")
        j = int(j.split('_')[0])
        mode = "Software"
        if m == "h":
            mode = "Hardware"
        print(f"\n{load} Load {'Dist' if '_s' not in experiment else 'Shared'} Cores: {j} {mode} DU{'s' if int(j) > 1 else ''}")
        sorted_times = sorted(entries.items(), key=lambda x: x[1], reverse=True)
        
        for i, (func, count) in enumerate(sorted_times, 1):
            print(f"{i}. {func} - CPU Usage {(count/totalSamples * 100):.3f}%, CPU Time {(count/99):.3f}s")

def logs(dir, vars):
    for job in jobs_n:
        for m in vars:
            parse_logs(f"{dir}sw{job}_{m}_onCPU.log", f"{dir}sw{job}_{m}_offCPU.log", f"sw{job}_{m}", m, "dist")
            parse_logs(f"{dir}hw{job}_{m}_onCPU.log", f"{dir}hw{job}_{m}_offCPU.log", f"hw{job}_{m}", m, "dist")
            if job > 1:
                parse_logs(f"{dir}sw{job}_{m}_onCPU_s.log", f"{dir}sw{job}_{m}_offCPU_s.log", f"sw{job}_{m}_s", m, "shared")
                parse_logs(f"{dir}hw{job}_{m}_onCPU_s.log", f"{dir}hw{job}_{m}_offCPU_s.log", f"hw{job}_{m}_s", m, "shared")


logs("/home/fatim/fatim/new_logs/", mode)
topOffCPUFunc(parsed_shared, "High", "Dist")
topOnCPUFunc(parsed_dist, "High", "Dist")