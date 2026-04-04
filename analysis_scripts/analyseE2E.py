import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/e2e_logs/"
plot_dir = "/home/fatim/fatim/plots/e2e/"
dus = [1, 2, 4, 6]
modes = ["ul", "dl"]

def mean_std_labels(mean, std):
    labels = np.empty(mean.shape, dtype=object)
    for i in range(mean.shape[0]):
        for j in range(mean.shape[1]):
            labels[i, j] = f"{int(mean[i, j])}\n±{int(std[i, j])}"
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

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkLatency.png')

def server_energy(): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in modes:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{m}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{m}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{m}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{m}_shared"] = hw_data[:,0]
    
    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in parsed_power["s"].items():
        if "_shared" in k:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                    m = p
            
            if du in dus[1:] and m in modes:
                i = modes.index(m)  
                j = dus[1:].index(du)
                if "ul" in k:  
                    heat_matrix_ul_s[0, j] = np.mean(vals)
                    heat_matrix_ul_s_std[0, j] = np.std(vals)
                else:
                    heat_matrix_dl_s[0, j] = np.mean(vals)
                    heat_matrix_dl_s_std[0, j] = np.std(vals)
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                    m = p
                
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(vals)
                    heat_matrix_ul_std[0, j] = np.std(vals)
                else:
                    heat_matrix_dl[0, j] = np.mean(vals)
                    heat_matrix_dl_std[0, j] = np.std(vals)

        for k, vals in parsed_power["h"].items():
            if "_shared" in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals)
                        heat_matrix_ul_s_std[1, j] = np.std(vals)
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals)
                        heat_matrix_dl_s_std[1, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals)
                        heat_matrix_ul_std[1, j] = np.std(vals)
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals)
                        heat_matrix_dl_std[1, j] = np.std(vals)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Power Consumption")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Power Consumption (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Power Consumption")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Power Consumption (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}Power.png')

def cpu_watts():
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in modes:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{m}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{m}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{m}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{m}_shared"] = hw_data

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in parsed_power_cpu["s"].items():
        if "_shared" in k:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p in modes:
                    m = p
            
            if du in dus[1:] and m in modes:
                i = modes.index(m)  
                j = dus[1:].index(du)
                if "ul" in k: 
                    heat_matrix_ul_s[0, j] = np.mean(vals)
                    heat_matrix_ul_s_std[0, j] = np.std(vals)
                else:
                    heat_matrix_dl_s[0, j] = np.mean(vals)
                    heat_matrix_dl_s_std[0, j] = np.std(vals)
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                    m = p
                
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(vals)
                    heat_matrix_ul_std[0, j] = np.std(vals)
                else:
                    heat_matrix_dl[0, j] = np.mean(vals)
                    heat_matrix_dl_std[0, j] = np.std(vals)

        for k, vals in parsed_power_cpu["h"].items():
            if "_shared" in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals)
                        heat_matrix_ul_s_std[1, j] = np.std(vals)
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals)
                        heat_matrix_dl_s_std[1, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals)
                        heat_matrix_ul_std[1, j] = np.std(vals)
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals)
                        heat_matrix_dl_std[1, j] = np.std(vals)
        
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink CPU Power Consumption")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink CPU Power Consumption (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink CPU Power Consumption")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink CPU Power Consumption (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}CPUPower.png')

