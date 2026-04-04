import numpy as np
import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

dir_lt = "/home/fatim/fatim/loadtesting_logs/"
dir_old = "/home/fatim/fatim/old_logs/"
dir_no = "/home/fatim/fatim/no_logs/"

dirs = [dir_lt, dir_old, dir_no]

pidstats_keys = [("usr", 3), ("sys", 4), ("wait", 6), ("cpu", 7), ("mem", 13), ("cswch/s", 14), ("nvcswch/s", 15)]
jobs_n = [1,2]
dus = [1,2]
plt.style.use('grayscale')
mode = ["shared", "dist"]

parsed_power = defaultdict(lambda: defaultdict())
parsed_cpu = defaultdict()
parsed_cpu["cu_h"] = defaultdict()
parsed_cpu["cu_l"] = defaultdict()
parsed_cpu_power = defaultdict(lambda: defaultdict())

def percent_increase(compare, baseline):
        compare = np.array(compare)
        baseline = np.array(baseline)
        return np.where(baseline == 0, 0, (compare - baseline) / baseline * 100)

def parse_log(log_file, job):
    with open(log_file, 'r') as f:
            x = defaultdict(lambda: defaultdict(list))
            i = 0 
            for line in f:
                gnb = i % job
                line = line.strip()
                split = line.split()
                for k,v in pidstats_keys:
                    x[gnb][k].append(float(split[v]))
                i += 1
            if "_h" in log_file[23:-8]:
                parsed_cpu["cu_h"][log_file] = {gnb: {k: (np.round(np.median(v), decimals=2), np.round(np.std(v), decimals=2)) for k,v in metrics.items()} for gnb, metrics in x.items()}
            else:    
                parsed_cpu["cu_l"][log_file] = {gnb: {k: (np.round(np.median(v), decimals=2), np.round(np.std(v), decimals=2)) for k,v in metrics.items()} for gnb, metrics in x.items()}

def parse_metrics(metric_list):
    core, sys, usr = [], [], []
    for c, s, u in metric_list:
        core.append(c)
        sys.append(s)
        usr.append(u)
    return core, sys, usr

