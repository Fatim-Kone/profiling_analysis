import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

dir_e2e = "/home/fatim/fatim/e2e_logs/"
dir_real = "/home/fatim/fatim/realue_logs/"
modes = ["sw", "hw"]
channel = ["ul", "dl"]

def power_labels(power, cpu):
    labels = np.empty(power.shape, dtype=object)
    for i in range(power.shape[0]):
        for j in range(power.shape[1]):
            labels[i, j] = f"{power[i, j]:.2f}\n({cpu[i, j]:.2f})"
    return labels

def server_cpu_power():
    parsed_power = defaultdict(lambda: defaultdict())
    parsed_power_cpu = defaultdict(lambda: defaultdict())

    for dir in [dir_e2e, dir_real]:
        for m in channel:
            du = 1
            if dir == dir_real:
                du = ""
            if m == "dl" and dir == dir_real:
                m = "dl_udp"
            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_power.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_power.csv", delimiter=',')
            parsed_power["s"][f"{dir}sw{du}_{m}"] = sw_data[:,0]
            parsed_power["h"][f"{dir}hw{du}_{m}"] = hw_data[:,0]

            sw_data = np.genfromtxt(f"{dir}sw{du}_{m}_energy.csv", delimiter=',')
            hw_data = np.genfromtxt(f"{dir}hw{du}_{m}_energy.csv", delimiter=',')
            parsed_power_cpu["s"][f"{dir}sw{du}_{m}"] = sw_data
            parsed_power_cpu["h"][f"{dir}hw{du}_{m}"] = hw_data

    heat_matrix_ul = np.zeros((len(modes), 2))
    heat_matrix_dl = np.zeros((len(modes), 2))

    heat_matrix_ul_cpu = np.zeros((len(modes), 2))
    heat_matrix_dl_cpu = np.zeros((len(modes), 2))

    for k,vals in parsed_power["s"].items():
        if "_shared" not in k:   
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in modes:
                        m = p  
            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul[0, 0] = np.mean(vals)
                else:
                    heat_matrix_ul[0, 1] = np.mean(vals)
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl[0, 0] = np.mean(vals)
                else:
                    heat_matrix_dl[0, 1] = np.mean(vals)

    for k,vals in parsed_power["h"].items():
        if "_shared" not in k:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in modes:
                    m = p
                
            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul[1, 0] = np.mean(vals)
                else:
                    heat_matrix_ul[1, 1] = np.mean(vals)
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl[1, 0] = np.mean(vals)
                else:
                    heat_matrix_dl[1, 1] = np.mean(vals)

    for k,vals in parsed_power_cpu["s"].items():
        if "_shared" not in k:
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p  in modes:
                        m = p
            
            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul_cpu[0, 0] = np.mean(vals)
                else:
                    heat_matrix_ul_cpu[0, 1] = np.mean(vals)
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl_cpu[0, 0] = np.mean(vals)
                else:
                    heat_matrix_dl_cpu[0, 1] = np.mean(vals)

    for k,vals in parsed_power_cpu["h"].items():
        if "_shared" not in k:  
            du = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p  in modes:
                        m = p
            
            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul_cpu[1, 0] = np.mean(vals)
                else:
                    heat_matrix_ul_cpu[1, 1] = np.mean(vals)
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl_cpu[1, 0] = np.mean(vals)
                else:
                    heat_matrix_dl_cpu[1, 1] = np.mean(vals)
    

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.heatmap(heat_matrix_ul, annot=power_labels(heat_matrix_ul, heat_matrix_ul_cpu), fmt="", xticklabels=["UL (Real)", "UL (E2E)"], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[0])
    axes[0].set_title("Uplink")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=power_labels(heat_matrix_dl, heat_matrix_dl_cpu), fmt="", xticklabels=["UL (Real)", "UL (E2E)"], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Power Consumption (W)'}, ax=axes[1])
    axes[1].set_title("Downlink")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/E2EvRealPowerComparison.png')