def cpu_usage():
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for m in modes:
            log_files = [f"{dir}sw{du}_{m}_cpu.log", f"{dir}hw{du}_{m}_cpu.log"]
            if du > 1:
                log_files.append(f"{dir}sw{du}_{m}_cpu_s.log")
                log_files.append(f"{dir}hw{du}_{m}_cpu_s.log")
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

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_off = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_off = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_off = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_off = np.zeros((len(modes), len(dus[1:])))


    for k, v in parsed_cpu["s"].items():
        if "_s." in k:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                    m = p
            
            if du in dus[1:] and m in modes:
                i = modes.index(m)  
                j = dus[1:].index(du)
                if "ul" in k:    
                    heat_matrix_ul_s[0, j] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_s_off[0, j] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_dl_s[0, j] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_s_off[0, j] = np.mean(np.array(v)[:,1])
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                    m = p
                
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_off[0, j] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_dl[0, j] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_off[0, j] = np.mean(np.array(v)[:,1])

        for k, v in parsed_cpu["h"].items():
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_s_off[1, j] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_s_off[1, j] = np.mean(np.array(v)[:,1])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_off[1, j] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_dl[1, j] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_off[1, j] = np.mean(np.array(v)[:,1])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=power_labels(heat_matrix_ul, heat_matrix_ul_off), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink CPU Usage")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=power_labels(heat_matrix_ul_s, heat_matrix_ul_s_off), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink CPU Usage (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=power_labels(heat_matrix_dl, heat_matrix_dl_off), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink CPU Usage")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=power_labels(heat_matrix_dl_s, heat_matrix_dl_s_off), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink CPU Usage (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

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

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = int(np.mean(vals["ul"]))
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = int(np.mean(vals["dl"]))
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = int(np.mean(vals["ul"]))
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = int(np.mean(vals["dl"]))
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = int(np.mean(vals["ul"]))
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = int(np.mean(vals["dl"]))
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = int(np.mean(vals["ul"]))
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = int(np.mean(vals["dl"]))
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Throughput (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}TP.png')
   
def memory_usage():
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for m in modes:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_mem.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{m}"] = sw_data
            parsed_mem["h"][f"hw{du}_{m}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_mem_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"{dir}sw{du}_{m}_shared"] = sw_data
                parsed_mem["h"][f"{dir}hw{du}_{m}_shared"] = hw_data

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)   
                    with open(f"{dir}/mem_sw{du}_{m}_s.log") as f:
                        total_mem = int(f.readline())     
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(total_mem - v) / 1024
                        heat_matrix_ul_s_std[0, j] = np.std(total_mem - v) / 1024
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(total_mem - v) / 1024
                        heat_matrix_dl_s_std[0, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)   
                with open(f"{dir}/mem_sw{du}_{m}.log") as f:
                        total_mem = int(f.readline())     
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(total_mem - v) / 1024
                    heat_matrix_ul_std[0, j] = np.std(total_mem - v) / 1024
                else:
                    heat_matrix_dl[0, j] = np.mean(total_mem - v) / 1024
                    heat_matrix_dl_std[0, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    with open(f"{dir}/mem_hw{du}_{m}_s.log") as f:
                        total_mem = int(f.readline())    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(total_mem - v) / 1024
                        heat_matrix_ul_s_std[1, j] = np.std(total_mem - v) / 1024
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(total_mem - v) / 1024
                        heat_matrix_dl_s_std[1, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    m = int(p)
            
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                with open(f"{dir}/mem_hw{du}_{m}.log") as f:
                        total_mem = int(f.readline())    
                if "ul" in k:    
                    heat_matrix_ul[1, j] = np.mean(total_mem - v) / 1024
                    heat_matrix_ul_std[1, j] = np.std(total_mem - v) / 1024
                else:
                    heat_matrix_dl[1, j] = np.mean(total_mem - v) / 1024
                    heat_matrix_dl_std[1, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Memory Usage")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Memory Usage (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Memory Usage")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Memory Usage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Memory Usage (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

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

    heat_matrix_dl = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)   
                    if "dl" in k: 
                        heat_matrix_dl_s[0, j] = np.mean(vals) 
                        heat_matrix_dl_s_std[0, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "dl" in k: 
                        heat_matrix_dl[0, j] = np.mean(vals) 
                        heat_matrix_dl_std[0, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "dl" in k: 
                        heat_matrix_dl_s[1, j] = np.mean(vals) 
                        heat_matrix_dl_s_std[1, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "dl" in k: 
                        heat_matrix_dl[1, j] = np.mean(vals) 
                        heat_matrix_dl_std[1, j] = np.std(vals)

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0])
    axes[0].set_title("LDPC Encoding and Rate Matching Latency")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1])
    axes[1].set_title("LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Execution Modes")

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

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)   
                    if "ul" in k: 
                        heat_matrix_ul_s[0, j] = np.mean(vals) 
                        heat_matrix_ul_s_std[0, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k: 
                        heat_matrix_ul[0, j] = np.mean(vals) 
                        heat_matrix_ul_std[0, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k: 
                        heat_matrix_ul_s[1, j] = np.mean(vals) 
                        heat_matrix_ul_s_std[1, j] = np.std(vals)
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k: 
                        heat_matrix_ul[1, j] = np.mean(vals) 
                        heat_matrix_ul_std[1, j] = np.std(vals)

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0])
    axes[0].set_title("LDPC Decoding and Rate Dematching Latency")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1])
    axes[1].set_title("LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DecoderLatency.png')

def cache():
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for m in modes:
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

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_llc = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_llc = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_llc = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_llc = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std_llc = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std_llc = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std_llc = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std_llc = np.zeros((len(modes), len(dus[1:])))

    for k,vals in parsed_cache["s"].items():
        if "_s." in k:
                du = None
                m =None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif  p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["L1"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["L1"])
                        heat_matrix_ul_s_llc[0, j] = np.mean(vals["LLC"])
                        heat_matrix_ul_s_std_llc[0, j] = np.std(vals["LLC"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["L1"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["L1"])
                        heat_matrix_dl_s_llc[0, j] = np.mean(vals["LLC"])
                        heat_matrix_dl_s_std_llc[0, j] = np.std(vals["LLC"])
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif  p  in modes:
                        m = p
            
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(vals["L1"])
                    heat_matrix_ul_std[0, j] = np.std(vals["L1"])
                    heat_matrix_ul_llc[0, j] = np.mean(vals["LLC"])
                    heat_matrix_ul_std_llc[0, j] = np.std(vals["LLC"])
                else:
                    heat_matrix_dl[0, j] = np.mean(vals["L1"])
                    heat_matrix_dl_std[0, j] = np.std(vals["L1"])
                    heat_matrix_dl_llc[0, j] = np.mean(vals["LLC"])
                    heat_matrix_dl_std_llc[0, j] = np.std(vals["LLC"])

    for k,vals in parsed_cache["h"].items():
        if "_s." in k:
                du = None
                m =None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif  p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["L1"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["L1"])
                        heat_matrix_ul_s_llc[1, j] = np.mean(vals["LLC"])
                        heat_matrix_ul_s_std_llc[1, j] = np.std(vals["LLC"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["L1"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["L1"])
                        heat_matrix_dl_s_llc[1, j] = np.mean(vals["LLC"])
                        heat_matrix_dl_s_std_llc[1, j] = np.std(vals["LLC"])
        else:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif  p  in modes:
                        m = p
            
            if du in dus and m in modes:
                i = modes.index(m)  
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[1, j] = np.mean(vals["L1"])
                    heat_matrix_ul_std[1, j] = np.std(vals["L1"])
                    heat_matrix_ul_llc[1, j] = np.mean(vals["LLC"])
                    heat_matrix_ul_std_llc[1, j] = np.std(vals["LLC"])
                else:
                    heat_matrix_dl[1, j] = np.mean(vals["L1"])
                    heat_matrix_dl_std[1, j] = np.std(vals["L1"])
                    heat_matrix_dl_llc[1, j] = np.mean(vals["LLC"])
                    heat_matrix_dl_std_llc[1, j] = np.std(vals["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_ul_llc, annot=mean_std_labels(heat_matrix_ul_llc, heat_matrix_ul_std_llc), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Uplink LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_ul_s_llc, annot=mean_std_labels(heat_matrix_ul_s_llc, heat_matrix_ul_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Uplink LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}UplinkCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Downlink L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Downlink L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_dl_llc, annot=mean_std_labels(heat_matrix_dl_llc, heat_matrix_dl_std_llc), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Execution Modes")

    sns.heatmap(heat_matrix_dl_s_llc, annot=mean_std_labels(heat_matrix_dl_s_llc, heat_matrix_dl_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}DownlinkCache.png')

def noks():
    noks_rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "dl" in k:
                noks_rate[k]["dl"] = [e["dl_nok"] / (e["dl_nok"] + e["dl_ok"]) *100 for e in entry["metrics_cell"]]
            else:
                noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "dl" in k:
                noks_rate[k]["dl"] = [e["dl_nok"]/ (e["dl_nok"] + e["dl_ok"]) *100  for e in entry["metrics_cell"]]
            else:
                noks_rate[k]["ul"] = [e["ul_nok"] / (e["ul_nok"] + e["ul_ok"]) *100 for e in entry["metrics_cell"]]

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in noks_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'BLER (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'BLER (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'BLER (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}BLER.png')

def proc_rate():
    proc_rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["ul"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["ul"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("PUSCH")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("PUSCH (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("PDSCH Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("PDSCH Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}Rate.png')

def server_cpu_power():
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in modes:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{m}"] = sw_data[:,0]
            parsed_power["h"][f"hw{du}_{m}"] = hw_data[:,0]
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{m}_shared"] = sw_data[:,0]
                parsed_power["h"][f"hw{du}_{m}_shared"] = hw_data[:,0]
    
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for m in modes:
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{m}"] = sw_data
            parsed_power_cpu["h"][f"hw{du}_{m}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy_s.csv", delimiter=',')
                hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{m}_shared"] = sw_data
                parsed_power_cpu["h"][f"hw{du}_{m}_shared"] = hw_data

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_cpu = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_cpu = np.zeros((len(modes), len(dus)))

    for k,vals in parsed_power["s"].items():
        if "_shared" not in k:   
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                        m = p
            
            if du in dus and m in modes:
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul[0, j] = np.mean(vals)
                else:
                    heat_matrix_dl[0, j] = np.mean(vals)

    for k,vals in parsed_power["h"].items():
        if "_shared" not in k:
                du = None
                m = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p in modes:
                        m = p
                
                if du in dus and m in modes:
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals)
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals)

    for k,vals in parsed_power_cpu["s"].items():
        if "_shared" not in k:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p  in modes:
                        m = p
            
            if du in dus and m in modes:
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul_cpu[0, j] = np.mean(vals)
                else:
                    heat_matrix_dl_cpu[0, j] = np.mean(vals)

    for k,vals in parsed_power_cpu["h"].items():
        if "_shared" not in k:  
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p  in modes:
                        m = p
            
            if du in dus and m in modes:
                j = dus.index(du)    
                if "ul" in k:    
                    heat_matrix_ul_cpu[1, j] = np.mean(vals)
                else:
                    heat_matrix_dl_cpu[1, j] = np.mean(vals)
    

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_ul, annot=power_labels(heat_matrix_ul, heat_matrix_ul_cpu), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0])
    axes[0].set_title("Uplink")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=power_labels(heat_matrix_dl, heat_matrix_dl_cpu), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1])
    axes[1].set_title("Downlink")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}/PowerComparison.png')

def mac_latency():
    latency = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "ul" in k:
                latency[k]["ul"] = [e["wall_latency"] for e in entry["upper_du_metrics"] if "wall_latency" in e]
            else:
                latency[k]["dl"] = [e["wall_latency"] for e in entry["upper_du_metrics"] if "wall_latency" in e]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "ul" in k:
                latency[k]["ul"] = [e["wall_latency"] for e in entry["upper_du_metrics"] if "wall_latency" in e]
            else:
                latency[k]["dl"] = [e["wall_latency"] for e in entry["upper_du_metrics"] if "wall_latency" in e]

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Uplink Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Downlink Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}MACLatency.png')

def rlc_rate():
    rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "ul" in k:
                rate[k]["ul"] = [e["rx_rate"] for e in entry["upper_du_metrics"] if "rx_rate" in e.keys() and e["rx_rate"] != 0]
            else:
                rate[k]["dl"] = [e["tx_rate"] for e in entry["upper_du_metrics"] if "tx_rate" in e.keys() and e["tx_rate"] != 0]

    with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "ul" in k:
                rate[k]["ul"] = [e["rx_rate"] for e in entry["upper_du_metrics"] if "rx_rate" in e.keys() and e["rx_rate"] != 0]
            else:
                rate[k]["dl"] = [e["tx_rate"] for e in entry["upper_du_metrics"] if "tx_rate" in e.keys() and e["tx_rate"] != 0]

    heat_matrix_ul = np.zeros((len(modes), len(dus)))
    heat_matrix_dl = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s = np.zeros((len(modes), len(dus[1:])))

    heat_matrix_ul_std = np.zeros((len(modes), len(dus)))
    heat_matrix_dl_std = np.zeros((len(modes), len(dus)))

    heat_matrix_ul_s_std = np.zeros((len(modes), len(dus[1:])))
    heat_matrix_dl_s_std = np.zeros((len(modes), len(dus[1:])))
    for k, vals in rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)
                    if "ul" in k:    
                        heat_matrix_ul_s[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[0, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                    
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du)    
                    if "ul" in k:    
                        heat_matrix_ul[0, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[0, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[0, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[0, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus[1:] and m in modes:
                    i = modes.index(m)  
                    j = dus[1:].index(du)    
                    if "ul" in k:    
                        heat_matrix_ul_s[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_s_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl_s[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_s_std[1, j] = np.std(vals["dl"])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p  in modes:
                        m = p
                
                if du in dus and m in modes:
                    i = modes.index(m)  
                    j = dus.index(du) 
                    if "ul" in k:    
                        heat_matrix_ul[1, j] = np.mean(vals["ul"])
                        heat_matrix_ul_std[1, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_dl[1, j] = np.mean(vals["dl"])
                        heat_matrix_dl_std[1, j] = np.std(vals["dl"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=mean_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,0])
    axes[0,0].set_title("RX Rate")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_ul_s, annot=mean_std_labels(heat_matrix_ul_s, heat_matrix_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[0,1])
    axes[0,1].set_title("RX Rate (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=mean_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=dus, yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[1,0])
    axes[1,0].set_title("TX Rate")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl_s, annot=mean_std_labels(heat_matrix_dl_s, heat_matrix_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd", cbar_kws={'label': 'Rate (Mbps)'}, ax=axes[1,1])
    axes[1,1].set_title("TX Rate (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{plot_dir}RLCRate.png')

# latency()
# server_energy()
# cpu_watts()
throughput()
# memory_usage()
# ldpc_encoding()
# ldpc_decoding()
# proc_rate()
# noks()
# cache()
# server_cpu_power()
# mac_latency()
# rlc_rate()