def get_metrics(directory):
    metrics = defaultdict()
    with open(f"{directory}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "_h" in k:
                metrics[k] = entry["metrics_cell"]

    with open(f"{directory}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "_h" in k:
                metrics[k] = entry["metrics_cell"]
    return metrics

for dir in dirs:
    for job in jobs_n:
        parse_log(f"{dir}sw{job}_h_cpu.log", job)
        parse_log(f"{dir}hw{job}_h_cpu.log", job)
        if job > 1:
            parse_log(f"{dir}sw{job}_h_cpu_s.log", job)
            parse_log(f"{dir}hw{job}_h_cpu_s.log", job)
            sw_data = np.genfromtxt(f"{dir}sw{job}_h_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{job}_h_energy.csv", delimiter=',')
            sw_data = sw_data[~np.isnan(sw_data)]
            hw_data = hw_data[~np.isnan(hw_data)]
            parsed_cpu_power["dist"][f"{dir}sw{job}"] = np.median(sw_data)
            parsed_cpu_power["dist"][f"{dir}hw{job}"] = np.median(hw_data)
            sw_data_s = np.genfromtxt(f"{dir}sw{job}_h_energy_s.csv", delimiter=',')
            hw_data_s = np.genfromtxt(f"{dir}hw{job}_h_energy_s.csv", delimiter=',')
            sw_data_s = sw_data_s[~np.isnan(sw_data_s)]
            hw_data_s = hw_data_s[~np.isnan(hw_data_s)]
            parsed_cpu_power["shared"][f"{dir}sw{job}"] = np.median(sw_data_s)
            parsed_cpu_power["shared"][f"{dir}hw{job}"] = np.median(hw_data_s)
        if job > 2:
            sw_data = np.genfromtxt(f"{dir}sw{job}_h_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{job}_h_power.csv", delimiter=',')
            parsed_power["s"][f"{dir}sw{job}"] = sw_data
            parsed_power["h"][f"{dir}hw{job}"] = hw_data
            sw_data = np.genfromtxt(f"{dir}sw{job}_h_power_s.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{job}_h_power_s.csv", delimiter=',')
            parsed_power["s"][f"{dir}sw{job}_shared"] = sw_data
            parsed_power["h"][f"{dir}hw{job}_shared"] = hw_data

def compareCoreUsage():
    per = {}
    for cpu_type in ["cu_h", "cu_l"]:
        for file, gnbs in parsed_cpu[cpu_type].items():
            total_core = sum(entry["cpu"][0] for entry in gnbs.values())
            total_usr = sum(entry["usr"][0] for entry in gnbs.values())
            total_sys = sum(entry["sys"][0] for entry in gnbs.values())
            per[file] = [total_core, total_usr, total_sys]
    new_per_h_h_core, new_per_h_h_sys, new_per_h_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "hw" in file and dir_new in file])
    new_per_s_h_core, new_per_s_h_sys, new_per_s_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "sw" in file and dir_new in file])
    new_per_s_h_s_core, new_per_s_h_s_sys, new_per_s_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "sw" in file and dir_new in file])
    new_per_h_h_s_core, new_per_h_h_s_sys, new_per_h_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "hw" in file and dir_new in file]) 
    
    old_per_h_h_core, old_per_h_h_sys, old_per_h_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "hw" in file and dir_old in file])
    old_per_s_h_core, old_per_s_h_sys, old_per_s_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "sw" in file and dir_old in file])
    old_per_s_h_s_core, old_per_s_h_s_sys, old_per_s_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "sw" in file and dir_old in file])
    old_per_h_h_s_core, old_per_h_h_s_sys, old_per_h_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "hw" in file and dir_old in file]) 

    no_per_h_h_core, no_per_h_h_sys, no_per_h_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "hw" in file and dir_no in file])
    no_per_s_h_core, no_per_s_h_sys, no_per_s_h_usr = parse_metrics([x for file, x in per.items() if "_s" not in file and "sw" in file and dir_no in file])
    no_per_s_h_s_core, no_per_s_h_s_sys, no_per_s_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "sw" in file and dir_no in file])
    no_per_h_h_s_core, no_per_h_h_s_sys, no_per_h_h_s_usr = parse_metrics([x for file, x in per.items() if "_s" in file and "hw" in file and dir_no in file]) 


    new_per_h_h_pct = percent_increase(new_per_h_h_core, no_per_h_h_core)
    old_per_h_h_pct = percent_increase(old_per_h_h_core, no_per_h_h_core)

    new_per_s_h_pct = percent_increase(new_per_s_h_core, no_per_s_h_core)
    old_per_s_h_pct = percent_increase(old_per_s_h_core, no_per_s_h_core)

    new_per_h_h_s_pct = percent_increase(new_per_h_h_s_core, no_per_h_h_s_core)
    old_per_h_h_s_pct = percent_increase(old_per_h_h_s_core, no_per_h_h_s_core)

    new_per_s_h_s_pct = percent_increase(new_per_s_h_s_core, no_per_s_h_s_core)
    old_per_s_h_s_pct = percent_increase(old_per_s_h_s_core, no_per_s_h_s_core)


    x_axis = [f"{i} DUs" for i in dus]
    x_axis_shared = [f"{i} DUs" for i in [2]]
    w, x, x_s = 0.25, np.arange(len(x_axis)), np.arange(len(x_axis_shared))

    hatch_handles = [
        mpatches.Patch(facecolor='white', label='New Log Method', hatch=''),
        mpatches.Patch(facecolor='white', label='Old Log Method', hatch='//'),
    ]


    fig, ax = plt.subplots()

    ax.bar(x - w/2, new_per_h_h_pct, width=w, color='white', edgecolor='black')
    ax.bar(x + w/2 , old_per_h_h_pct, width=w, color='white', edgecolor='black', hatch='//')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Core Usage Increase (%) vs No Logs')
    ax.legend(handles=hatch_handles)
    ax.set_title("Hardware Core Usage Comparison Across Profiling Methods (Distributed Cores, High Load)", fontsize=9, loc='center')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/HardwareCompareCoreUsage.png', dpi=300)

    fig, ax = plt.subplots()

    ax.bar(x - w/2, new_per_s_h_pct, width=w, color='white', edgecolor='black')

    ax.bar(x + w/2, old_per_s_h_pct, width=w, color='white', edgecolor='black', hatch='//')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Core Usage Increase (%) vs No Logs')
    ax.legend(handles=hatch_handles)
    ax.set_title("Software Core Usage Comparison Across Profiling Methods (Distributed Cores, High Load)", fontsize=9, loc='center')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/SoftwareCompareCoreUsage.png', dpi=300)

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, new_per_h_h_s_pct, width=w, color='white', edgecolor='black')

    ax.bar(x_s + w/2, old_per_h_h_s_pct, width=w, color='white', edgecolor='black', hatch='//')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Core Usage Increase (%) vs No Logs')
    ax.legend(handles=hatch_handles)
    ax.set_title("Hardware Core Usage Comparison Across Profiling Methods (Shared Cores, High Load)", fontsize=9, loc='center')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/HardwareCompareCoreUsageShared.png', dpi=300)

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, new_per_s_h_s_pct, width=w, color='white', edgecolor='black')

    ax.bar(x_s + w/2, old_per_s_h_s_pct, width=w, color='white', edgecolor='black', hatch='//')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Core Usage Increase (%) vs No Logs')
    ax.legend(handles=hatch_handles)
    ax.set_title("Software Core Usage Comparison Across Profiling Methods (Shared Cores, High Load)", fontsize=9, loc='center')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/SoftwareCompareCoreUsageShared.png', dpi=300)

