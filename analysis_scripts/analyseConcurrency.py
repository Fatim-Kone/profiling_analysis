import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/concur_logs/"
dus = [1, 2]
concur = [2, 4, 8, 12, 14]
tick = [2, 4, 8, 12, "No Limit"]
labels =  ["2", "4", "8", "12", "No Limit"]

def median_std_labels(median, std):
    labels = np.empty(median.shape, dtype=object)
    for i in range(median.shape[0]):
        for j in range(median.shape[1]):
            labels[i, j] = f"{median[i, j]:.2f}\n±{std[i, j]:.2f}"
    return labels

def latency(channel):
    latency = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["ul"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])

    if channel == "pusch":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Uplink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Uplink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Uplink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Uplink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle("Average Uplink Latency Varying Concurrent PDSCH and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('/home/fatim/fatim/plots/Concurrency/UplinkLatency.png')
    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Downlink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Downlink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Downlink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Downlink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle("Average Downlink Latency Varying Concurrent PDSCH and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('/home/fatim/fatim/plots/Concurrency/DownlinkLatency.png')

def server_energy(channel): 
    parsed_power = defaultdict(lambda: defaultdict())
    for du in dus:
        for con in concur:
            sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_power.csv", delimiter=',')
            parsed_power["s"][f"sw{du}_{con}"] = sw_data[:,0]
            if con > 0:
                hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_power.csv", delimiter=',')
                parsed_power["h"][f"hw{du}_{con}"] = hw_data[:,0]
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_power_s.csv", delimiter=',')
                parsed_power["s"][f"sw{du}_{con}_shared"] = sw_data[:,0]
                if con > 0:
                    hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_power_s.csv", delimiter=',')
                    parsed_power["h"][f"hw{du}_{con}_shared"] = hw_data[:,0]

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))


    for k,v in parsed_power["s"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power["h"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur[:-1]:
                i = concur[:-1].index(con)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
        
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Median Power Consumption Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurPower.png')

def cpu_watts(channel):
    parsed_power_cpu = defaultdict(lambda: defaultdict())
    for du in dus:
        for con in concur:
            sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"sw{du}_{con}"] = sw_data
            if con > 0:
                hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_energy.csv", delimiter=',')
                parsed_power_cpu["h"][f"hw{du}_{con}"] = hw_data
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_energy_s.csv", delimiter=',')
                parsed_power_cpu["s"][f"sw{du}_{con}_shared"] = sw_data
                if con > 0:
                    hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_energy_s.csv", delimiter=',')
                    parsed_power_cpu["h"][f"hw{du}_{con}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k,v in parsed_power_cpu["s"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
                    
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                        con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_power_cpu["h"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur[:-1]:
                i = concur[:-1].index(con)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)

        
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median Power Consumption (W)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Median CPU Power Consumption Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurCPUPower.png')

def cpu_usage(channel):
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for con in concur:
            log_files = [f"{dir}{channel}/sw{du}_{con}_cpu.log"]
            if con > 0:
                log_files.append(f"{dir}{channel}/hw{du}_{con}_cpu.log")
            if du > 1:
                log_files.append(f"{dir}{channel}/sw{du}_{con}_cpu_s.log")
                if con > 0:
                    log_files.append(f"{dir}{channel}/hw{du}_{con}_cpu_s.log")
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

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))


    for k,v in parsed_cpu["s"].items():
        if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v)
                    heat_matrix_software_s_std[i, j] = np.std(v)
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v)
                heat_matrix_software_std[i, j] = np.std(v)

    for k,v in parsed_cpu["h"].items():
        if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v)
                    heat_matrix_hardware_s_std[i, j] = np.std(v)
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur[:-1]:
                i = concur[:-1].index(con)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v)
                heat_matrix_hardware_std[i, j] = np.std(v)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Median CPU Usage Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurCPUUsage.png')

