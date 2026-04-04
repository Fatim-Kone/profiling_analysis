import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/iter_logs/"
dus = [1, 2, 4, 6]
iters = [2, 4, 6, 8, 10]

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

    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                            iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                            iter = int(p)
                    
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/UplinkLatency.png')


    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/DownlinkLatency.png')

def server_energy(): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for iter in iters:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{iter}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{iter}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{iter}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{iter}_shared"] = hw_data[:,0]

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))


    for k,v in parsed_power["s"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                         iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median Power Consumption Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/Power.png')

def cpu_watts():
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for iter in iters:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{iter}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{iter}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{iter}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{iter}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
                    
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)

        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median CPU Power Consumption Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/CPUPower.png')

def cpu_usage():
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for iter in iters:
            log_files = [f"{dir}sw{du}_{iter}_cpu.log", f"{dir}hw{du}_{iter}_cpu.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{iter}_cpu_s.log")
                log_files.append(f"{dir}hw{du}_{iter}_cpu_s.log")
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

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))


    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median CPU Usage Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/CPUUsage.png')

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

    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                                    
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"]) 
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"]) 
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
                    

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median Uplink Throughput Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/UplinkTP.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median Downlink Throughput Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/DownlinkTP.png')    

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

    
    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in usage.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median Uplink CPU Usage Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/UplinkUsage.png')


    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Median Downlink CPU Usage Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/DownlinkUsage.png')  

def memory_usage():
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for iter in iters:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_mem.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{iter}"] = sw_data
            parsed_mem["h"][f"hw{du}_{iter}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_mem_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"{dir}sw{du}_{iter}_shared"] = sw_data
                parsed_mem["h"][f"{dir}hw{du}_{iter}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)  
                    with open(f"{dir}/mem_sw{du}_{iter}_s.log") as f:
                        total_mem = int(f.readline())   
                    heat_matrix_software_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_software_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                with open(f"{dir}/mem_sw{du}_{iter}.log") as f:
                        total_mem = int(f.readline()) 
                heat_matrix_software[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_software_std[i, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    with open(f"{dir}/mem_hw{du}_{iter}_s.log") as f:
                        total_mem = int(f.readline()) 
                    heat_matrix_hardware_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_hardware_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                with open(f"{dir}/mem_hw{du}_{iter}.log") as f:
                        total_mem = int(f.readline()) 
                heat_matrix_hardware[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_hardware_std[i, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 6))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/MemUsage.png')

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
                enc_latency[k] = [e["encoder"]["avg_latency"] - e["mod"]["avg_latency"] - e["scrambling"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] - e["mod"]["avg_latency"] - e["scrambling"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals) 
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Encoding and Rate Matching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Encoding and Rate Matching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.suptitle("Average LDPC Encoder and Rate Matching Latency Varying Decoder Iterations and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/EncoderLatency.png')

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

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.mean(vals)
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.mean(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.mean(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.mean(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Decoding and Rate Dematching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Decoding and Rate Dematching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Iter/DecoderLatency.png')

def cache():
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for iter in iters:
            log_files = [f"{dir}sw{du}_{iter}_cache.log", f"{dir}hw{du}_{iter}_cache.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{iter}_cache_s.log")
                log_files.append(f"{dir}hw{du}_{iter}_cache_s.log")
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


    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_llc = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_llc = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_llc = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_llc = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_std_llc = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_std_llc = np.zeros((len(iters), len(dus)))

    heat_matrix_software_s_std_llc = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_s_std_llc = np.zeros((len(iters), len(dus[1:])))

    for k,v in parsed_cache["s"].items():
        if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v["L1"])
                    heat_matrix_software_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_software_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_software_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v["L1"])
                heat_matrix_software_std[i, j] = np.std(v["L1"])
                heat_matrix_software_llc[i, j] = np.median(v["LLC"])
                heat_matrix_software_std_llc[i, j] = np.std(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v["L1"])
                    heat_matrix_hardware_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_hardware_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_hardware_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v["L1"])
                heat_matrix_hardware_std[i, j] = np.std(v["L1"])
                heat_matrix_hardware_llc[i, j] = np.median(v["LLC"])
                heat_matrix_hardware_std_llc[i, j] = np.std(v["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software L1 Cache Hit Rate")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software L1 Cache Hit Rate (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_software_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Software LLC Cache Hit Rate")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_software_s_llc, annot=median_std_labels(heat_matrix_software_s_llc, heat_matrix_software_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Software LLC Cache Hit Rate (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/SoftwareCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(12, 6))
    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Hardware L1 Cache Hit Rate")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Hardware L1 Cache Hit Rate (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LLC Cache Hit Rate")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_s_llc, annot=median_std_labels(heat_matrix_hardware_s_llc, heat_matrix_hardware_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Cache Hit Rate (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LLC Cache Hit Rate (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/HardwareCache.png')

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

    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)
                    print("here", np.mean(vals["pusch"]))
                    heat_matrix_software_ul[i, j] = np.mean(vals["pusch"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)

                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)  
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["pusch"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["pdsch"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["pdsch"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/PUSCHRate.png')
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/PDSCHRate.png')

def server_cpu_power():
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for iter in iters:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{iter}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{iter}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{iter}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{iter}_shared"] = hw_data[:,0]
    
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for iter in iters:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{iter}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{iter}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{iter}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{iter}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{iter}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{iter}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware = np.zeros((len(iters), len(dus)))

    heat_matrix_software_cpu = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_cpu = np.zeros((len(iters), len(dus)))

    for k,v in parsed_power["s"].items():
        if "_shared" not in k:   
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.mean(v)

    for k,v in parsed_power["h"].items():
        if "_shared" not in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.mean(v)

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" not in k:
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_software_cpu[i, j] = np.mean(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" not in k:  
            du = None
            iter = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    iter = int(p)
            
            if du in dus and iter in iters:
                i = iters.index(iter)  
                j = dus.index(du)    
                heat_matrix_hardware_cpu[i, j] = np.mean(v)
    

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software, annot=power_labels(heat_matrix_software, heat_matrix_software_cpu), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0])
    axes[0].set_title("Software")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware, annot=power_labels(heat_matrix_hardware, heat_matrix_hardware_cpu), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1])
    axes[1].set_title("Hardware")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/IterPowerComparison.png')

def uldltp():
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

    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                                    
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["ul"]) 
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_ul, annot=heat_matrix_software_ul, fmt=".1f", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=heat_matrix_software_ul_s, fmt=".1f", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl, annot=heat_matrix_software_dl, fmt=".1f", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Software Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=heat_matrix_software_dl_s, fmt=".1f", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Software Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/IterULDLTP.png')

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

    heat_matrix_software_ul = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(iters), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(iters), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(iters), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(iters), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(iters), len(dus[1:])))

    for k, vals in noks_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                    
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus[1:] and iter in iters:
                    i = iters.index(iter)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                iter = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        iter = int(p)
                
                if du in dus and iter in iters:
                    i = iters.index(iter)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.mean(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.mean(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd" ,cbar_kws={'label': 'BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Uplink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Uplink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Uplink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Uplink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/UplinkBLER.png')


    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software Downlink")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software Downlink (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware Downlink")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Decoder Iterations")

    sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=iters,
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware Downlink (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Decoder Iterations")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Iter/DownlinkBLER.png')


latency()
server_energy()
cpu_watts()
cpu_usage()
throughput()
memory_usage()
ldpc_encoding()
ldpc_decoding()
cache()

proc_rate()
cache()

ldpc_decoding()
server_cpu_power()
uldltp()
noks()