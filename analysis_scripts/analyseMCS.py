import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/mcs_logs/"
dus = [1, 2, 4, 6]
mcs = [0, 4, 5, 10, 11, 19, 20, 27]
ticks = ["QPSK(0)", "QPSK(2)", "16QAM(5)", "16QAM(10)", "64QAM(11)", "64QAM(19)", "256QAM(20)", "256QAM(27)"]

def median_std_labels(median, std):
    labels = np.empty(median.shape, dtype=object)
    for i in range(median.shape[0]):
        for j in range(median.shape[1]):
            labels[i, j] = f"{median[i, j]:.2f}\n±{std[i, j]:.2f}"
    return labels

def latency():
    latency = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(16, 6))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/UplinkLatency.png')


    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/DownlinkLatency.png')

def server_energy(): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in mcs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{m}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{m}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{m}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{m}_shared"] = hw_data[:,0]

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))


    for k,v in parsed_power["s"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.suptitle("Median Power Consumption Varying MCS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/Power.png')

def cpu_watts():
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in mcs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{m}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{m}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{m}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{m}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
                    
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                        m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)

        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.suptitle("Median CPU Power Consumption Varying MCS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/CPUPower.png')

def cpu_usage():
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for m in mcs:
            log_files = [f"{dir}sw{du}_{m}_cpu.log", f"{dir}hw{du}_{m}_cpu.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{m}_cpu_s.log")
                log_files.append(f"{dir}hw{du}_{m}_cpu_s.log")
            for log_file in log_files:
                with open(log_file, 'r') as f:
                        i = 0
                        accum_cpu = 0
                        for line in f:
                            gnb = i % du
                            line = line.strip()
                            split = line.split()
                            if gnb == 0:
                                if "sw" in log_file:
                                    parsed_cpu["s"][log_file].append(accum_cpu)
                                else:    
                                    parsed_cpu["h"][log_file].append(accum_cpu) 
                                accum_cpu = float(split[7])
                            else:
                                accum_cpu += float(split[7])
                            i += 1 

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))


    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 8))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/CPUUsage.png')

def throughput():
    tp = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    heat_matrix_software_ul = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                                    
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["ul"]) 
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
                    

    fig, axes = plt.subplots(2, 2, figsize=(16, 8))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/UplinkTP.png')


    fig, axes = plt.subplots(2, 2, figsize=(16, 8))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/DownlinkTP.png')    

