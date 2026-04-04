import numpy as np
import seaborn as sns
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/realue_logs/"
mode = ["sw", "hw"]
channels = ["dl", "udp", "ul"]

def median_std_labels(median, std):
    labels = np.empty(median.shape, dtype=object)
    for i in range(median.shape[0]):
        for j in range(median.shape[1]):
            labels[i, j] = f"{median[i, j]:.2f}\n±{std[i, j]:.2f}"
    return labels

def latency():
    latency = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs_ul.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["Uplink"] = [e["phy"]["ul_avg_latency"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_dl.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]
    
    with open(f"{dir}parsed_logs_udp.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            latency[k]["dl"] = [e["phy"]["dl_avg_latency"] for e in entry["metrics"]]

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in latency.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 0] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 0] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 0] = np.std(vals["dl"])
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 1] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 1] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 1] = np.std(vals["dl"])

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us)'}, ax=axes[0])
    axes[0].set_title("Uplink Latency")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Average Latency (us)'}, ax=axes[1])
    axes[1].set_title("Downlink Latency")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("Uplink and Downlink Latency of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Latency.png')
    
def server_energy(): 
    parsed_power = defaultdict()
    sw_data = np.genfromtxt(f"{dir}sw_dl_power.csv", delimiter=',')
    parsed_power["sw_dl"] = sw_data[:,0]

    hw_data = np.genfromtxt(f"{dir}hw_dl_power.csv", delimiter=',')
    parsed_power["hw_dl"] = hw_data[:,0]

    sw_data = np.genfromtxt(f"{dir}sw_dl_udp_power.csv", delimiter=',')
    parsed_power["sw_dl_udp"] = sw_data[:,0]

    hw_data = np.genfromtxt(f"{dir}hw_dl_udp_power.csv", delimiter=',')
    parsed_power["hw_dl_udp"] = hw_data[:,0]

    sw_data = np.genfromtxt(f"{dir}sw_ul_power.csv", delimiter=',')
    parsed_power["sw_ul"] = sw_data[:,0]

    hw_data = np.genfromtxt(f"{dir}hw_ul_power.csv", delimiter=',')
    parsed_power["hw_ul"] = hw_data[:,0]

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in parsed_power.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals)
                    heat_matrix_ul_std[0, 0] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals)
                    heat_matrix_dl_std[0, 0] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals)
                    heat_matrix_dl_std[1, 0] = np.std(vals)
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals)
                    heat_matrix_ul_std[0, 1] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals)
                    heat_matrix_dl_std[0, 1] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals)
                    heat_matrix_dl_std[1, 1] = np.std(vals)

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Watts (W)'}, ax=axes[0])
    axes[0].set_title("Uplink Power Consumption")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Average Watts (W)'}, ax=axes[1])
    axes[1].set_title("Downlink Power Consumption")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("Server Power Consumption of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Power.png')

def cpu_watts():
    parsed_power_cpu = defaultdict()
    sw_data = np.genfromtxt(f"{dir}sw_dl_energy.csv", delimiter=',')
    parsed_power_cpu["sw_dl"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_dl_energy.csv", delimiter=',')
    parsed_power_cpu["hw_dl"] = hw_data

    sw_data = np.genfromtxt(f"{dir}sw_dl_udp_energy.csv", delimiter=',')
    parsed_power_cpu["sw_dl_udp"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_dl_udp_energy.csv", delimiter=',')
    parsed_power_cpu["hw_dl_udp"] = hw_data

    sw_data = np.genfromtxt(f"{dir}sw_ul_energy.csv", delimiter=',')
    parsed_power_cpu["sw_ul"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_ul_energy.csv", delimiter=',')
    parsed_power_cpu["hw_ul"] = hw_data

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in parsed_power_cpu.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals)
                    heat_matrix_ul_std[0, 0] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals)
                    heat_matrix_dl_std[0, 0] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals)
                    heat_matrix_dl_std[1, 0] = np.std(vals)
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals)
                    heat_matrix_ul_std[0, 1] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals)
                    heat_matrix_dl_std[0, 1] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals)
                    heat_matrix_dl_std[1, 1] = np.std(vals)

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Watts (W)'}, ax=axes[0])
    axes[0].set_title("Uplink CPU Power Consumption")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Average Watts (W)'}, ax=axes[1])
    axes[1].set_title("Downlink CPU Power Consumption")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("CPU Power Consumption of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/CPUPower.png')

def cpu_usage():
    parsed_cpu = defaultdict(list)
    log_files = [
        f"{dir}sw_dl_cpu.log",
        f"{dir}hw_dl_cpu.log",
        f"{dir}sw_dl_udp_cpu.log",
        f"{dir}hw_dl_udp_cpu.log",
        f"{dir}sw_ul_cpu.log",
        f"{dir}hw_ul_cpu.log"
    ]
    for log_file in log_files:
        with open(log_file, 'r') as f:
                i = 0
                accum_cpu = 0
                for line in f:
                    gnb = i % 1
                    line = line.strip()
                    split = line.split()
                    if gnb == 0:
                        parsed_cpu[log_file].append(accum_cpu)
                        accum_cpu = float(split[7])
                    else:
                        accum_cpu += float(split[7])
                    i += 1 

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in parsed_cpu.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals)
                    heat_matrix_ul_std[0, 0] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals)
                    heat_matrix_dl_std[0, 0] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals)
                    heat_matrix_dl_std[1, 0] = np.std(vals)
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals)
                    heat_matrix_ul_std[0, 1] = np.std(vals)
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals)
                    heat_matrix_dl_std[0, 1] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals)
                    heat_matrix_dl_std[1, 1] = np.std(vals)

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[0])
    axes[0].set_title("Uplink CPU Usage")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Median CPU Usage (%)'}, ax=axes[1])
    axes[1].set_title("Downlink CPU Usage")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("CPU Usage of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/CPUUsage.png')

def throughput():
    tp = defaultdict(lambda: defaultdict(list))
    with open(f"{dir}parsed_logs_ul.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["Uplink"] = [e["ul_brate"] for e in entry["metrics_cell"]]

    with open(f"{dir}parsed_logs_dl.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]
    
    with open(f"{dir}parsed_logs_udp.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            tp[k]["dl"] = [e["dl_brate"] for e in entry["metrics_cell"]]


    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in tp.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 0] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 0] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 0] = np.std(vals["dl"])
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 1] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 1] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 1] = np.std(vals["dl"])

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[0])
    axes[0].set_title("Uplink Throughput")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Median Throughput (Mbps)'}, ax=axes[1])
    axes[1].set_title("Downlink Throughput")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("CPU Usage of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Throughput.png')

def memory_usage():
    with open(f"/home/fatim/fatim/new_logs/initial_mem.log") as f:
        total_mem = int(f.readline())
    parsed_mem = defaultdict()
    sw_data = np.genfromtxt(f"{dir}sw_dl_mem.csv", delimiter=',')
    parsed_mem["sw_dl"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_dl_mem.csv", delimiter=',')
    parsed_mem["hw_dl"] = hw_data

    sw_data = np.genfromtxt(f"{dir}sw_dl_udp_mem.csv", delimiter=',')
    parsed_mem["sw_dl_udp"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_dl_udp_mem.csv", delimiter=',')
    parsed_mem["hw_dl_udp"] = hw_data

    sw_data = np.genfromtxt(f"{dir}sw_ul_mem.csv", delimiter=',')
    parsed_mem["sw_ul"] = sw_data

    hw_data = np.genfromtxt(f"{dir}hw_ul_mem.csv", delimiter=',')
    parsed_mem["hw_ul"] = hw_data

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in parsed_mem.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(total_mem - vals) / 1024
                    heat_matrix_ul_std[0, 0] = np.std(total_mem - vals) / 1024
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(total_mem - vals) / 1024
                    heat_matrix_dl_std[0, 0] = np.std(total_mem - vals) / 1024
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(total_mem - vals) / 1024
                    heat_matrix_dl_std[1, 0] = np.std(total_mem - vals) / 1024
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(total_mem - vals) / 1024
                    heat_matrix_ul_std[0, 1] = np.std(total_mem - vals) / 1024
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(total_mem - vals) / 1024
                    heat_matrix_dl_std[0, 1] = np.std(total_mem - vals) / 1024
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(total_mem - vals) / 1024
                    heat_matrix_dl_std[1, 1] = np.std(total_mem - vals) / 1024

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Median Memory Usage (MB)'}, ax=axes[0])
    axes[0].set_title("Uplink Memory Usage")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Median Memory Usage (MB)'}, ax=axes[1])
    axes[1].set_title("Downlink Memory Usage")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("Memory Usage of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Memory.png')

def ldpc_encoding():
    enc_latency = defaultdict()
    with open(f"{dir}parsed_logs_dl.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"]  for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0] 

    with open(f"{dir}parsed_logs_udp.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                enc_latency[k] = [e["encoder"]["avg_latency"] + e["rate"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]
            else:
                enc_latency[k] = [e["encoder"]["avg_latency"] for e in entry["metrics"] if e["encoder"]["avg_nof_cbs"] != 0]   

    heat_matrix_dl = np.zeros((2, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in enc_latency.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals)
                    heat_matrix_dl_std[0, 0] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals)
                    heat_matrix_dl_std[1, 0] = np.std(vals)
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals)
                    heat_matrix_dl_std[0, 1] = np.std(vals)
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals)
                    heat_matrix_dl_std[1, 1] = np.std(vals)

    fig, axes = plt.subplots(1, 1, figsize=(8, 5))
    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us'}, ax=axes)
    axes.set_title("LDPC Encoding and Rate Matching Latency")
    axes.set_xlabel("Execution Mode")
    axes.set_ylabel(f"Real UE")

    plt.suptitle("LDPC Encoding and Rate Matching Latency of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Encoder.png')

def ldpc_decoding():
    dec_latency = defaultdict()
    with open(f"{dir}parsed_logs_ul.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            if "sw" in k:
                dec_latency[k] = [e["decoder"]["avg_latency"] + e["derate"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]
            else:
                dec_latency[k] = [e["decoder"]["avg_latency"] for e in entry["metrics"] if e["decoder"]["avg_nof_cbs"] != 0]

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_ul_std = np.zeros((1, len(mode)))

    for k, vals in dec_latency.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals)
                    heat_matrix_ul_std[0, 0] = np.std(vals)
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals)
                    heat_matrix_ul_std[0, 1] = np.std(vals)

    fig, axes = plt.subplots(1, 1, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Latency (us'}, ax=axes)
    axes.set_title("LDPC Decoding and Rate Matching Latency")
    axes.set_xlabel("Execution Mode")
    axes.set_ylabel(f"Real UE")

    plt.suptitle("LDPC Decoding and Rate Matching Latency of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Decoder.png')

def proc_rate():
    proc_rate = defaultdict(lambda: {"ul": [], "dl": []})
    with open(f"{dir}parsed_logs_ul.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["Uplink"] = [e["pusch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_dl.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    with open(f"{dir}parsed_logs_udp.jsonl", "r") as f:
        for line in f:
            j_line = json.loads(line)
            k = j_line.pop("file")
            entry = j_line
            proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    for k, vals in proc_rate.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
    
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 0] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 0] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 0] = np.std(vals["dl"])
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals["Uplink"])
                    heat_matrix_ul_std[0, 1] = np.std(vals["Uplink"])
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[0, 1] = np.std(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals["dl"])
                    heat_matrix_dl_std[1, 1] = np.std(vals["dl"])

    fig, axes = plt.subplots(1, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[0])
    axes[0].set_title("Uplink Processing Rate")
    axes[0].set_xlabel("Execution Mode")
    axes[0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Average Rate (Mbps)'}, ax=axes[1])
    axes[1].set_title("Downlink Processing Rate")
    axes[1].set_xlabel("Execution Mode")
    axes[1].set_ylabel(f"Real UE")

    plt.suptitle("Uplink and Downlink Processing Rate of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/ProcRate.png')

def cache():
    parsed_cache = defaultdict(lambda: defaultdict(list))
    log_files = [
        f"{dir}sw_dl_cache.log",
        f"{dir}hw_dl_cache.log",
        f"{dir}sw_dl_udp_cache.log",
        f"{dir}hw_dl_udp_cache.log",
        f"{dir}sw_ul_cache.log",
        f"{dir}hw_ul_cache.log"
    ]
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
                        parsed_cache[log_file]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                        parsed_cache[log_file]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                    else:    
                        parsed_cache[log_file]["LLC"].append((cache_ref - cache_miss) / cache_ref * 100)
                        parsed_cache[log_file]["L1"].append((l1_load - l1_miss) / l1_load * 100)
                i += 1    


    heat_matrix_ul = np.zeros((1, len(mode)))
    heat_matrix_dl = np.zeros((2, len(mode)))

    heat_matrix_ul_std = np.zeros((1, len(mode)))
    heat_matrix_dl_std = np.zeros((2, len(mode)))

    heat_matrix_ul_llc = np.zeros((1, len(mode)))
    heat_matrix_dl_llc = np.zeros((2, len(mode)))

    heat_matrix_ul_std_llc = np.zeros((1, len(mode)))
    heat_matrix_dl_std_llc = np.zeros((2, len(mode)))

    for k, vals in parsed_cache.items():
        if "sw" in k:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
                    if "udp" in k:
                        channel = "udp"

            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.median(vals["L1"])
                    heat_matrix_ul_std[0, 0] = np.std(vals["L1"])
                    heat_matrix_ul_llc[0, 0] = np.median(vals["LLC"])
                    heat_matrix_ul_std_llc[0, 0] = np.std(vals["LLc"])
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.median(vals["L1"])
                    heat_matrix_dl_std[0, 0] = np.std(vals["L1"])
                    heat_matrix_dl_llc[0, 0] = np.median(vals["LLC"])
                    heat_matrix_dl_std_llc[0, 0] = np.std(vals["LLC"])
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.median(vals["L1"])
                    heat_matrix_dl_std[1, 0] = np.std(vals["L1"])
                    heat_matrix_dl_llc[1, 0] = np.median(vals["LLC"])
                    heat_matrix_dl_std_llc[1, 0] = np.std(vals["LLC"])
        else:
            channel = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.median(vals["L1"])
                    heat_matrix_ul_std[0, 1] = np.std(vals["L1"])
                    heat_matrix_ul_llc[0, 1] = np.median(vals["LLC"])
                    heat_matrix_ul_std_llc[0, 1] = np.std(vals["LLC"])
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.median(vals["L1"])
                    heat_matrix_dl_std[0, 1] = np.std(vals["L1"])
                    heat_matrix_dl_llc[0, 1] = np.median(vals["LLC"])
                    heat_matrix_dl_std_llc[0, 1] = np.std(vals["LLC"])
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.median(vals["L1"])
                    heat_matrix_dl_std[1, 1] = np.std(vals["L1"])
                    heat_matrix_dl_llc[1, 1] = np.median(vals["LLC"])
                    heat_matrix_dl_std_llc[1, 1] = np.std(vals["LLC"])

    fig, axes = plt.subplots(2, 2, figsize=(8, 5))
    sns.heatmap(heat_matrix_ul, annot=median_std_labels(heat_matrix_ul, heat_matrix_ul_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Hit Ratio (%)'}, ax=axes[0,0])
    axes[0,0].set_title("Uplink L1 Cache Hit Ratio")
    axes[0,0].set_xlabel("Execution Mode")
    axes[0,0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl, annot=median_std_labels(heat_matrix_dl, heat_matrix_dl_std), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio (%)'}, ax=axes[0,1])
    axes[0,1].set_title("Downlink L1 Cache Hit Ratio")
    axes[0,1].set_xlabel("Execution Mode")
    axes[0,1].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_ul_llc, annot=median_std_labels(heat_matrix_ul_llc, heat_matrix_ul_std_llc), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Uplink"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Hit Ratio (%)'}, ax=axes[1,0])
    axes[1,0].set_title("Uplink LLC Cache Hit Ratio")
    axes[1,0].set_xlabel("Execution Mode")
    axes[1,0].set_ylabel(f"Real UE")

    sns.heatmap(heat_matrix_dl_llc, annot=median_std_labels(heat_matrix_dl_llc, heat_matrix_dl_std_llc), fmt="", xticklabels=["Software", "Hardware"], yticklabels=["Downlink (TCP)", "Downlink (UDP)"],
                cmap="YlOrRd", cbar_kws={'label': 'Hit Ratio (%)'}, ax=axes[1,1])
    axes[1,1].set_title("Downlink LLC Cache Hit Ratio")
    axes[1,1].set_xlabel("Execution Mode")
    axes[1,1].set_ylabel(f"Real UE")

    plt.suptitle("Cache Hit Rate of Real UE", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('plots/realue/Cache.png')

latency()
server_energy()
cpu_watts()
cpu_usage()
throughput()
memory_usage()
ldpc_decoding()
ldpc_encoding()
proc_rate()
cache()