def comparePower():
    marker_handles = [
        Line2D([0], [0], marker='+', color='black', linestyle='None',
            markersize=10, label='New Log Method'),
        Line2D([0], [0], marker='o', color='black', linestyle='None',
            markersize=8, label='Old Log Method')
    ]

    dist_handles = [
        mpatches.Patch(color='darkgrey', label='Shared Cores'),
        mpatches.Patch(color='black', label='Distributed Cores')
    ]

    baseline_dist = None
    baseline_shared = None

    for key, arr in parsed_power["h"].items():
        if dir_no in key:
            if "shared" in key:
                baseline_shared = arr[:,0]
            else:
                baseline_dist = arr[:,0]

    fig, ax = plt.subplots(figsize=(8, 4))
    for key, arr in parsed_power["h"].items():
        if dir_no not in key:
            colour = "black"
            if dir_new in key:
                marker = "+"
            else:
                marker = "o"

            if "shared" in key:
                colour = "darkgrey"
                baseline = baseline_shared
            else:
                baseline = baseline_dist

            average = arr[:, 0]  
            pct = percent_increase(average, baseline)
            time = np.arange(len(average)) * 10 
            plt.plot(time, pct, color=colour, marker=marker)

    plt.xlabel('Time (Seconds)')
    plt.ylabel('Power Increase (%) vs No Logs')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small', handles=dist_handles+marker_handles)
    plt.title("Hardware Power Comparison Across Profiling Methods (4 DUs, High Load)")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/profPlots/HardwarePowerComparison.png', dpi=300)

    baseline_dist = None
    baseline_shared = None

    for key, arr in parsed_power["s"].items():
        if dir_no in key:
            if "shared" in key:
                baseline_shared = arr[:,0]
            else:
                baseline_dist = arr[:,0]

    fig, ax = plt.subplots(figsize=(8, 4))
    for key, arr in parsed_power["s"].items():
        if dir_no not in key:
            colour = "black"
            if dir_new in key:
                marker = "+"
            else:
                marker = "o"

            if "shared" in key:
                colour = "darkgrey"
                baseline = baseline_shared
            else:
                baseline = baseline_dist

            average = arr[:, 0]  
            pct = percent_increase(average, baseline)
            time = np.arange(len(average)) * 10 
            plt.plot(time, pct, color=colour, marker=marker)

    plt.xlabel('Time (Seconds)')
    plt.ylabel('Power Increase (%) vs No Logs')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small', handles=dist_handles+marker_handles)
    plt.title("Software Power Comparison Across Profiling Methods (4 DUs, High Load)")
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/profPlots/SoftwarePowerComparison.png', dpi=300)

