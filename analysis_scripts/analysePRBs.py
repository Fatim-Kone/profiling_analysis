import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/prb_logs/"
plot_dir = "plots/PRB/"
dus = [1, 2, 4, 6]
prbs = [50, 100, 200, 250]

def median_std_labels(median, std):
    labels = np.empty(median.shape, dtype=object)
    for i in range(median.shape[0]):
        for j in range(median.shape[1]):
            labels[i, j] = f"{median[i, j]:.2f}\n±{std[i, j]:.2f}"
    return labels

def power_labels(power, cpu):
    labels = np.empty(power.shape, dtype=object)
    for i in range(power.shape[0]):
        for j in range(power.shape[1]):
            labels[i, j] = f"{power[i, j]:.2f}\n({cpu[i, j]:.2f})"
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

    heat_matrix_software_ul = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                    
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Average Uplink Latency Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkLatency.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Average Downlink Latency Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DownlinkLatency.png')

def server_energy(): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for prb in prbs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{prb}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{prb}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{prb}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{prb}_shared"] = hw_data[:,0]

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(prbs), len(dus[1:])))


    for k,v in parsed_power["s"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.mean(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.mean(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.mean(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.mean(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Median Power Consumption Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}Power.png')

def cpu_watts():
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for prb in prbs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{prb}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{prb}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{prb}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{prb}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
                    
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)

        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Median CPU Power Consumption Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}CPUPower.png')

def cpu_usage():
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for prb in prbs:
            log_files = [f"{dir}sw{du}_{prb}_cpu.log", f"{dir}hw{du}_{prb}_cpu.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{prb}_cpu_s.log")
                log_files.append(f"{dir}hw{du}_{prb}_cpu_s.log")
            for log_file in log_files:
                with open(log_file, 'r') as f:
                        i = 0
                        off_cpu = 0
                        accum_cpu = 0
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

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_off = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_off = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_off = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_off = np.zeros((len(prbs), len(dus[1:])))


    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(np.array(v)[:,0])
                    heat_matrix_software_s_off[i, j] = np.median(np.array(v)[:,1])
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(np.array(v)[:,0])
                heat_matrix_software_off[i, j] = np.median(np.array(v)[:,1])

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(np.array(v)[:,0])
                    heat_matrix_hardware_s_off[i, j] = np.median(np.array(v)[:,1])
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(np.array(v)[:,0])
                heat_matrix_hardware_off[i, j] = np.median(np.array(v)[:,1])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software, annot=power_labels(heat_matrix_software, heat_matrix_software_off), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=power_labels(heat_matrix_software_s, heat_matrix_software_s_off), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=power_labels(heat_matrix_hardware, heat_matrix_hardware_off), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=power_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_off), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}CPUUsage.png')

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

    heat_matrix_software_ul = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                                    
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
                    

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkTP.png')


    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DownlinkTP.png')    

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

    
    heat_matrix_software_ul = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in usage.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Median Uplink CPU Usage Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkUsage.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Median Downlink CPU Usage Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DownlinkUsage.png')  

def memory_usage():
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for prb in prbs:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_mem.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{prb}"] = sw_data
            parsed_mem["h"][f"hw{du}_{prb}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{prb}_mem_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{prb}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"{dir}sw{du}_{prb}_shared"] = sw_data
                parsed_mem["h"][f"{dir}hw{du}_{prb}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)   
                    with open(f"{dir}/mem_sw{du}_{prb}_s.log") as f:
                        total_mem = int(f.readline())     
                    heat_matrix_software_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_software_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)   
                with open(f"{dir}/mem_sw{du}_{prb}.log") as f:
                        total_mem = int(f.readline())     
                heat_matrix_software[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_software_std[i, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    with open(f"{dir}/mem_hw{du}_{prb}_s.log") as f:
                        total_mem = int(f.readline())    
                    heat_matrix_hardware_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_hardware_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            prb = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb = int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                with open(f"{dir}/mem_hw{du}_{prb}.log") as f:
                        total_mem = int(f.readline())    
                heat_matrix_hardware[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_hardware_std[i, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Median Mem Usage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Median Memory Usage Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}MemUsage.png')

def ldpc_encoding():
    enc_latency = defaultdict()
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals) 
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Encoding and Rate Matching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Encoding and Rate Matching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Average LDPC Encoder and Rate Matching Latency Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}EncoderLatency.png')

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

    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals)
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)

        else:
            if "_s" in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=True, fmt=".2f", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Decoding and Rate Dematching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_s, annot=True, fmt=".2f", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware, annot=True, fmt=".2f", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Decoding and Rate Dematching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=True, fmt=".2f", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.suptitle("Average LDPC Decoder and Rate Dematching Latency Varying PRBS and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DecoderLatency.png')

def cache():
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for prb in prbs:
            log_files = [f"{dir}sw{du}_{prb}_cache.log", f"{dir}hw{du}_{prb}_cache.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{prb}_cache_s.log")
                log_files.append(f"{dir}hw{du}_{prb}_cache_s.log")
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


    heat_matrix_software = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_llc = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_llc = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_llc = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_llc = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_std_llc = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_std_llc = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_s_std_llc = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_s_std_llc = np.zeros((len(prbs), len(dus[1:])))

    for k,v in parsed_cache["s"].items():
        if "_shared" in k:
                du = None
                prb =None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb =int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v["L1"])
                    heat_matrix_software_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_software_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_software_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            prb =None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb =int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v["L1"])
                heat_matrix_software_std[i, j] = np.std(v["L1"])
                heat_matrix_software_llc[i, j] = np.median(v["LLC"])
                heat_matrix_software_std_llc[i, j] = np.std(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_shared" in k:
                du = None
                prb =None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb =int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v["L1"])
                    heat_matrix_hardware_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_hardware_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_hardware_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            prb =None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    prb =int(p)
            
            if du in dus and prb in prbs:
                i = prbs.index(prb)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v["L1"])
                heat_matrix_hardware_std[i, j] = np.std(v["L1"])
                heat_matrix_hardware_llc[i, j] = np.median(v["LLC"])
                heat_matrix_hardware_std_llc[i, j] = np.std(v["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Software L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Software L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_software_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Software LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_software_s_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Software LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"PRBs")

    plt.suptitle(f"Software Cache Hit Ratio Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}SoftwareCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Hardware L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Hardware L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_s_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"PRBs")

    plt.suptitle(f"Hardware Cache Hit Ratio Varying PRBs and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}HardwareCache.png')

def noks():
    noks_rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            noks_rate[k]["dl"] = [e["dl_nok"] / (e["dl_nok"] + e["dl_ok"]) *100 for e in entry["metrics_cell"]]
            noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            noks_rate[k]["dl"] = [e["dl_nok"]/ (e["dl_nok"] + e["dl_ok"]) *100  for e in entry["metrics_cell"]]
            noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    heat_matrix_software_ul = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(prbs), len(dus[1:])))

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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                    
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
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
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkBLER.png')


    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("PRBs")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DownlinkBLER.png')

def proc_rate():
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    with open(f"{dir}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(prbs), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(prbs), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(prbs), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(prbs), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(prbs), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus[1:] and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                prb = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        prb = int(p)
                
                if du in dus and prb in prbs:
                    i = prbs.index(prb)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["pdsch"])

    
    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd" ,cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}PUSCHRate.png')

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"PRBs")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=prbs,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"PRBs")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}PDSCHRate.png')

# latency()
# server_energy()
# cpu_watts()
# cpu_usage()
# throughput()
# uplink_downlink_usage()
# memory_usage()
# ldpc_encoding()
# ldpc_decoding()
# proc_rate()
# noks()
# cache()