def throughput(channel):
    tp = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
            tp[k]["ul"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    heat_matrix_software_ul = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in tp.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                                    
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    if channel == "pusch":
                        heat_matrix_software_ul_s[i, j] = np.median(vals["ul"]) 
                        heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                        heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    if channel == "pusch":
                        heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                        heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    else:
                        heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                        heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)   
                    if channel == "pusch": 
                        heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                        heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"]) 
                    else:
                        heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
                        heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus.index(du)    
                    if channel == "pusch": 
                        heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                        heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"]) 
                    else:
                        heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
                        heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])

    if channel == "pusch":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd" ,cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Uplink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Uplink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Uplink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Uplink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle(f"Median Uplink Throughput Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurUplinkTP.png')
    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Downlink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Downlink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Downlink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Downlink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle(f"Median Downlink Throughput Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurDownlinkTP.png')    

def uplink_downlink_usage(channel):
    usage = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"]= [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            usage[k]["dl"] = [e["pdsch_cpu"]["upper_phy_dl"] for e in entry["metrics"]]
            usage[k]["ul"] = [e["pusch_cpu"]["upper_phy_ul"] for e in entry["metrics"]]

    
    heat_matrix_software_ul = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in usage.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_software_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["dl"])

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["dl"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["ul"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["dl"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["ul"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["dl"])
    if channel == "pusch":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Uplink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Uplink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Uplink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Uplink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle(f"Median Uplink CPU Usage Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurUplinkUsage.png')
    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Downlink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Downlink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Downlink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Downlink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle(f"Median Downlink CPU Usage Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurDownlinkUsage.png')  

def memory_usage(channel):
    parsed_mem = defaultdict(lambda: defaultdict(list))
    for du in dus:
        for con in concur:
            sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_mem.csv", delimiter=',')
            parsed_mem["s"][f"sw{du}_{con}"] = sw_data
            if con > 0:
                hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_mem.csv", delimiter=',')
                parsed_mem["h"][f"hw{du}_{con}"] = hw_data
            
            if du > 1:
                sw_data = np.genfromtxt(f"{dir}{channel}/sw{du}_{con}_mem_s.csv", delimiter=',')
                parsed_mem["s"][f"{dir}{channel}/sw{du}_{con}_shared"] = sw_data
                if con > 0:
                    hw_data = np.genfromtxt(f"{dir}{channel}/hw{du}_{con}_mem_s.csv", delimiter=',')
                    parsed_mem["h"][f"{dir}{channel}/hw{du}_{con}_shared"] = hw_data

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k,v in parsed_mem["s"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    with open(f"{dir}{channel}/mem_sw{du}_{con}_s.log") as f:
                        total_mem = int(f.readline())
                    heat_matrix_software_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_software_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)
                with open(f"{dir}{channel}/mem_sw{du}_{con}.log") as f:
                        total_mem = int(f.readline())    
                heat_matrix_software[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_software_std[i, j] = np.std(total_mem - v) / 1024

    for k,v in parsed_mem["h"].items():
        if "_shared" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur[:-1]:
                    i = concur[:-1].index(con)  
                    j = dus[1:].index(du)   
                    with open(f"{dir}{channel}/mem_hw{du}_{con}_s.log") as f:
                        total_mem = int(f.readline()) 
                    heat_matrix_hardware_s[i, j] = np.median(total_mem - v) / 1024
                    heat_matrix_hardware_s_std[i, j] = np.std(total_mem - v) / 1024
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur[:-1]:
                i = concur[:-1].index(con)  
                j = dus.index(du)    
                with open(f"{dir}{channel}/mem_hw{du}_{con}.log") as f:
                        total_mem = int(f.readline())
                heat_matrix_hardware[i, j] = np.median(total_mem - v) / 1024
                heat_matrix_hardware_std[i, j] = np.std(total_mem - v) / 1024
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median MeconUsage (MB)'}, ax=axes[0,0])
    axes[0,0].set_title("Software")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Median MeconUsage (MB)'}, ax=axes[0,1])
    axes[0,1].set_title("Software (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median MeconUsage (MB)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Median MeconUsage (MB)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Median Memory Usage Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurMemUsage.png')

def ldpc_encoding(channel):
    enc_latency = defaultdict()
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] - e["mod"]["avg_latency"] - e["scrambling"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"]]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] - e["mod"]["avg_latency"] - e["scrambling"]["avg_latency"]  for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]  

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in enc_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals) 
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Encoding and Rate Matching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Encoding and Rate Matching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Encoding and Rate Matching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Average LDPC Encoder and Rate Matching Latency Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurEncoderLatency.png')

def ldpc_decoding(channel):
    dec_latency = defaultdict()
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"]]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]

    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in dec_latency.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(vals)
                    heat_matrix_software_s_std[i, j] = np.std(vals)
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_software[i, j] = np.median(vals)
                    heat_matrix_software_std[i, j] = np.std(vals)

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(vals)
                    heat_matrix_hardware_s_std[i, j] = np.std(vals)
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)

                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_hardware[i, j] = np.median(vals)
                    heat_matrix_hardware_std[i, j] = np.std(vals)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,0])
    axes[0,0].set_title("Software LDPC Decoding and Rate Dematching Latency")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0,1])
    axes[0,1].set_title("Software LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LDPC Decoding and Rate Dematching Latency")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LDPC Decoding and Rate Dematching Latency (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Average LDPC Decoder and Rate Dematching Latency Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/ConcurDecoderLatency.png')

def proc_rate(channel):
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["pusch"] = [e["pusch"]["rate"] for e in entry["metrics"]]
            proc_rate[k]["pdsch"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_ul_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_ul_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_dl_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_dl_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_ul_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_ul_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_dl_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_dl_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_software_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_software_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_software_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_software_dl_std[i, j] = np.std(vals["pdsch"])

        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_ul_s[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl_s[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_s_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_s_std[i, j] = np.std(vals["pdsch"])
            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus and con in concur:
                    i = concur.index(con)  
                    j = dus.index(du)    
                    heat_matrix_hardware_ul[i, j] = np.median(vals["pusch"])
                    heat_matrix_hardware_dl[i, j] = np.median(vals["pdsch"])
                    heat_matrix_hardware_ul_std[i, j] = np.std(vals["pusch"])
                    heat_matrix_hardware_dl_std[i, j] = np.std(vals["pdsch"])

    if channel == "pusch":
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_ul, annot=median_std_labels(heat_matrix_software_ul, heat_matrix_software_ul_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd" ,cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Uplink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_ul_s, annot=median_std_labels(heat_matrix_software_ul_s, heat_matrix_software_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Uplink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul, annot=median_std_labels(heat_matrix_hardware_ul, heat_matrix_hardware_ul_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Uplink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_ul_s, annot=median_std_labels(heat_matrix_hardware_ul_s, heat_matrix_hardware_ul_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Uplink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle("Average PUSCH Processing Rate Varying Concurrent PUSCH and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('/home/fatim/fatim/plots/Concurrency/PUSCHRate.png')
    else:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        sns.heatmap(heat_matrix_software_dl, annot=median_std_labels(heat_matrix_software_dl, heat_matrix_software_dl_std), fmt="", xticklabels=dus, yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,0])
        axes[0,0].set_title("Software Downlink")
        axes[0,0].set_xlabel("DUs")
        axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_software_dl_s, annot=median_std_labels(heat_matrix_software_dl_s, heat_matrix_software_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0,1])
        axes[0,1].set_title("Software Downlink (Shared Cores)")
        axes[0,1].set_xlabel("DUs")
        axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl, annot=median_std_labels(heat_matrix_hardware_dl, heat_matrix_hardware_dl_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,0])
        axes[1,0].set_title("Hardware Downlink")
        axes[1,0].set_xlabel("DUs")
        axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

        sns.heatmap(heat_matrix_hardware_dl_s, annot=median_std_labels(heat_matrix_hardware_dl_s, heat_matrix_hardware_dl_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                    cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1,1])
        axes[1,1].set_title("Hardware Downlink (Shared Cores)")
        axes[1,1].set_xlabel("DUs")
        axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

        plt.suptitle("Average PDSCH Processing Rate Varying Concurrent PDSCH and Number of DUs", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig('/home/fatim/fatim/plots/Concurrency/PDSCHRate.png')

def cache(channel):
    parsed_cache = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for du in dus:
        for con in concur:
            log_files = [f"{dir}{channel}/sw{du}_{con}_cache.log"]
            if con > 0:
                log_files.append(f"{dir}{channel}/hw{du}_{con}_cache.log")
            if du > 1:
                log_files.append(f"{dir}{channel}/sw{du}_{con}_cache_s.log")
                if con > 0:
                    log_files.append(f"{dir}{channel}/hw{du}_{con}_cache_s.log")
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


    heat_matrix_software = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_llc = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_llc = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_llc = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_llc = np.zeros((len(concur[:-1]), len(dus[1:])))

    heat_matrix_software_std_llc = np.zeros((len(concur), len(dus)))
    heat_matrix_hardware_std_llc = np.zeros((len(concur[:-1]), len(dus)))

    heat_matrix_software_s_std_llc = np.zeros((len(concur), len(dus[1:])))
    heat_matrix_hardware_s_std_llc = np.zeros((len(concur[:-1]), len(dus[1:])))

    for k,v in parsed_cache["s"].items():
        if "_s" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_software_s[i, j] = np.median(v["L1"])
                    heat_matrix_software_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_software_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_software_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("sw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)    
                heat_matrix_software[i, j] = np.median(v["L1"])
                heat_matrix_software_std[i, j] = np.std(v["L1"])
                heat_matrix_software_llc[i, j] = np.median(v["LLC"])
                heat_matrix_software_std_llc[i, j] = np.std(v["LLC"])

    for k,v in parsed_cache["h"].items():
        if "_s" in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                
                if du in dus[1:] and con in concur:
                    i = concur.index(con)  
                    j = dus[1:].index(du)    
                    heat_matrix_hardware_s[i, j] = np.median(v["L1"])
                    heat_matrix_hardware_s_std[i, j] = np.std(v["L1"])
                    heat_matrix_hardware_s_llc[i, j] = np.median(v["LLC"])
                    heat_matrix_hardware_s_std_llc[i, j] = np.std(v["LLC"])
        else:
            du = None
            con = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p.startswith("hw"):
                    du = int(p[2:])
                elif p.isdigit():
                    con = int(p)
            
            if du in dus and con in concur:
                i = concur.index(con)  
                j = dus.index(du)    
                heat_matrix_hardware[i, j] = np.median(v["L1"])
                heat_matrix_hardware_std[i, j] = np.std(v["L1"])
                heat_matrix_hardware_llc[i, j] = np.median(v["LLC"])
                heat_matrix_hardware_std_llc[i, j] = np.std(v["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_software, annot=median_std_labels(heat_matrix_software, heat_matrix_software_std), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Software L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s, annot=median_std_labels(heat_matrix_software_s, heat_matrix_software_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Software L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_llc, annot=median_std_labels(heat_matrix_software_llc, heat_matrix_software_std_llc), fmt="", xticklabels=dus, yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Software LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_software_s_llc, annot=median_std_labels(heat_matrix_software_s_llc, heat_matrix_software_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=tick,
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Software LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Software Cache Hit Ratio Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/SoftwareCache.png')

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sns.heatmap(heat_matrix_hardware, annot=median_std_labels(heat_matrix_hardware, heat_matrix_hardware_std), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,0])
    axes[0,0].set_title("Hardware L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s, annot=median_std_labels(heat_matrix_hardware_s, heat_matrix_hardware_s_std), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[0,1])
    axes[0,1].set_title("Hardware L1 Cache Hit Ratio (Shared Cores)")
    axes[0,1].set_xlabel("DUs")
    axes[0,1].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_llc, annot=median_std_labels(heat_matrix_hardware_llc, heat_matrix_hardware_std_llc), fmt="", xticklabels=dus, yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,0])
    axes[1,0].set_title("Hardware LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Concurrent {channel.upper()}")

    sns.heatmap(heat_matrix_hardware_s_llc, annot=median_std_labels(heat_matrix_hardware_s_llc, heat_matrix_hardware_s_std_llc), fmt="", xticklabels=dus[1:], yticklabels=tick[:-1],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio'}, ax=axes[1,1])
    axes[1,1].set_title("Hardware LLC Cache Hit Ratio (Shared Cores)")
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_ylabel(f"Concurrent {channel.upper()}")

    plt.suptitle(f"Hardware Cache Hit Ratio Varying Concurrent {channel.upper()} and Number of DUs", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/Concurrency/{channel}/HardwareCache.png')

def rate():
    proc_rate = defaultdict(lambda: {"pusch": [], "pdsch": []})
    for channel in ["pusch", "pdsch"]:
        with open(f"{dir}{channel}/parsed_logs.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                proc_rate[k][channel] = [e[channel]["rate"] for e in entry["metrics"]]

        with open(f"{dir}{channel}/parsed_logs_shared.jsonl", "r") as f:
            for line in f:
                j_line = json.loads(line)
                k = j_line.pop("file")
                entry = j_line
                proc_rate[k][channel] = [e[channel]["rate"] for e in entry["metrics"]]

    heat_matrix_software_ul = np.zeros(len(concur))
    heat_matrix_hardware_ul = np.zeros(len(concur[:-1]))

    heat_matrix_software_dl = np.zeros(len(concur))
    heat_matrix_hardware_dl = np.zeros(len(concur[:-1]))

    heat_matrix_software_ul_s = np.zeros(len(concur))
    heat_matrix_hardware_ul_s = np.zeros(len(concur[:-1]))

    heat_matrix_software_dl_s = np.zeros(len(concur))
    heat_matrix_hardware_dl_s = np.zeros(len(concur[:-1]))

    heat_matrix_software_ul_std = np.zeros(len(concur))
    heat_matrix_hardware_ul_std = np.zeros(len(concur[:-1]))

    heat_matrix_software_dl_std = np.zeros(len(concur))
    heat_matrix_hardware_dl_std = np.zeros(len(concur[:-1]))

    heat_matrix_software_ul_s_std = np.zeros(len(concur))
    heat_matrix_hardware_ul_s_std = np.zeros(len(concur[:-1]))

    heat_matrix_software_dl_s_std = np.zeros(len(concur))
    heat_matrix_hardware_dl_s_std = np.zeros(len(concur[:-1]))

    for k, vals in proc_rate.items():
        if "sw" in k:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                        if con == 0:
                            con = 14 
                if du == 1 and con in concur:
                    i = concur.index(con)
                    if "pusch" in k:
                        heat_matrix_software_ul_s[i] = np.median(vals["pusch"])
                    else:
                        heat_matrix_software_dl_s[i] = np.median(vals["pdsch"])

            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("sw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p)
                        if con == 0:
                            con = 14   
                
                if du == 1 and con in concur:
                    i = concur.index(con)
                    if "pusch" in k:
                        heat_matrix_software_ul[i] = np.median(vals["pusch"])
                    else:
                        heat_matrix_software_dl[i] = np.median(vals["pdsch"])


        else:
            if "_s." in k:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p) 
                        if con == 0:
                            con = 14    
                
                if du == 1 and con in concur:
                    i = concur.index(con)
                    if "pusch" in k:
                        heat_matrix_hardware_ul_s[i] = np.median(vals["pusch"])
                    else:
                        heat_matrix_hardware_dl_s[i] = np.median(vals["pdsch"])

            else:
                du = None
                con = None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p.startswith("hw"):
                        du = int(p[2:])
                    elif p.isdigit():
                        con = int(p) 
                        if con == 0:
                            con = 14                       
                
                if du == 1 and con in concur:
                    i = concur.index(con)  
                    if "pusch" in k:
                        heat_matrix_hardware_ul[i] = np.median(vals["pusch"])
                    else:
                        heat_matrix_hardware_dl[i] = np.median(vals["pdsch"])

    print(heat_matrix_hardware_ul, heat_matrix_hardware_dl)
    print(heat_matrix_software_ul, heat_matrix_software_dl)
    plt.style.use('grayscale')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(concur[:-1], heat_matrix_hardware_ul, label="Hardware")
    axes[0].plot(concur, heat_matrix_software_ul, label="Software", color="lightgrey")
    axes[0].set_xticks(concur)
    axes[0].set_xticklabels(labels)
    axes[0].legend()
    axes[0].set_title("Concurrent PUSCH Processing Rate")
    axes[0].set_xlabel("Concurrent PUSCH")
    axes[0].set_ylabel(f"Processing Rate (Mbps)")

    axes[1].plot(concur[:-1], heat_matrix_hardware_dl, label="Hardware")
    axes[1].plot(concur, heat_matrix_software_dl, label="Software", color="lightgrey")
    axes[1].set_xticks(concur)
    axes[1].set_xticklabels(labels)
    axes[1].legend()
    axes[1].set_title("Concurrent PDSCH Processing Rate")
    axes[1].set_xlabel("Concurrent PDSCH")
    axes[1].set_ylabel(f"Processing Rate (Mbps)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/Concurrency/CompareRate.png')

def pdsch_concur():
    latency("pdsch")
    server_energy("pdsch")
    cpu_watts("pdsch")
    cpu_usage("pdsch")
    throughput("pdsch")
    memory_usage("pdsch")
    ldpc_encoding("pdsch")
    proc_rate("pdsch")
    cache("pdsch")

def pusch_concur():
    latency("pusch")
    server_energy("pusch")
    cpu_watts("pusch")
    cpu_usage("pusch")
    throughput("pusch")
    memory_usage("pusch")
    ldpc_decoding("pusch")
    proc_rate("pusch")
    cache("pusch")

rate()