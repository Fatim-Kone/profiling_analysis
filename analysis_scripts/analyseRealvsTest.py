import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict

dir_test_ul = "/home/fatim/fatim/concur_logs/pusch"
dir_test_dl = "/home/fatim/fatim/concur_logs/pdsch"
dir_real = "/home/fatim/fatim/realue_logs/"

metrics = {}
proc_rate = defaultdict(lambda: {"ul": [], "dl": []})
mode = ["sw", "hw"]
modes = {"h":"High Load", "l":"Low Load"}
channels = ["dl", "udp", "ul"]
plt.style.use('grayscale')

with open(f"{dir_test_dl}parsed_logs.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        if "1" in k:
            entry = j_line
            metrics[k] = entry["metrics"]
            proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]
            
with open(f"{dir_test_ul}parsed_logs.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        if "1" in k:
            entry = j_line
            metrics[k] = entry["metrics"]          
            proc_rate[k]["ul"] = [e["pusch"]["rate"] for e in entry["metrics"]]

with open(f"{dir_real}parsed_logs_dl.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        entry = j_line
        metrics[k] = entry["metrics"]
        proc_rate[k]["dl"] = [e["pusch"]["rate"] for e in entry["metrics"]]

with open(f"{dir_real}parsed_logs_ul.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        entry = j_line
        metrics[k] = entry["metrics"]
        proc_rate[k]["ul"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

with open(f"{dir_real}parsed_logs_udp.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        entry = j_line
        metrics[k] = entry["metrics"]
        proc_rate[k]["dl"] = [e["pdsch"]["rate"] for e in entry["metrics"]]

def pdsch_plot():
    pdsch_sw = defaultdict(list)
    pdsch_hw = defaultdict(list)

    for k,v in metrics.items():
        if "sw" in k and "ul" not in k and "pusch" not in k:
            for entry in metrics[k]:
                pdsch_sw[k].append(entry)
        elif "ul" not in k:
            for entry in metrics[k]:
                pdsch_hw[k].append(entry)

    median_entries_s = defaultdict(list)
    median_entries_h = defaultdict(list)

    for logFile, entries in pdsch_sw.items():
        median_entries_s[logFile] = [np.median([x["encoder"]["avg_latency"] for x in entries if x["encoder"]["avg_nof_cbs"] != 0]), 
                                np.median([x["rate"]["avg_latency"] for x in entries]),
                                np.median([x["mod"]["avg_latency"] for x in entries]),
                                np.median([x["scrambling"]["avg_latency"] for x in entries])
        ]

    for logFile, entries in pdsch_hw.items():
        median_entries_h[logFile] = [np.median([x["encoder"]["avg_latency"] for x in entries if x["encoder"]["avg_nof_cbs"] != 0]),
                                np.median([x["rate"]["avg_latency"] for x in entries]),
                                np.median([x["mod"]["avg_latency"] for x in entries]),
                                np.median([x["scrambling"]["avg_latency"] for x in entries])
        ]

    enc_rm_s, mod_s, scramb_s = [], [], []
    enc_h, mod_h, scramb_h = [], [], []

    for b, e in median_entries_s.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]
        rm = e[1]

        enc_rm_s.append(enc+rm)
        mod_s.append(mod)
        scramb_s.append(scr)

    for b, e in median_entries_h.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]

        enc_h.append(enc)
        mod_h.append(mod)
        scramb_h.append(scr)


    x_axis = ["Test UE (High Load)", "Test UE (Low Load)", "Real UE (TCP)", "Real UE (UDP)"]

    w, x = 0.3, np.arange(len(x_axis))

    enc_rm_s = np.array(enc_rm_s)
    mod_s = np.array(mod_s)
    scramb_s = np.array(scramb_s)

    enc_h = np.array(enc_h)
    mod_h = np.array(mod_h)
    scramb_h = np.array(scramb_h)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - w/2, enc_h, width=w, label='Encoding+RateMatching', edgecolor='black', color='black')
    ax.bar(x - w/2, scramb_h, width=w, label='Scrambling', bottom=enc_h, edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, mod_h, width=w, label='Modulation', bottom=enc_h+scramb_h, edgecolor='black', color='white')

    ax.bar(x + w/2, enc_rm_s, width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, scramb_s, width=w, label='_nolegend_', bottom=enc_rm_s, color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, mod_s, width=w, label='_nolegend_',bottom=enc_rm_s+scramb_s, color='white', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis, fontsize=12)
    ax.set_ylabel('Time (us)', fontsize=12)
    ax.set_xlabel("UE/Load Scenario", fontsize=12)
    ax.legend(fontsize=14)
    plt.figtext(
        0.12, 0.95,
        "Hardware = Left Bar \nSoftware = Right Bar",
        ha="left",
        va="top",
        fontsize=14
    )
    plt.tight_layout()

    plt.savefig('plots/PDSCH.png')

def pusch_plot():
    pusch_sw = defaultdict(list)
    pusch_hw = defaultdict(list)

    for k,v in metrics.items():
        if "sw" in k and "dl" not in k and "udp" not in k and "pdsch" not in k:
            for entry in metrics[k]:
                pusch_sw[k].append(entry)
        elif "dl" not in k and "udp" not in k:
            for entry in metrics[k]:
                pusch_hw[k].append(entry)

    median_entries_s = defaultdict(list)
    median_entries_h = defaultdict(list)

    for logFile, entries in pusch_sw.items():
        median_entries_s[logFile] = [np.median([x["decoder"]["avg_latency"] for x in entries if x["decoder"]["avg_nof_cbs"] != 0]), 
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]), #demultiplex
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]
    for logFile, entries in pusch_hw.items():
        median_entries_h[logFile] = [np.median([x["decoder"]["avg_latency"] for x in entries if x["decoder"]["avg_nof_cbs"] != 0]), 
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]), #demultiplex
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]

    decode_s, demod_s, descramb_s, eq_s, est_s = [], [], [], [], []
    decode_h, demod_h, descramb_h, eq_h, est_h = [], [], [], [], []


    for b, e in median_entries_s.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        demod_s.append(demod)
        descramb_s.append(descr)
        est_s.append(est)
        eq_s.append(eq)
        decode_s.append(decode+derate)

    for b, e in median_entries_h.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        demod_h.append(demod)
        descramb_h.append(descr)
        est_h.append(est)
        eq_h.append(eq)
        decode_h.append(decode+derate)


    
    x_axis = ["Test UE (High Load)", "Test UE (Low Load)", "Real UE"]
    w, x = 0.3, np.arange(len(x_axis))

    demod_s = np.array(demod_s)
    est_s = np.array(est_s)
    eq_s = np.array(eq_s)
    descramb_s = np.array(descramb_s)
    decode_s = np.array(decode_s)

    demod_h = np.array(demod_h)
    est_h = np.array(est_h)
    eq_h = np.array(eq_h)
    descramb_h = np.array(descramb_h)
    decode_h = np.array(decode_h)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - w/2, eq_h, width=w, label='Channel Equalisation', edgecolor='black', color='black')
    ax.bar(x - w/2, descramb_h, width=w, label='Descrambling', bottom=eq_h, edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, demod_h, width=w, label='Demodulation', bottom=eq_h+descramb_h, edgecolor='black', color='white')
    ax.bar(x - w/2, est_h, width=w, label='Channel Estimation', bottom=eq_h+demod_h+descramb_h, edgecolor='black', color='white', hatch="x")
    ax.bar(x - w/2, decode_h, width=w, label='Decode+RateDematch', bottom=eq_h+descramb_h+est_h+demod_h, edgecolor='black', color='dimgrey')

    ax.bar(x + w/2, eq_s, width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, descramb_s, width=w, label='_nolegend_', bottom=eq_s, color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, demod_s, width=w, label='_nolegend_',bottom=eq_s+descramb_s, color='white', edgecolor='black')
    ax.bar(x + w/2, est_s, width=w, label='_nolegend_', bottom=eq_s+demod_s+descramb_s, edgecolor='black', color='white', hatch="x")
    ax.bar(x + w/2, decode_s, width=w, label='_nolegend_', bottom=eq_s+descramb_s+est_s+demod_s, edgecolor='black', color='dimgrey')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis, fontsize=12)
    ax.set_ylabel('Time (us)', fontsize=12)
    ax.set_xlabel("UE/Load Scenario", fontsize=12)
    ax.legend(fontsize=14)
    plt.figtext(
        0.48, 0.94,
        "Hardware = Left Bar \nSoftware = Right Bar",
        ha="left",
        va="top",
        fontsize=14
    )
    plt.tight_layout()

    plt.savefig('plots/PUSCH.png')

