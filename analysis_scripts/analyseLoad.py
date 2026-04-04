import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import re

dus = [1,2, 4, 5, 6, 8]
modes = {"h":"High Load", "l":"Low Load"}
exp_title = {
    "new": "Under Different Loads and Number of DUs",
    "smt": "Under Different Loads and Number of DUs (SMT Enabled, Siblings Paired)",
    "smtsib": "Under Different Loads and Number of DUs (SMT Enabled, Siblings Competing)"}

def median_std_labels(median, std):
    labels = np.empty(median.shape, dtype=object)
    for i in range(median.shape[0]):
        for j in range(median.shape[1]):
            labels[i, j] = f"{median[i, j]:.1f}\n±{std[i, j]:.1f}"
    return labels

def power_labels(power, cpu):
    labels = np.empty(power.shape, dtype=object)
    for i in range(power.shape[0]):
        for j in range(power.shape[1]):
            labels[i, j] = f"{int(power[i, j])}\n({int(cpu[i, j])})"
    return labels

def latency(exp, exp_logs):
    latency = defaultdict(lambda: {"ul": [], "dl": []})
    stuck_sec = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]
            stuck_sec[k]["ul"] = entry["ul_stuck"]
            stuck_sec[k]["dl"] = entry["dl_stuck"]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]
            stuck_sec[k]["ul"] = entry["ul_stuck"]
            stuck_sec[k]["dl"] = entry["dl_stuck"]
    

    heat_matrix_software_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    sw_dist_ul = np.zeros((len(modes), len(dus)))
    sw_dist_dl = np.zeros((len(modes), len(dus)))
    hw_dist_ul = np.zeros((len(modes), len(dus)))
    hw_dist_dl = np.zeros((len(modes), len(dus)))

    sw_shared_ul = np.zeros((len(modes), len(dus[1:])))
    sw_shared_dl = np.zeros((len(modes), len(dus[1:])))
    hw_shared_ul = np.zeros((len(modes), len(dus[1:])))
    hw_shared_dl = np.zeros((len(modes), len(dus[1:])))
    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Median Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Uplink Latency {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/UplinkLatency.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Downlink Latency {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/DownlinkLatency.png')


    for k, vals in stuck_sec.items():
        log = k.split("/")[-1]
        du = None
        mode = None
        for p in log.split("_"):
            if p.startswith("sw"):
                du = int(p[2:])
            elif p.startswith("hw"):
                du = int(p[2:])
            elif p in modes.keys():
                mode = p

        if du is None or mode is None:
            continue

        i = list(modes.keys()).index(mode)

        # Dist vs Shared
        if "_s" in log and du in dus:
            if "sw" in log:
                j = dus[1:].index(du)
                sw_shared_ul[i, j] = np.sum(vals["ul"])
                sw_shared_dl[i, j] = np.sum(vals["dl"])
            else:
                j = dus[1:].index(du)
                hw_shared_ul[i, j] = np.sum(vals["ul"])
                hw_shared_dl[i, j] = np.sum(vals["dl"])
        elif du in dus:
            if "sw" in log:
                j = dus.index(du)
                sw_dist_ul[i, j] = np.sum(vals["ul"])
                sw_dist_dl[i, j] = np.sum(vals["dl"])
            else:
                j = dus.index(du)
                hw_dist_ul[i, j] = np.sum(vals["ul"])
                hw_dist_dl[i, j] = np.sum(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    sns.heatmap(sw_dist_ul+sw_dist_dl,
            annot=power_labels(sw_dist_ul, sw_dist_dl), fmt="", 
            xticklabels=dus, yticklabels=modes.values(),
            cbar_kws={'label': 'Stuck Seconds'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(sw_shared_ul+sw_shared_dl, 
                annot=power_labels(sw_shared_ul, sw_shared_dl), fmt="", 
                xticklabels=dus[1:], yticklabels=modes.values(),
                cbar_kws={'label': 'Stuck Seconds'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(hw_dist_ul+hw_dist_dl, 
                annot=power_labels(hw_dist_ul, hw_dist_dl), fmt="", 
                xticklabels=dus, yticklabels=modes.values(),
                cbar_kws={'label': 'Stuck Seconds'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(hw_shared_ul+hw_shared_dl, 
                annot=power_labels(hw_shared_ul, hw_shared_dl), fmt="", 
                xticklabels=dus[1:], yticklabels=modes.values(),
                cbar_kws={'label': 'Stuck Seconds'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle("UL+DL Full Stall Seconds", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/Stall.png')

    experiments = [6, 7, 8]

    for exps in experiments:
        ul_sw_dist, dl_sw_dist = [], []
        ul_hw_dist, dl_hw_dist = [], []
        ul_sw_shared, dl_sw_shared = [], []
        ul_hw_shared, dl_hw_shared = [], []
        for k, vals in stuck_sec.items():
            if f"{exps}_l" in k:
                if "sw" in k:
                    if "_s." in k:
                        ul_sw_shared.extend(vals["ul"])
                        dl_sw_shared.extend(vals["dl"])
                    else:
                        ul_sw_dist.extend(vals["ul"])
                        dl_sw_dist.extend(vals["dl"])
                elif "hw" in k:
                    if "_s." in k:
                        ul_hw_shared.extend(vals["ul"])
                        dl_hw_shared.extend(vals["dl"])
                    else:
                        ul_hw_dist.extend(vals["ul"])
                        dl_hw_dist.extend(vals["dl"])

        max_dus = max(len(ul_sw_dist), len(ul_hw_dist), len(ul_sw_shared), len(ul_hw_shared))
        dus_labels = [f"DU{i+1}" for i in range(max_dus)]
        x = np.arange(max_dus)
        total_w = 0.8
        w = total_w / 4 

        fig, axes = plt.subplots(1, 2, figsize=(8, 4), sharey=True)
        axes[0].bar(x - 1.5*w, ul_hw_dist, w,
                    label="UL", color="navy")
        axes[0].bar(x - 0.5*w, dl_hw_dist, w,
                    label="DL", color="red")
        axes[0].bar(x + 0.5*w, ul_hw_shared, w,
                    label="UL Shared", color="navy", hatch='//', edgecolor='white')
        axes[0].bar(x + 1.5*w, dl_hw_shared, w,
                    label="DL Shared", color="red", hatch='//', edgecolor='white')
        axes[0].set_title("Hardware")
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(dus_labels)
        axes[0].set_xlabel("DUs")
        axes[0].set_ylabel("Total Starved Seconds")

        axes[1].bar(x - 1.5*w, ul_sw_dist, w,
                    label="UL", color="navy")
        axes[1].bar(x - 0.5*w, dl_sw_dist, w,
                    label="DL", color="red")
        axes[1].bar(x + 0.5*w, ul_sw_shared, w,
                    label="UL Shared", color="navy", hatch='//', edgecolor='white')
        axes[1].bar(x + 1.5*w, dl_sw_shared, w,
                    label="DL Shared", color="red", hatch='//', edgecolor='white')
        axes[1].set_title("Software")
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(dus_labels)
        axes[1].set_xlabel("DUs")
        axes[1].legend(loc='upper left', bbox_to_anchor=(1,1))
        plt.tight_layout()
        plt.savefig(f'/home/fatim/fatim/plots/{exp}/Stall{exps}PerDU.png')

def server_energy(exp, exp_logs): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for mode in modes.keys():
            sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{mode}"] = sw_data[:,0]
            if mode != "h" or du != 10:
                hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_power.csv", delimiter=',')
                parsed_power["h"][f"hw{du}_{mode}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{mode}_shared"] = sw_data[:,0]
                if mode != "h" or du != 10:
                    hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_power_s.csv", delimiter=',')
                    parsed_power["h"][f"hw{du}_{mode}_shared"] = hw_data[:,0]

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))


    for k,v in parsed_power["s"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Power Consumption {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/Power.png')

def cpu_watts(exp, exp_logs):
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for mode in modes.keys():
            sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{mode}"] = sw_data
            if mode != "h" or du != 10:
                hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_energy.csv", delimiter=',')
                parsed_power_cpu["h"][f"hw{du}_{mode}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{mode}_shared"] = sw_data
                if mode != "h" or du != 10:
                    hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_energy_s.csv", delimiter=',')
                    parsed_power_cpu["h"][f"hw{du}_{mode}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
                    
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)

        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median CPU Power Consumption {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/CPUPower.png')

def cpu_usage(exp, exp_logs):
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for mode in modes.keys():
            log_files = [f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_cpu.log"]
            if mode != "h" or du != 10:
                log_files.append(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_cpu.log")
            if du > 1:
                log_files.append(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_cpu_s.log")
                if mode != "h" or du != 10:
                    log_files.append(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_cpu_s.log")
            for log_file in log_files:
                with open(log_file, 'r') as f:
                        i = 0
                        accum_cpu = 0
                        off_cpu = 0
                        for line in f:
                            gnb = i % du
                            line = line.strip()
                            split = line.split()
                            if gnb == 0:
                                if "sw" in log_file:
                                    parsed_cpu["s"][log_file].append((accum_cpu, off_cpu))
                                else:    
                                    parsed_cpu["h"][log_file].append((accum_cpu, off_cpu)) 
                                accum_cpu = float(split[7])
                                off_cpu = float(split[6])
                            else:
                                accum_cpu += float(split[7])
                                off_cpu += float(split[6])
                            i += 1  

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_off = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_off = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_off = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_off = np.zeros((len(modes), len(dus[1:])))


    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(np.array(v)[:,0])
                    heat_matrix_software_s_off[i, j] = np.median(np.array(v)[:,1])
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(np.array(v)[:,0])
                heat_matrix_software_off[i, j] = np.median(np.array(v)[:,1])

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(np.array(v)[:,0])
                    heat_matrix_hardware_s_off[i, j] = np.median(np.array(v)[:,1])
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(np.array(v)[:,0])
                heat_matrix_hardware_off[i, j] = np.median(np.array(v)[:,1])
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=power_labels(heat_matrix_software, heat_matrix_software_off), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=power_labels(heat_matrix_software_s, heat_matrix_software_s_off), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=power_labels(heat_matrix_hardware, heat_matrix_hardware_off), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=power_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_off), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median CPU Usage {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/CPUUsage.png')

def throughput(exp, exp_logs):
    tp = defaultdict(lambda: defaultdict(list))
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    heat_matrix_software_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                                    
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"]) 
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
                    

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Uplink Throughput {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/UplinkTP.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Downlink Throughput {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/DownlinkTP.png')    

def uplink_downlink_usage(exp, exp_logs):
    usage = defaultdict(lambda: defaultdict(list))
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"]= [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"] = [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    
    heat_matrix_software_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in usage.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Uplink CPU Usage {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/UplinkUsage.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Median Downlink CPU Usage {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/DownlinkUsage.png')  

def memory_usage(exp, exp_logs):
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for mode in modes.keys():
            sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{mode}"] = sw_data
            if mode != "h" or du != 10:
                hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_mem.csv", delimiter=',')
                parsed_mem["h"][f"hw{du}_{mode}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_shared"] = sw_data
                if mode != "h" or du != 10:
                    hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_mem_s.csv", delimiter=',')
                    parsed_mem["h"][f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)
                    with open(f"/home/fatim/fatim/{exp_logs}/mem_sw{du}_{mode}_s.log") as f:
                        total_mem = int(f.readline())    
                    heat_matrix_software_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_software_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                with open(f"/home/fatim/fatim/{exp_logs}/mem_sw{du}_{mode}.log") as f:
                        total_mem = int(f.readline())  
                heat_matrix_software[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_software_std[i, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    with open(f"/home/fatim/fatim/{exp_logs}/mem_hw{du}_{mode}_s.log") as f:
                        total_mem = int(f.readline())  
                    heat_matrix_hardware_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_hardware_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)  
                j = dus.index(du)    
                with open(f"/home/fatim/fatim/{exp_logs}/mem_hw{du}_{mode}.log") as f:
                        total_mem = int(f.readline())  
                heat_matrix_hardware[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_hardware_std[i, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/MemUsage.png')

def ldpc_encoding(exp, exp_logs):
    enc_latency = defaultdict()
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]            
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"]]  

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.mean(vals) 
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.mean(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.mean(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.mean(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Average LDPC Encoder and Rate Matching Latency {exp_title[exp]}", fontsize=10)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/EncoderLatency.png')

def ldpc_decoding(exp, exp_logs):
    dec_latency = defaultdict()
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"]]

    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.mean(vals)
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.mean(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.mean(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.mean(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Average LDPC Decoder and Rate Dematching Latency {exp_title[exp]}", fontsize=10)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/DecoderLatency.png')

def cache(exp, exp_logs):
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for mode in modes.keys():
            log_files = [f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_cache.log"]
            if mode != "h" or du != 10:
                log_files.append(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_cache.log")
            if du > 1:
                log_files.append(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_cache_s.log")
                if mode != "h" or du != 10:
                    log_files.append(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_cache_s.log")
            for log_file in log_files:
                with open(log_file, 'r') as f:
                        i = 0
                        cache_ref = 0
                        cache_miss = 0
                        l1_load = 0
                        l1_miss = 0
                        for line in f:
                            line_num = i % 5
                            line = line.strip()
                            split = line.split(",")
                            if line_num == 0:
                                if split[1].strip() == "cache-references":
                                    cache_ref = int(split[0])
                            
                            elif line_num == 1:
                                if split[1].strip() == "cache-misses":
                                    cache_miss = int(split[0])
                            
                            elif line_num == 2:
                                if split[1].strip() == "L1-dcache-loads":
                                    l1_load = int(split[0])
                            
                            elif line_num == 4:
                                if split[1].strip() == "L1-dcache-load-misses":
                                    l1_miss = int(split[0])
                                if "sw" in log_file:
                                    parsed_cache["s"][log_file]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                                    parsed_cache["s"][log_file]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                                else:    
                                    parsed_cache["h"][log_file]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                                    parsed_cache["h"][log_file]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                            i += 1    


    heat_matrix_software = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_llc = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_llc = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_llc = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_llc = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_std_llc = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_std_llc = np.zeros((len(modes), len(dus)))

    heat_matrix_software_s_std_llc = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_s_std_llc = np.zeros((len(modes), len(dus[1:])))

    for k,v in parsed_cache["s"].items():
        if "_s" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v["L1"])
                    heat_matrix_software_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_software_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_software_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode)
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v["L1"])
                heat_matrix_software_std[i, j] = np.std(v["L1"])
                heat_matrix_software_llc[i, j] = np.median(v["LLC"])
                heat_matrix_software_std_llc[i, j] = np.std(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_s" in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v["L1"])
                    heat_matrix_hardware_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_hardware_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_hardware_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            mode = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
            
            if du in dus and mode in modes.keys():
                i = list(modes.keys()).index(mode) 
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v["L1"])
                heat_matrix_hardware_std[i, j] = np.std(v["L1"])
                heat_matrix_hardware_llc[i, j] = np.median(v["LLC"])
                heat_matrix_hardware_std_llc[i, j] = np.std(v["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Software L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Software L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_software_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Software LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_software_s_llc, annot=median_std_labels(heat_matrix_software_s_llc, heat_matrix_software_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Software LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Load")

    plt.suptitle(f"Software Cache Hit Ratio {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/SoftwareCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Hardware L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Hardware L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_hardware_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Load")

    sns.heatmap(heat_matrix_hardware_s_llc, annot=median_std_labels(heat_matrix_hardware_s_llc, heat_matrix_hardware_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Load")

    plt.suptitle(f"Hardware Cache Hit Ratio {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/HardwareCache.png')

def proc_rate(exp, exp_logs):
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["pdsch"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Average PUSCH Processing Rate {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/PUSCHRate.png')
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.suptitle(f"Average PDSCH Processing Rate {exp_title[exp]}", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/PDSCHRate.png')

def noks(exp, exp_logs):
    noks_rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            noks_rate[k]["dl"] = [e["dl_nok"] / (e["dl_nok"] + e["dl_ok"]) *100 for e in entry["metrics_cell"]]
            noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    with open(f"/home/fatim/fatim/{exp_logs}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            noks_rate[k]["dl"] = [e["dl_nok"]/ (e["dl_nok"] + e["dl_ok"]) *100  for e in entry["metrics_cell"]]
            noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    heat_matrix_software_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in noks_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode) 
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode) 
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(12, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd" ,cbar_kws={'label': 'Average BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul[:, :-1], annot=median_std_labels(heat_matrix_hardware_ul[:, :-1], heat_matrix_hardware_ul_std[:, :-1]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/UplinkBLER.png')


    fig, axes = plt.subplots(2, 2, figsize=(12, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl[:, :-1], annot=median_std_labels(heat_matrix_hardware_dl[:, :-1], heat_matrix_hardware_dl_std[:, :-1]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/DownlinkBLER.png')

def server_cpu_power(exp, exp_logs):
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for mode in modes.keys():
            sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{mode}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{mode}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{mode}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{mode}_shared"] = hw_data[:,0]
    
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for mode in modes.keys():
            sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{mode}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{mode}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/sw{du}_{mode}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"/home/fatim/fatim/{exp_logs}/hw{du}_{mode}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{mode}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{mode}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_software_cpu = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_hardware_cpu = np.zeros((len(modes), len(dus[1:])))

    for k,v in parsed_power["s"].items():
        if "_shared" in k:   
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                        mode = p
                
            if du in dus[1:] and mode in modes.keys():
                i = list(modes.keys()).index(mode)   
                j = dus[1:].index(du)    
                heat_matrix_software[i, j] = np.mean(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                
                if du in dus[1:] and mode in modes.keys():
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware[i, j] = np.mean(v)

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                
            if du in dus[1:] and mode in modes.keys():
                i = list(modes.keys()).index(mode)   
                j = dus[1:].index(du)    
                heat_matrix_software_cpu[i, j] = np.mean(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:  
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                        mode = p
                
            if du in dus[1:] and mode in modes.keys():
                i = list(modes.keys()).index(mode)   
                j = dus[1:].index(du)    
                heat_matrix_hardware_cpu[i, j] = np.mean(v)
    

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.heatmap(heat_matrix_software, annot=power_labels(heat_matrix_software, heat_matrix_software_cpu), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0])
    axes[0].set_title("Software")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware, annot=power_labels(heat_matrix_hardware, heat_matrix_hardware_cpu), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1])
    axes[1].set_title("Hardware")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Load")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/PowerComparison.png')

def cxtswitches(exp, exp_logs):
    hw = []
    sw = []
    hw_s = []
    sw_s = []
    dir = f"/home/fatim/fatim/{exp_logs}/"
    log_files = [f"{dir}sw2_h_cpu.log", f"{dir}hw2_h_cpu.log", f"{dir}sw2_h_cpu_s.log", f"{dir}hw2_h_cpu_s.log"]
    for log_file in log_files:
        with open(log_file, 'r') as f:
            i = 0
            vol_cpu = 0
            nonvol_cpu = 0
            for line in f:
                gnb = i % 2
                line = line.strip()
                split = line.split()
                if gnb == 0:
                    if "sw" in log_file:
                        if "_s." in log_file:
                            sw_s.append((vol_cpu, nonvol_cpu))
                        else:
                            sw.append((vol_cpu, nonvol_cpu))
                    else:    
                        if "_s." in log_file:
                            hw_s.append((vol_cpu, nonvol_cpu))
                        else:
                            hw.append((vol_cpu, nonvol_cpu)) 
                    vol_cpu = float(split[14])
                    nonvol_cpu = float(split[15])
                else:
                    vol_cpu += float(split[14])
                    nonvol_cpu += float(split[15])
                i += 1  
    
    categories = [hw, sw, hw_s, sw_s]
    x_labels = ["Hardware", "Software", "Hardware (Shared)", "Software (Shared)"]

    mean_vol = [np.mean([v for v, nv in c]) for c in categories]
    mean_non = [np.mean([nv for v, nv in c]) for c in categories]
    std_vol = [np.std([v for v, nv in c]) for c in categories]
    std_non = [np.std([nv for v, nv in c]) for c in categories]

    width = 0.35
    x = np.arange(len(x_labels))

    fig, ax = plt.subplots(figsize=(8,4))
    bars_vol = ax.bar(x - width/2, mean_vol, width, label="Voluntary", color="navy")
    bars_non = ax.bar(x + width/2, mean_non, width, label="Non-Voluntary", color= "red")

    for bar, std in zip(bars_vol, std_vol):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"±{std:.1f}", ha='center', va='bottom')

    for bar, std in zip(bars_non, std_non):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"±{std:.1f}", ha='center', va='bottom')

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel("Context Switches Per Second")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'/home/fatim/fatim/plots/{exp}/Context.png')

def smtCompare():
    exp_logs = ["smtsib_logs", "smt_logs", "new_logs16"]
    exps = ["smtsib", "smt", "new"]
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    for exp in exp_logs:
        with open(f"/home/fatim/fatim/{exp}/parsed_logs.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                proc_rate[f"{k}_{exp}"]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
                proc_rate[f"{k}_{exp}"]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

        with open(f"/home/fatim/fatim/{exp}/parsed_logs_shared.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                proc_rate[f"{k}_{exp}"]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
                proc_rate[f"{k}_{exp}"]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(exps), len(modes), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(exps), len(modes), len(dus)))

    heat_matrix_software_dl = np.zeros((len(exps), len(modes), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(exps), len(modes), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(exps), len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(exps), len(modes), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(exps), len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(exps), len(modes), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(exps), len(modes), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(exps), len(modes), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(exps), len(modes), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(exps), len(modes), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(exps), len(modes), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(exps), len(modes), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(exps), len(modes), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(exps), len(modes), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du in dus[1:] and mode in modes.keys() and experiment in exps:
                    x = exps.index(experiment)
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[x, i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl_s[x, i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_s_std[x, i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[x, i, j] = np.std(vals["pdsch"])
            else:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du in dus and mode in modes.keys() and experiment in exps:
                    x = exps.index(experiment)
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[x, i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl[x, i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_std[x, i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[x, i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du in dus[1:] and mode in modes.keys() and experiment in exps:
                    x = exps.index(experiment)
                    i = list(modes.keys()).index(mode)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[x, i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl_s[x, i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[x, i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[x, i, j]= np.std(vals["pdsch"])
            else:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du in dus and mode in modes.keys() and experiment in exps:
                    x = exps.index(experiment)
                    i = list(modes.keys()).index(mode)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[x, i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl[x, i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_std[x, i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[x, i, j] = np.std(vals["pdsch"])

    fig, axes = plt.subplots(3, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_hardware_ul[0, :, :], annot=median_std_labels(heat_matrix_hardware_ul[0, :, :], heat_matrix_hardware_ul_std[0, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("SMT Enabled (Siblings Competing)")
    # axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s[0, :, :], annot=median_std_labels(heat_matrix_hardware_ul_s[0, :, :], heat_matrix_hardware_ul_s_std[0, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("SMT Enabled (Siblings Competing, Shared Cores)")
    # axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul[1, :, :], annot=median_std_labels(heat_matrix_hardware_ul[1, :, :], heat_matrix_hardware_ul_std[1, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("SMT Enabled (Siblings Paired)")
    # axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s[1, :, :], annot=median_std_labels(heat_matrix_hardware_ul_s[1, :, :], heat_matrix_hardware_ul_s_std[1, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("SMT Enabled (Siblings Paired, Shared Cores)")
    # axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul[2, :, :], annot=median_std_labels(heat_matrix_hardware_ul[2, :, :], heat_matrix_hardware_ul_std[2, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[2,0])
    axes[2,0].set_title("SMT Disabled")
    axes[2,0].set_xlabel("DUs")
    axes[2,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_ul_s[2, :, :], annot=median_std_labels(heat_matrix_hardware_ul_s[2, :, :], heat_matrix_hardware_ul_s_std[2, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[2,1])
    axes[2,1].set_title("SMT Disabled (Shared Cores)")
    axes[2,1].set_xlabel("DUs")
    axes[2,1].set_ylabel("Load")

    plt.suptitle(f"Average PUSCH Processing Rate For Hardware-Offloaded Implementation", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/SMTComparePUSCHRate.png')
    
    fig, axes = plt.subplots(3, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_hardware_dl[0, :, :], annot=median_std_labels(heat_matrix_hardware_dl[0, :, :], heat_matrix_hardware_dl_std[0, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("SMT Enabled (Siblings Competing)")
    # axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s[0, :, :], annot=median_std_labels(heat_matrix_hardware_dl_s[0, :, :], heat_matrix_hardware_dl_s_std[0, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("SMT Enabled (Siblings Competing)")
    # axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl[1, :, :], annot=median_std_labels(heat_matrix_hardware_dl[1, :, :], heat_matrix_hardware_dl_std[1, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("SMT Enabled (Siblings Paired)")
    # axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s[1, :, :], annot=median_std_labels(heat_matrix_hardware_dl_s[1, :, :], heat_matrix_hardware_dl_s_std[1, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("SMT Enabled (Siblings Paired, Shared Cores)")
    # axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl[2, :, :], annot=median_std_labels(heat_matrix_hardware_dl[2, :, :], heat_matrix_hardware_dl_std[2, :, :]), fmt="", xticklabels=dus, yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[2,0])
    axes[2,0].set_title("SMT Disabled")
    axes[2,0].set_xlabel("DUs")
    # axes[2,0].set_ylabel("Load")

    sns.heatmap(heat_matrix_hardware_dl_s[2, :, :], annot=median_std_labels(heat_matrix_hardware_dl_s[2, :, :], heat_matrix_hardware_dl_s_std[2, :, :]), fmt="", xticklabels=dus[1:], yticklabels=modes.values(),
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[2,1])
    axes[2,1].set_title("SMT Disabled (Shared Cores)")
    axes[2,1].set_xlabel("DUs")
    # axes[2,1].set_ylabel("Load")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/SMTComparePDSCHRate.png')

def smtCache():
    exp_logs = ["smtsib_logs", "smt_logs", "new_logs16"]
    exps = ["smtsib", "smt", "new"]
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for exp in exp_logs:
        dir = f"/home/fatim/fatim/{exp}/"
        log_files = [f"{dir}sw2_h_cache.log", f"{dir}hw2_h_cache.log", f"{dir}sw2_h_cache_s.log", f"{dir}hw2_h_cache_s.log"]
        for log_file in log_files:
            with open(log_file, 'r') as f:
                i = 0
                cache_ref = 0
                cache_miss = 0
                l1_load = 0
                l1_miss = 0
                for line in f:
                    line_num = i % 5
                    line = line.strip()
                    split = line.split(",")
                    if line_num == 0:
                        if split[1].strip() == "cache-references":
                            cache_ref = int(split[0])
                    
                    elif line_num == 1:
                        if split[1].strip() == "cache-misses":
                            cache_miss = int(split[0])
                    
                    elif line_num == 2:
                        if split[1].strip() == "L1-dcache-loads":
                            l1_load = int(split[0])
                    
                    elif line_num == 4:
                        if split[1].strip() == "L1-dcache-load-misses":
                            l1_miss = int(split[0])
                        if "sw" in log_file:
                            parsed_cache["s"][f"{log_file}_{exp}"]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                            parsed_cache["s"][f"{log_file}_{exp}"]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                        else:    
                            parsed_cache["h"][f"{log_file}_{exp}"]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                            parsed_cache["h"][f"{log_file}_{exp}"]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                    i += 1

    heat_matrix_software = np.zeros(len(exps))
    heat_matrix_hardware = np.zeros(len(exps))

    heat_matrix_software_llc = np.zeros(len(exps))
    heat_matrix_hardware_llc = np.zeros(len(exps))

    heat_matrix_software_s = np.zeros(len(exps))
    heat_matrix_hardware_s = np.zeros(len(exps))

    heat_matrix_software_s_llc = np.zeros(len(exps))
    heat_matrix_hardware_s_llc = np.zeros(len(exps))

    for k,v in parsed_cache["s"].items():
        if "_s." in k:
            du = None
            mode = None
            experiment = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                elif p in exps:
                    experiment = p

            if du == 2 and experiment in exps:
                i = exps.index(experiment)
                heat_matrix_software_s[i] = np.mean(v["L1"])
                heat_matrix_software_s_llc[i] = np.mean(v["LLC"])
        else:
            du = None
            mode = None
            experiment = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                elif p in exps:
                        experiment = p
            
            if du == 2 and experiment in exps:
                i = exps.index(experiment)
                heat_matrix_software[i] = np.mean(v["L1"])
                heat_matrix_software_llc[i] = np.mean(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and experiment in exps:
                    i = exps.index(experiment)  
                    heat_matrix_hardware_s[i] = np.mean(v["L1"])
                    heat_matrix_hardware_s_llc[i] = np.mean(v["LLC"])
        else:
            du = None
            mode = None
            experiment = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                elif p in exps:
                    experiment = p
            
            if du == 2 and experiment in exps:
                i = exps.index(experiment) 
                heat_matrix_hardware[i] = np.mean(v["L1"])
                heat_matrix_hardware_llc[i] = np.mean(v["LLC"])

    plt.style.use('grayscale')
    x_axis = ["L1", "LLC"]
    w, x = 0.3, np.arange(len(x_axis))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].bar(x - w, [heat_matrix_hardware[0], heat_matrix_hardware_llc[0]], width=w, label='SMT Enabled (Siblings Paired)')
    axes[0].bar(x, [heat_matrix_hardware[1], heat_matrix_hardware_llc[1]], width=w, label='SMT Enabled (Siblings Competing)')
    axes[0].bar(x + w, [heat_matrix_hardware[2], heat_matrix_hardware_llc[2]], width=w, label='SMT Disabled')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(x_axis)
    axes[0].set_xlabel('Cache Type')
    axes[0].set_ylabel('Cache Hit Rate (%)')
    axes[0].set_title('Hardware')

    axes[1].bar(x - w, [heat_matrix_software_s[0], heat_matrix_software_s_llc[0]], width=w, label='SMT Enabled (Siblings Paired)')
    axes[1].bar(x, [heat_matrix_software_s[1], heat_matrix_software_s_llc[1]], width=w, label='SMT Enabled (Siblings Competing)')
    axes[1].bar(x + w, [heat_matrix_software_s[2], heat_matrix_software_s_llc[2]], width=w, label='SMT Disabled')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(x_axis)
    axes[1].set_ylabel('Cache Hit Rate (%)')
    axes[1].set_xlabel('Cache Type')
    axes[1].set_title('Software')
    axes[1].legend(loc='upper right', fontsize=8)
    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/plots/SMTCache.png')

def smtCpu():
    exp_logs = ["smtsib_logs", "smt_logs", "new_logs16"]
    exps = ["smtsib", "smt", "new"]
    parsed_cpu = defaultdict(lambda: defaultdict(list)) 
    for exp in exp_logs:
        dir = f"/home/fatim/fatim/{exp}/"
        log_files = [f"{dir}sw2_h_cpu.log", f"{dir}hw2_h_cpu.log", f"{dir}sw2_h_cpu_s.log", f"{dir}hw2_h_cpu_s.log"]
        for log_file in log_files:
            with open(log_file, 'r') as f:
                i = 0
                accum_cpu = 0
                off_cpu = 0
                for line in f:
                    gnb = i % 2
                    line = line.strip()
                    split = line.split()
                    if gnb == 0:
                        if "sw" in log_file:
                            parsed_cpu["s"][f"{log_file}_{exp}"].append((accum_cpu, off_cpu))
                        else:    
                            parsed_cpu["h"][f"{log_file}_{exp}"].append((accum_cpu, off_cpu)) 
                        accum_cpu = float(split[7])
                        off_cpu = float(split[6])
                    else:
                        accum_cpu += float(split[7])
                        off_cpu += float(split[6])
                    i += 1  
    
    heat_matrix_software = np.zeros((len(exps), 2))
    heat_matrix_hardware = np.zeros((len(exps), 2))

    heat_matrix_software_off = np.zeros((len(exps), 2))
    heat_matrix_hardware_off = np.zeros((len(exps), 2))

    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                experiment = None
                mode = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    i = exps.index(experiment) 
                    heat_matrix_software[i, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_software_off[i, 1] = np.mean(np.array(v)[:,1])
        else:
            du = None
            mode = None
            experiment = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                elif p in exps:
                    experiment = p
            
            if du == 2 and mode == "h" and experiment in exps:
                i = exps.index(experiment)   
                heat_matrix_software[i, 0] = np.mean(np.array(v)[:,0])
                heat_matrix_software_off[i, 0] = np.mean(np.array(v)[:,1])

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    i = exps.index(experiment)
                    heat_matrix_hardware[i, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_hardware_off[i, 1] = np.mean(np.array(v)[:,1])
        else:
            du = None
            mode = None
            experiment = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p in modes.keys():
                    mode = p
                elif p in exps:
                    experiment = p
            
            if du == 2 and mode == "h" and experiment in exps:
                i = exps.index(experiment)  
                heat_matrix_hardware[i, 0] = np.mean(np.array(v)[:,0])
                heat_matrix_hardware_off[i, 0] = np.mean(np.array(v)[:,1])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    sns.heatmap(heat_matrix_software, annot=power_labels(heat_matrix_software, heat_matrix_software_off), fmt="", xticklabels=["Distributed Cores", "Shared Cores"], yticklabels=["Siblings Competing", "Siblings Paired", "Disabled"],
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0])
    axes[0].set_title("Software")
    axes[0].set_ylabel("SMT Configuration")
    axes[0].set_xlabel("Core Allocation")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0, ha='center')

    sns.heatmap(heat_matrix_hardware, annot=power_labels(heat_matrix_hardware, heat_matrix_hardware_off), fmt="", xticklabels=["Distributed Cores", "Shared Cores"], yticklabels=["Siblings Competing", "Siblings Paired", "Disabled"],
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1])
    axes[1].set_title("Hardware")
    axes[1].set_xlabel("Core Allocation")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0, ha='center')


    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/CompareSMTCPUUsage.png')

def smt_server_cpu_power():
    exp_logs = ["smtsib_logs", "smt_logs", "new_logs16"]
    exps = ["smtsib", "smt", "new"]
    tp = defaultdict(lambda: defaultdict(list))
    for exp in exp_logs:
        with open(f"/home/fatim/fatim/{exp}/parsed_logs.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                tp[f"{k}_{exp}"]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
                tp[f"{k}_{exp}"]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

        with open(f"/home/fatim/fatim/{exp}/parsed_logs_shared.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                tp[f"{k}_{exp}"]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
                tp[f"{k}_{exp}"]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    heat_matrix_ul = np.zeros((len(modes), len(exps), len(modes)))
    heat_matrix_dl = np.zeros((len(modes),len(exps), len(modes)))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    x = exps.index(experiment)  
                    heat_matrix_ul[1, x, 1] = np.mean(vals["ul"])
                    heat_matrix_dl[1, x, 1] = np.mean(vals["dl"])

            else:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    x = exps.index(experiment)
                    heat_matrix_ul[0, x, 1] = np.mean(vals["ul"])
                    heat_matrix_dl[0, x, 1] = np.mean(vals["dl"])

        else:
            if "_s." in k:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    x = exps.index(experiment) 
                    heat_matrix_ul[1, x, 0] = np.mean(vals["ul"])
                    heat_matrix_dl[1, x, 0] = np.mean(vals["dl"])
            else:
                du = None
                mode = None
                experiment = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes.keys():
                        mode = p
                    elif p in exps:
                        experiment = p
                
                if du == 2 and mode == "h" and experiment in exps:
                    x = exps.index(experiment)
                    heat_matrix_ul[0, x, 0] = np.mean(vals["ul"])
                    heat_matrix_dl[0, x, 0] = np.mean(vals["dl"])

    
    fig, axes = plt.subplots(2, 2, figsize=(14, 6))
    sns.heatmap(heat_matrix_ul[0, :, :].T, annot=heat_matrix_ul[0, :, :].T, fmt=".1f", xticklabels=["SMT (Siblings Competing)", "SMT (Siblings Paired)", "SMT Disabled"], yticklabels=["Hardware", "Software"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink")
    # axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")
    axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=0, ha='center')
    axes[0,0].set_yticklabels(axes[0,0].get_yticklabels())

    sns.heatmap(heat_matrix_dl[0, :, :].T, annot=heat_matrix_dl[0, :, :].T, fmt=".1f", xticklabels=["SMT (Siblings Competing)", "SMT (Siblings Paired)", "SMT Disabled"], yticklabels=["Hardware", "Software"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Downlink")
    # axes[0,1].set_xlabel("DUs")
    axes[0,1].set_xlabel("Execution Modes")
    axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=0, ha='center')
    axes[0,1].set_yticklabels(axes[0,1].get_yticklabels())

    sns.heatmap(heat_matrix_ul[1, :, :].T, annot=heat_matrix_ul[1, :, :].T, fmt=".1f", xticklabels=["SMT (Siblings Competing)", "SMT (Siblings Paired)", "SMT Disabled"], yticklabels=["Hardware", "Software"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    # axes[0,0].set_xlabel("DUs")
    axes[1,0].set_title("Uplink (Shared Cores)")
    axes[1,0].set_ylabel("Execution Modes")
    axes[1,0].set_xticklabels(axes[1,0].get_xticklabels(), rotation=0, ha='center')
    axes[1,0].set_yticklabels(axes[1,0].get_yticklabels())

    sns.heatmap(heat_matrix_dl[1, :, :].T, annot=heat_matrix_dl[1, :, :].T, fmt=".1f", xticklabels=["SMT (Siblings Competing)", "SMT (Siblings Paired)", "SMT Disabled"], yticklabels=["Hardware", "Software"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    # axes[0,1].set_xlabel("DUs")
    axes[1,1].set_title("Downlink (Shared Cores)")
    axes[1,1].set_ylabel("Execution Modes")
    axes[1,1].set_xticklabels(axes[1,1].get_xticklabels(), rotation=0, ha='center')
    axes[1,1].set_yticklabels(axes[1,1].get_yticklabels())

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/SMTTP.png')

def newLogs():
    latency("new", "new_logs")
    server_energy("new", "new_logs")
    server_cpu_power("new", "new_logs")
    cpu_watts("new", "new_logs")
    cpu_usage("new", "new_logs")
    throughput("new", "new_logs")
    memory_usage("new", "new_logs")
    ldpc_encoding("new", "new_logs")
    ldpc_decoding("new", "new_logs")
    cache("new", "new_logs")
    proc_rate("new", "new_logs")

def smtLogs():
    latency("smt", "smt_logs")
    server_energy("smt", "smt_logs")
    cpu_watts("smt", "smt_logs")
    cpu_usage("smt", "smt_logs")
    throughput("smt", "smt_logs")
    memory_usage("smt", "smt_logs")
    ldpc_encoding("smt", "smt_logs")
    ldpc_decoding("smt", "smt_logs")
    cache("smt", "smt_logs")
    proc_rate("smt", "smt_logs")

def perfLogs():
    latency("perf")
    server_energy("perf")
    cpu_watts("perf")
    cpu_usage("perf")
    throughput("perf")
    uplink_downlink_usage("perf")
    memory_usage("perf")
    ldpc_encoding("perf")
    ldpc_decoding("perf")

def smtsibLogs():
    # latency("smtsib", "smtsib_logs")
    # server_energy("smtsib", "smtsib_logs")
    # cpu_watts("smtsib", "smtsib_logs")
    # cpu_usage("smtsib", "smtsib_logs")
    # throughput("smtsib", "smtsib_logs")
    # memory_usage("smtsib", "smtsib_logs")
    # ldpc_encoding("smtsib", "smtsib_logs")
    # ldpc_decoding("smtsib", "smtsib_logs")
    cache("smtsib", "smtsib_logs")
    # proc_rate("smtsib", "smtsib_logs")