def cpuWatts():
    x_axis = ["2 DUs", "2 DUs (S)"]
    w, x = 0.25, np.arange(len(x_axis))

    fig, ax = plt.subplots(figsize=(8,4))
    
    new_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_new in k and "hw" in k]
    no_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_no in k and "hw" in k]
    old_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_old in k and "hw" in k]

    new_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_new in k and "hw" in k]
    no_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_no in k and "hw" in k]
    old_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_old in k and "hw" in k]
 
    new = new_mean + new_mean_s
    old = old_mean + old_mean_s
    no = no_mean + no_mean_s

    ax.bar(x - w, new, width=w, label="New Log Method")
    ax.bar(x , old, width=w, label="Old Log Method")
    ax.bar(x + w, no, width=w, label="No Logs")

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Mean Watts (W)')
    ax.set_title("Hardware CPU Power Comparison Across Profiling Methods", fontsize=9, loc='center')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/HardwareCPUPowerComparison.png', dpi=300)

    fig, ax = plt.subplots(figsize=(8,4))
    
    new_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_new in k and "sw" in k]
    no_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_no in k and "sw" in k]
    old_mean = [v for k,v in parsed_cpu_power["dist"].items() if dir_old in k and "sw" in k]

    new_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_new in k and "sw" in k]
    no_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_no in k and "sw" in k]
    old_mean_s = [v for k,v in parsed_cpu_power["shared"].items() if dir_old in k and "sw" in k]
 
    new = new_mean + new_mean_s
    old = old_mean + old_mean_s
    no = no_mean + no_mean_s

    ax.bar(x - w, new, width=w, label="New Log Method")
    ax.bar(x , old, width=w, label="Old Log Method")
    ax.bar(x + w, no, width=w, label="No Logs")

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Mean Watts (W)')
    ax.set_title("Software CPU Power Comparison Across Profiling Methods", fontsize=9, loc='center')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small')
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/profPlots/SoftwareCPUPowerComparison.png', dpi=300)