def uplink_downlink_usage():
    usage = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"]= [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"] = [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    
    heat_matrix_software_ul = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in usage.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.suptitle("Median Uplink CPU Usage Varying MCS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/UplinkUsage.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.suptitle("Median Downlink CPU Usage Varying MCS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/DownlinkUsage.png')  

def memory_usage():
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for m in mcs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_mem.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{m}"] = sw_data
            parsed_mem["h"][f"hw{du}_{m}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_mem_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"{dir}sw{du}_{m}_shared"] = sw_data
                parsed_mem["h"][f"{dir}hw{du}_{m}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du) 
                    with open(f"{dir}/mem_sw{du}_{m}_s.log") as f:
                        total_mem = int(f.readline())    
                    heat_matrix_software_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_software_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du) 
                with open(f"{dir}/mem_sw{du}_{m}.log") as f:
                        total_mem = int(f.readline())    
                heat_matrix_software[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_software_std[i, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)   
                    with open(f"{dir}/mem_hw{du}_{m}_s.log") as f:
                        total_mem = int(f.readline())  
                    heat_matrix_hardware_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_hardware_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                with open(f"{dir}/mem_hw{du}_{m}.log") as f:
                        total_mem = int(f.readline()) 
                heat_matrix_hardware[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_hardware_std[i, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 6))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.suptitle("Median Memory Usage Varying MCS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/MemUsage.png')

def ldpc_encoding():
    enc_latency = defaultdict()
    dec_latency = defaultdict()
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software_enc = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_enc = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dec = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dec = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_enc[i, j] = np.mean(vals) 

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_enc[i, j] = np.mean(vals)

        for k, vals in dec_latency.items():
            if "sw" in k:
                if "_s." in k:
                    du = None
                    m = None
                    log = k.split("/")[-1]
                    parts = log.split("_")
                    for p in parts:
                        if p.startswith("sw"):
                            du = int(p[2:])
                        elif p.isdigit():
                            m = int(p)
                    
                    if du in dus[1:] and m in mcs:
                        i = mcs.index(m)  
                        j = dus[1:].index(du)    
                        heat_matrix_software_dec[i, j] = np.mean(vals) 

            else:
                if "_s." in k:
                    du = None
                    m = None
                    log = k.split("/")[-1]
                    parts = log.split("_")
                    for p in parts:
                        if p.startswith("hw"):
                            du = int(p[2:])
                        elif p.isdigit():
                            m = int(p)
                    
                    if du in dus[1:] and m in mcs:
                        i = mcs.index(m)  
                        j = dus[1:].index(du)    
                        heat_matrix_hardware_dec[i, j] = np.mean(vals)
            

    fig, axes = plt.subplots(2, 2, figsize=(14, 6))
    sns.heatmap(heat_matrix_software_enc, annot=heat_matrix_software_enc, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Encoding and Rate Matching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_enc, annot=heat_matrix_hardware_enc, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Encoding and Rate Matching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_dec, annot=heat_matrix_software_dec, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Decoding and Rate Dematching Latency")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dec, annot=heat_matrix_hardware_dec, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Decoding and Rate Dematching Latency")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/plots/MCS/EncDecLatency.png')

def ldpc_decoding():
    dec_latency = defaultdict()
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals)
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)

                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(16, 8))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Decoding and Rate Dematching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Decoding and Rate Dematching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/DecoderLatency.png')

def modualtion():
    mod_latency = defaultdict()
    demod_latency = defaultdict()
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            mod_latency[k] = [e["mod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]
            demod_latency[k] = [e["demod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            mod_latency[k] = [e["mod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  
            demod_latency[k] = [e["demod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_de = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_de = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in mod_latency.items():
        if "sw" in k:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software[i, j] = np.mean(vals)
                    
        else:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware[i, j] = np.mean(vals)

    for k, vals in demod_latency.items():
        if "sw" in k:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_de[i, j] = np.mean(vals)
                    
        else:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_de[i, j] = np.mean(vals)
            

    fig, axes = plt.subplots(2, 2, figsize=(14, 6))
    sns.heatmap(heat_matrix_software, annot=heat_matrix_software, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Modulation Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=heat_matrix_hardware, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Modulation Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_de, annot=heat_matrix_software_de, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Demodulation Latency")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_de, annot=heat_matrix_hardware_de, fmt=".1f", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Demodulation Latency")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/plots/MCS/ModDemodLatency.png')

def demodulation():
    demod_latency = defaultdict()
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            demod_latency[k] = [e["demod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            demod_latency[k] = [e["demod"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in demod_latency.items():
        if "sw" in k:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals)
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s" in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(16, 8))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Demodulation Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Demodulation Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Demodulation Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Demodulation Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCS/DemodulationLatency.png')

def cache():
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for m in mcs:
            log_files = [f"{dir}sw{du}_{m}_cache.log", f"{dir}hw{du}_{m}_cache.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{m}_cache_s.log")
                log_files.append(f"{dir}hw{du}_{m}_cache_s.log")
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


    heat_matrix_software = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_llc = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_llc = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_llc = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_llc = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_std_llc = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_std_llc = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_s_std_llc = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_s_std_llc = np.zeros((len(mcs), len(dus[1:])))

    for k,v in parsed_cache["s"].items():
        if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v["L1"])
                    heat_matrix_software_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_software_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_software_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v["L1"])
                heat_matrix_software_std[i, j] = np.std(v["L1"])
                heat_matrix_software_llc[i, j] = np.median(v["LLC"])
                heat_matrix_software_std_llc[i, j] = np.std(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v["L1"])
                    heat_matrix_hardware_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_hardware_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_hardware_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in mcs:
                i = mcs.index(m)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v["L1"])
                heat_matrix_hardware_std[i, j] = np.std(v["L1"])
                heat_matrix_hardware_llc[i, j] = np.median(v["LLC"])
                heat_matrix_hardware_std_llc[i, j] = np.std(v["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Software L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Software L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_software_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Software LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_software_s_llc, annot=median_std_labels(heat_matrix_software_s_llc, heat_matrix_software_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Software LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/MCS/SoftwareCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Hardware L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Hardware L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_hardware_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"MCS")

    sns.heatmap(heat_matrix_hardware_s_llc, annot=median_std_labels(heat_matrix_hardware_s_llc, heat_matrix_hardware_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/MCS/HardwareCache.png')

def proc_rate():
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(mcs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(mcs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(mcs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(mcs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(mcs), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus[1:] and m in mcs:
                    i = mcs.index(m)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        m = int(p)
                
                if du in dus and m in mcs:
                    i = mcs.index(m)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["pdsch"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd" ,cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/MCS/PUSCHRate.png')
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("MCS")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=ticks,
                cmap="YlOrRd", cbar_kws={'label': ' Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("MCS")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/MCS/PDSCHRate.png')

def tp():
    tp = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]
    
    heat_matrix_ul = np.zeros(len(mcs))
    heat_matrix_dl = np.zeros(len(mcs))

    for k, vals in tp.items():
        if "sw" in k:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
                                
            if m in mcs and du == 1:
                i = mcs.index(m)  
                heat_matrix_ul[i] = np.mean(vals["ul"]) 
                heat_matrix_dl[i] = np.mean(vals["dl"])

    fig, axes = plt.subplots(1, 1, figsize=(6, 4))
    axes.plot(ticks, heat_matrix_ul, label="Uplink", color="black")
    axes.plot(ticks, heat_matrix_dl, label="Downlink", color="darkgrey")
    axes.set_xticks(ticks, rotation=20, fontsize=14)
    axes.set_xticklabels(ticks, rotation=20, fontsize=14)
    axes.legend(fontsize=14)
    axes.set_xlabel("MCS", fontsize=14)
    axes.set_ylabel(f"Throughput (Mbps)", fontsize=14)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/MCSTP.png')

# latency()
# server_energy()
# cpu_watts()
# cpu_usage()
# throughput()
# # uplink_downlink_usage()
# # memory_usage()
ldpc_encoding()
# # ldpc_decoding()
modualtion()
# demodulation()
# cache()
# tp()