def cpu_usage():
    parsed_cpu = defaultdict(lambda: defaultdict(list))
    for dir in [dir_e2e, dir_real]:
        for m in channel:
            du = 1
            if dir == dir_real:
                du = ""
            if m == "dl" and dir == dir_real:
                m = "dl_udp"
            log_files = [f"{dir}sw{du}_{m}_cpu.log", f"{dir}hw{du}_{m}_cpu.log"]
            for log_file in log_files:
                with open(log_file, 'r') as f:
                        i = 0
                        off_cpu = 0
                        accum_cpu = 0
                        for line in f:
                            gnb = i % 1
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

    heat_matrix_ul = np.zeros((len(modes), 2))
    heat_matrix_dl = np.zeros((len(modes), 2))

    heat_matrix_ul_off = np.zeros((len(modes), 2))
    heat_matrix_dl_off = np.zeros((len(modes), 2))

    for k, v in parsed_cpu["s"].items():
        if "_s." in k:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p  in modes:
                    m = p

            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul[0, 0] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_off[0, 0] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_ul[0, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_off[0, 1] = np.mean(np.array(v)[:,1])
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl[0, 0] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_off[0, 0] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_dl[0, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_off[0, 1] = np.mean(np.array(v)[:,1])
        else:
            du = None
            m =  None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p  in modes:
                    m = p
                
            if "ul" in k:
                if dir_real in k:
                    heat_matrix_ul[0, 0] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_off[0, 0] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_ul[0, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_ul_off[0, 1] = np.mean(np.array(v)[:,1])
            elif "dl" in k:
                if dir_real in k and "dl_udp" in k:
                    heat_matrix_dl[0, 0] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_off[0, 0] = np.mean(np.array(v)[:,1])
                else:
                    heat_matrix_dl[0, 1] = np.mean(np.array(v)[:,0])
                    heat_matrix_dl_off[0, 1] = np.mean(np.array(v)[:,1])

        for k, v in parsed_cpu["h"].items():
            if "_s." in k:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p  in modes:
                        m = p
                
                if "ul" in k:
                    if dir_real in k:
                        heat_matrix_ul[1, 0] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_off[1, 0] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_ul[1, 1] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_off[1, 1] = np.mean(np.array(v)[:,1])
                elif "dl" in k:
                    if dir_real in k and "dl_udp" in k:
                        heat_matrix_dl[1, 0] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_off[1, 0] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_dl[1, 1] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_off[1, 1] = np.mean(np.array(v)[:,1])
            else:
                du = None
                m =  None
                log = k.split("/")[-1]
                parts = log.split("_")
                for p in parts:
                    if p  in modes:
                        m = p
                
                if "ul" in k:
                    if dir_real in k:
                        heat_matrix_ul[1, 0] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_off[1, 0] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_ul[1, 1] = np.mean(np.array(v)[:,0])
                        heat_matrix_ul_off[1, 1] = np.mean(np.array(v)[:,1])
                elif "dl" in k:
                    if dir_real in k and "dl_udp" in k:
                        heat_matrix_dl[1, 0] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_off[1, 0] = np.mean(np.array(v)[:,1])
                    else:
                        heat_matrix_dl[1, 1] = np.mean(np.array(v)[:,0])
                        heat_matrix_dl_off[1, 1] = np.mean(np.array(v)[:,1])

    fig, axes = plt.subplots(1, 2, figsize=(6, 4))
    sns.heatmap(heat_matrix_ul, annot=power_labels(heat_matrix_ul, heat_matrix_ul_off), fmt="", xticklabels=["UL (Real)", "UL (E2E)"], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[0])
    axes[0].set_title("Uplink CPU Usage")
    axes[0].set_xlabel("DUs")
    axes[0].set_ylabel("Execution Modes")

    sns.heatmap(heat_matrix_dl, annot=power_labels(heat_matrix_dl, heat_matrix_dl_off), fmt="", xticklabels=["DL (Real)", "DL (E2E)"], yticklabels=["Software", "Hardware"],
                cmap="YlOrRd" ,cbar_kws={'label': 'CPU Usage (%)'}, ax=axes[1])
    axes[1].set_title("Downlink CPU Usage")
    axes[1].set_xlabel("DUs")
    axes[1].set_ylabel("Execution Modes")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'/home/fatim/fatim/plots/RealE2ECPUUsage.png')

server_cpu_power()
cpu_usage()