def compareThroughput():
    cell_metrics = {d: get_metrics(d) for d in dirs}

    tp_pusch = defaultdict(lambda: defaultdict(list))  # uplink
    tp_pdsch = defaultdict(lambda: defaultdict(list))  # downlink

    for dir_name, entries in cell_metrics.items():
        for k, entry_list in entries.items():
            if "4" not in k or "6" not in k or "8" not in k:
                key_type = "shared" if "_s" in k else "dist"
                for entry in entry_list:
                    tp_pusch[key_type][k].append(entry["ul_brate"])
                    tp_pdsch[key_type][k].append(entry["dl_brate"])

    # Compute median values
    def compute_medians(tp_dict):
        result = {}
        for log_type, name in [("new", dir_new), ("old", dir_old), ("no", dir_no)]:
            medians = []
            for key_type in ["dist", "shared"]:
                for k, v in tp_dict[key_type].items():
                    if name in k and "sw" in k and ("2" in k or "1" in k):
                        medians.append(np.median(v))
            result[log_type] = medians
        return result

    pusch_sw = compute_medians(tp_pusch)
    pdsch_sw = compute_medians(tp_pdsch)

    # Compute percentage change relative to No Logs
    def percent_change(data_dict):
        no_base = np.array(data_dict["no"])
        print(no_base)
        result = {}
        for key in ["new", "old"]:
            result[key] = ((np.array(data_dict[key]) - no_base) / no_base) * 100
        return result

    pusch_sw_pct = percent_change(pusch_sw)
    pdsch_sw_pct = percent_change(pdsch_sw)

    # Lollipop plot function
    def plot_lollipop(pusch_dict, pdsch_dict):
        x_axis = ["1 DU", "2 DUs", "2 DUs (S)"]
        titles = ["Uplink Throughput", "Downlink Throughput"]
        x = np.arange(len(x_axis))
        w = 0.15  # horizontal offset for markers
        fig, axes = plt.subplots(1, 2, figsize=(8,4))
        for i,data_dict in enumerate([pusch_dict, pdsch_dict]):
            title = titles[i]
            for offset, label, method, color in [(-w, "Aggregated Logging", "new", "#1f77b4"), (w, "Per-Function-Call Logging", "old", "#ff7f0e")]:
                # vertical lines
                axes[i].vlines(x + offset, 0, data_dict[method], color=color, alpha=0.7, linewidth=2)
                # markers
                axes[i].plot(x + offset, data_dict[method], 'o', color=color, markersize=6, label=f"{label.title()}")

            axes[i].axhline(0, color='gray', linestyle='--', linewidth=0.8)  # baseline
            axes[i].set_xticks(x)
            axes[i].set_xticklabels(x_axis)
            axes[i].set_title(title, fontsize=8)
            if i == 0:
                axes[i].set_ylabel('Percentage Change vs No Logs (%)')
            if i == 1:
                axes[i].legend(loc='upper left', fontsize='small', framealpha=0.5, bbox_to_anchor=(1,1))
        plt.tight_layout()
        plt.savefig('/home/fatim/fatim/profPlots/SoftwareTPComparison.png', dpi=300)

    # Generate lollipop plots
    plot_lollipop(pusch_sw_pct, pdsch_sw_pct)
    # plot_lollipop(pusch_sw_pct, "Software Uplink Throughput % Change vs No Logs", '/home/fatim/fatim/profPlots/SoftwareUplinkTPComparison.png')
    # plot_lollipop(pdsch_sw_pct, "Software Downlink Throughput % Change vs No Logs", '/home/fatim/fatim/profPlots/SoftwareDownlinkTPComparison.png')

    # fig, ax = plt.subplots(figsize=(8,4))

    # ax.bar(x - w, new_pusch_hw, width=w, label="New Log Method")
    # ax.bar(x , old_pusch_hw, width=w, label="Old Log Method")
    # ax.bar(x + w, no_pusch_hw, width=w, label="No Logs")

    # ax.set_xticks(x)
    # ax.set_xticklabels(x_axis)
    # ax.set_ylabel('Mean Throughput (Mbps)')
    # ax.set_title("hardware Uplink Throughput Comparison Across Profiling Methods", fontsize=9, loc='center')
    # ax.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small')
    # plt.tight_layout()

    # plt.savefig('/home/fatim/fatim/profPlots/HardwareTPUplinkComparison.png', dpi=300)

    # fig, ax = plt.subplots(figsize=(8,4))

    # ax.bar(x - w, new_pdsch_hw, width=w, label="New Log Method")
    # ax.bar(x , old_pdsch_hw, width=w, label="Old Log Method")
    # ax.bar(x + w, no_pdsch_hw, width=w, label="No Logs")

    # ax.set_xticks(x)
    # ax.set_xticklabels(x_axis)
    # ax.set_ylabel('Mean Throughput (Mbps)')
    # ax.set_title("Hardware Downlink Throughput Comparison Across Profiling Methods", fontsize=9, loc='center')
    # ax.legend(loc='upper right', bbox_to_anchor=(1.3,1), fontsize='small')
    # plt.tight_layout()

    # plt.savefig('/home/fatim/fatim/profPlots/HardwareTPDownlinkComparison.png', dpi=300)

compareCoreUsage()
comparePower()
compareThroughput()
cpuWatts()