def proc_comp():
    pusch_sw = defaultdict(list)
    pusch_hw = defaultdict(list)

    pdsch_sw = defaultdict(list)
    pdsch_hw = defaultdict(list)
    
    heat_matrix_ul = np.zeros((3, len(mode)))
    heat_matrix_dl = np.zeros((4, len(mode)))

    for k, vals in proc_rate.items():
        if "sw" in k:
            channel = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
                elif p in modes.keys():
                        m = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 0] = np.mean(vals["ul"])
                elif channel == "dl":
                    heat_matrix_dl[0, 0] = np.mean(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 0] = np.mean(vals["dl"])
            elif m in modes.keys():
                if m == "h":
                    heat_matrix_ul[1, 0] = np.mean(vals["ul"])
                    heat_matrix_dl[2, 0] = np.mean(vals["dl"])
                else:
                    heat_matrix_ul[2, 0] = np.mean(vals["ul"])
                    heat_matrix_dl[3, 0] = np.mean(vals["dl"])
        else:
            channel = None
            m = None
            log = k.split("/")[-1]
            parts = log.split("_")
            for p in parts:
                if p in channels:
                    channel = p
                elif p in modes.keys():
                        m = p
            
            if channel in channels:
                if channel == "ul":
                    heat_matrix_ul[0, 1] = np.mean(vals["ul"])
                elif channel == "dl":
                    heat_matrix_dl[0, 1] = np.mean(vals["dl"])
                elif channel == "udp":
                    heat_matrix_dl[1, 1] = np.mean(vals["dl"])
            elif m in modes.keys():
                if m == "h":
                    heat_matrix_ul[1, 1] = np.mean(vals["ul"])
                    heat_matrix_dl[2, 1] = np.mean(vals["dl"])
                else:
                    heat_matrix_ul[2, 1] = np.mean(vals["ul"])
                    heat_matrix_dl[3, 1] = np.mean(vals["dl"])

    fig, axes = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={'wspace':0.3})
    sns.heatmap(heat_matrix_ul.T, annot=heat_matrix_ul.T, fmt=".1f", yticklabels=["Software", "Hardware"], xticklabels=["UL (Real UE)", "UL (Test UE, High Load)","UL (Test UE, Low Load)"],
                cmap="YlOrRd" ,cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[0])
    axes[0].set_title("PUSCH")
    axes[0].set_xlabel("UE/Load Scenario")
    axes[0].set_ylabel(f"Execution Mode")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=10, ha='center', fontsize=8)

    sns.heatmap(heat_matrix_dl.T, annot=heat_matrix_dl.T, fmt=".1f", yticklabels=["Software", "Hardware"], xticklabels=["DL (Real UE, TCP)", "DL (Real UE, UDP)", "DL (Test UE, High Load)", "DL (Test UE, Low Load)"],
                cmap="YlOrRd", cbar_kws={'label': 'Processing Rate (Mbps)'}, ax=axes[1])
    axes[1].set_title("PDSCH")
    axes[1].set_xlabel("UE/Load Scenario")
    axes[1].set_ylabel(f"Execution Mode")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=10, ha='center', fontsize=8)
    plt.savefig('plots/RealComparisonProcRate.png')

pusch_plot()
pdsch_plot()
# proc_comp()