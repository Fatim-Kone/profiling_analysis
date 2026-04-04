import numpy as np
import json
import matplotlib.pyplot as plt
from collections import defaultdict

dir = "/home/fatim/fatim/new_logs/"
dus = [1,2,4,6,8]

pdsch = {}
pusch = {}
metrics = {}
metrics_cell = {}
plt.style.use('grayscale')

with open(f"{dir}parsed_logs.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        entry = j_line
        pdsch[k] = entry["pdsch"]
        pusch[k] = entry["pusch"]
        metrics[k] = entry["metrics"]
        metrics_cell[k] = entry["metrics_cell"]

with open(f"{dir}parsed_logs_shared.jsonl", "r") as f:
    for line in f:
        j_line = json.loads(line)
        k = j_line.pop("file")
        entry = j_line
        pdsch[k] = entry["pdsch"]
        pusch[k] = entry["pusch"]
        metrics[k] = entry["metrics"]
        metrics_cell[k] = entry["metrics_cell"]

def pad(lst):
    return np.array(lst)

def pdsch_plot():
    pdsch_sw = defaultdict(list)
    pdsch_hw = defaultdict(list)
    pdsch_sw_s = defaultdict(list)
    pdsch_hw_s = defaultdict(list)

    for k,v in metrics.items():
        if "sw" in k:
            for entry in metrics[k]:
                if "_s." in k:
                    pdsch_sw_s[k].append(entry)
                else:
                    pdsch_sw[k].append(entry)
        else:
            for entry in metrics[k]:
                if "_s." in k:
                    pdsch_hw_s[k].append(entry)
                else:
                    pdsch_hw[k].append(entry)

    median_entries_s = defaultdict(list)
    median_entries_h = defaultdict(list)
    median_entries_s_s = defaultdict(list)
    median_entries_h_s = defaultdict(list)

    for logFile, entries in pdsch_sw.items():
        median_entries_s[logFile] = [np.median([x["encoder"]["avg_latency"] for x in entries]), 
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

    for logFile, entries in pdsch_sw_s.items():
        median_entries_s_s[logFile] = [np.median([x["encoder"]["avg_latency"] for x in entries]),
                                np.median([x["rate"]["avg_latency"] for x in entries]),
                                np.median([x["mod"]["avg_latency"] for x in entries]),
                                np.median([x["scrambling"]["avg_latency"] for x in entries])
        ]

    for logFile, entries in pdsch_hw_s.items():
        median_entries_h_s[logFile] = [np.median([x["encoder"]["avg_latency"] for x in entries if x["encoder"]["avg_nof_cbs"] != 0]),
                                np.median([x["rate"]["avg_latency"] for x in entries]),
                                np.median([x["mod"]["avg_latency"] for x in entries]),
                                np.median([x["scrambling"]["avg_latency"] for x in entries])
        ]

    enc_rm_l_s, mod_l_s, scramb_l_s = [], [], []
    enc_l_h, mod_l_h, scramb_l_h= [], [], []

    enc_rm_l_s_s, mod_l_s_s, scramb_l_s_s = [], [], []
    enc_l_h_s, mod_l_h_s, scramb_l_h_s = [], [], []

    enc_rm_h_s, mod_h_s, scramb_h_s = [], [], []
    enc_h_h, mod_h_h, scramb_h_h = [], [], []

    enc_rm_h_s_s, mod_h_s_s, scramb_h_s_s = [], [], []
    enc_h_h_s, mod_h_h_s, scramb_h_h_s = [], [], []

    for b, e in median_entries_s.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]
        rm = e[1]

        if "_l_" in b:
            enc_rm_l_s.append(enc+rm)
            mod_l_s.append(mod)
            scramb_l_s.append(scr)
        else:
            enc_rm_h_s.append(enc+rm)
            mod_h_s.append(mod)
            scramb_h_s.append(scr)

    for b, e in median_entries_h.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]

        if "_l_" in b:
            enc_l_h.append(enc)
            mod_l_h.append(mod)
            scramb_l_h.append(scr)
        else:
            enc_h_h.append(enc)
            mod_h_h.append(mod)
            scramb_h_h.append(scr)

    for b, e in median_entries_s_s.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]
        rm = e[1]

        if "_l_" in b:
            enc_rm_l_s_s.append(enc+rm)
            mod_l_s_s.append(mod)
            scramb_l_s_s.append(scr)
        else:
            enc_rm_h_s_s.append(enc+rm)
            mod_h_s_s.append(mod)
            scramb_h_s_s.append(scr)

    for b, e in median_entries_h_s.items():
        enc = e[0]
        mod = e[2]
        scr = e[3]

        if "_l_" in b:
            enc_l_h_s.append(enc)
            mod_l_h_s.append(mod)
            scramb_l_h_s.append(scr)
        else:
            enc_h_h_s.append(enc)
            mod_h_h_s.append(mod)
            scramb_h_h_s.append(scr)


    x_axis = [f"{i} DUs" for i in dus]
    x_axis_shared = [f"{i} DUs" for i in dus[1:]]

    w, x, x_s = 0.3, np.arange(len(x_axis)), np.arange(len(x_axis_shared))

    #Software Low Load Dis
    enc_rm_l_s = np.array(enc_rm_l_s)
    mod_l_s = np.array(mod_l_s)
    scramb_l_s = np.array(scramb_l_s)

    #Software High Load Dis
    enc_rm_h_s = np.array(enc_rm_h_s)
    mod_h_s = np.array(mod_h_s)
    scramb_h_s = np.array(scramb_h_s)

    #Hardware Low Load Dis
    enc_l_h = np.array(enc_l_h)
    mod_l_h = np.array(mod_l_h)
    scramb_l_h = np.array(scramb_l_h)

    #Hardware High Load Dis
    enc_h_h = np.array(enc_h_h)
    mod_h_h = np.array(mod_h_h)
    scramb_h_h = np.array(scramb_h_h)

    #Software Low Load Shared
    enc_rm_l_s_s = np.array(enc_rm_l_s_s)
    mod_l_s_s = np.array(mod_l_s_s)
    scramb_l_s_s = np.array(scramb_l_s_s)

    #Software High Load Shared
    enc_rm_h_s_s = np.array(enc_rm_h_s_s)
    mod_h_s_s = np.array(mod_h_s_s)
    scramb_h_s_s = np.array(scramb_h_s_s)

    #Hardware Low Load Shared
    enc_l_h_s = np.array(enc_l_h_s)
    mod_l_h_s = np.array(mod_l_h_s)
    scramb_l_h_s = np.array(scramb_l_h_s)

    #Hardware High Load Shared
    enc_h_h_s = np.array(enc_h_h_s)
    mod_h_h_s = np.array(mod_h_h_s)
    scramb_h_h_s = np.array(scramb_h_h_s)

    fig, ax = plt.subplots()

    ax.bar(x - w/2, enc_l_h[:-1], width=w, label='Encoding+RateMatching', edgecolor='black', color='black')
    ax.bar(x - w/2, scramb_l_h[:-1], width=w, label='Scrambling', bottom=enc_l_h[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, mod_l_h[:-1], width=w, label='Modulation', bottom=enc_l_h[:-1]+scramb_l_h[:-1], edgecolor='black', color='white')

    ax.bar(x + w/2, enc_rm_l_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, scramb_l_s[:-1], width=w, label='_nolegend_', bottom=enc_rm_l_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, mod_l_s[:-1], width=w, label='_nolegend_',bottom=enc_rm_l_s[:-1]+scramb_l_s[:-1], color='white', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Time (us)')
    ax.legend()
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/plots/PDSCH_LOW.png')

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - w/2, enc_h_h[:-1], width=w, label='Encoding+RateMatching', edgecolor='black', color='black')
    ax.bar(x - w/2, scramb_h_h[:-1], width=w, label='Scrambling', bottom=enc_h_h[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, mod_h_h[:-1], width=w, label='Modulation', bottom=enc_h_h[:-1]+scramb_h_h[:-1], edgecolor='black', color='white')

    ax.bar(x + w/2, enc_rm_h_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, scramb_h_s[:-1], width=w, label='_nolegend_', bottom=enc_rm_h_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, mod_h_s[:-1], width=w, label='_nolegend_',bottom=enc_rm_h_s[:-1]+scramb_h_s[:-1], color='white', edgecolor='black')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Time (us)')
    ax.set_xlabel('DUs')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=14)
    plt.figtext(
            0.60, 0.68,
            "Hardware = Left Bar \nSoftware = Right Bar",
            ha="left",
            fontsize=14
        )
    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/plots/PDSCH_HIGH.png')

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, enc_l_h_s[:-1], width=w, label='Encoding+RateMatching', edgecolor='black', color='black')
    ax.bar(x_s - w/2, scramb_l_h_s[:-1], width=w, label='Scrambling', bottom=enc_l_h_s[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x_s - w/2, mod_l_h_s[:-1], width=w, label='Modulation', bottom=enc_l_h_s[:-1]+scramb_l_h_s[:-1], edgecolor='black', color='white')

    ax.bar(x_s + w/2, enc_rm_l_s_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x_s + w/2, scramb_l_s_s[:-1], width=w, label='_nolegend_', bottom=enc_rm_l_s_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x_s + w/2, mod_l_s_s[:-1], width=w, label='_nolegend_',bottom=enc_rm_l_s_s[:-1]+scramb_l_s_s[:-1], color='white', edgecolor='black')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Time (us)')
    ax.legend()
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/plots/PDSCH_SHARED_LOW.png')

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, enc_h_h_s[:-1], width=w, label='Encoding+RateMatching', edgecolor='black', color='black')
    ax.bar(x_s - w/2, scramb_h_h_s[:-1], width=w, label='Scrambling', bottom=enc_h_h_s[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x_s - w/2, mod_h_h_s[:-1], width=w, label='Modulation', bottom=enc_h_h_s[:-1]+scramb_h_h_s[:-1], edgecolor='black', color='white')

    ax.bar(x_s + w/2, enc_rm_h_s_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x_s + w/2, scramb_h_s_s[:-1], width=w, label='_nolegend_', bottom=enc_rm_h_s_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x_s + w/2, mod_h_s_s[:-1], width=w, label='_nolegend_',bottom=enc_rm_h_s_s[:-1]+scramb_h_s_s[:-1], color='white', edgecolor='black')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Time (us)')
    ax.legend()
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/plots/PDSCH_SHARED_HIGH.png')

def pusch_plot():
    pusch_sw = defaultdict(list)
    pusch_hw = defaultdict(list)
    pusch_sw_s = defaultdict(list)
    pusch_hw_s = defaultdict(list)

    for k,v in metrics.items():
        if "sw" in k:
            for entry in metrics[k]:
                if "_s" in k:
                    pusch_sw_s[k].append(entry)
                else:
                    pusch_sw[k].append(entry)
        else:
            for entry in metrics[k]:
                if "_s" in k:
                    pusch_hw_s[k].append(entry)
                else:
                    pusch_hw[k].append(entry)

    median_entries_s = defaultdict(list)
    median_entries_h = defaultdict(list)
    median_entries_s_s = defaultdict(list)
    median_entries_h_s = defaultdict(list)

    for logFile, entries in pusch_sw.items():
        median_entries_s[logFile] = [np.median([x["decoder"]["avg_latency"] for x in entries]), 
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]), #demultiplex
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]
    for logFile, entries in pusch_hw.items():
        median_entries_h[logFile] = [np.median([x["decoder"]["avg_latency"]/x["decoder"]["avg_nof_cbs"] for x in entries if x["decoder"]["avg_nof_cbs"] != 0]), 
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]), #demultiplex
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]

    for logFile, entries in pusch_sw_s.items():
        median_entries_s_s[logFile] = [np.median([x["decoder"]["avg_latency"] for x in entries]),
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]), #demultiplex
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]

    for logFile, entries in pusch_hw_s.items():
        median_entries_h_s[logFile] = [np.median([x["decoder"]["avg_latency"]/x["decoder"]["avg_nof_cbs"] for x in entries if x["decoder"]["avg_nof_cbs"] != 0]),
                                    np.median([x["derate"]["avg_latency"] for x in entries]),
                                    np.median([x["descrambling"]["avg_latency"] for x in entries]),
                                    np.median([x["demod"]["avg_latency"] for x in entries]),
                                    np.median([x["equalizer"]["avg_latency"] for x in entries]),
                                    np.median([x["estimator"]["avg_latency"] for x in entries]),
        ]

    decode_l_s, demod_l_s, descramb_l_s, eq_l_s, est_l_s = [], [], [], [], []
    decode_l_h, demod_l_h, descramb_l_h, eq_l_h, est_l_h = [], [], [], [], []

    decode_h_s, demod_h_s, descramb_h_s, eq_h_s, est_h_s = [], [], [], [], []
    decode_h_h, demod_h_h, descramb_h_h, eq_h_h, est_h_h = [], [], [], [], []

    decode_l_s_s, demod_l_s_s, descramb_l_s_s, eq_l_s_s, est_l_s_s = [], [], [], [], []
    decode_l_h_s, demod_l_h_s, descramb_l_h_s, eq_l_h_s, est_l_h_s = [], [], [], [], []

    decode_h_s_s, demod_h_s_s, descramb_h_s_s, eq_h_s_s, est_h_s_s = [], [], [], [], []
    decode_h_h_s, demod_h_h_s, descramb_h_h_s, eq_h_h_s, est_h_h_s = [], [], [], [], []


    for b, e in median_entries_s.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        if "_l_" in b:
            demod_l_s.append(demod)
            descramb_l_s.append(descr)
            est_l_s.append(est)
            eq_l_s.append(eq)
            decode_l_s.append(decode+derate)
        
        else:
            demod_h_s.append(demod)
            descramb_h_s.append(descr)
            est_h_s.append(est)
            eq_h_s.append(eq)
            decode_h_s.append(decode+derate)

    for b, e in median_entries_h.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        if "_l_" in b:
            demod_l_h.append(demod)
            descramb_l_h.append(descr)
            est_l_h.append(est)
            eq_l_h.append(eq)
            decode_l_h.append(decode+derate)
        else:
            demod_h_h.append(demod)
            descramb_h_h.append(descr)
            est_h_h.append(est)
            eq_h_h.append(eq)
            decode_h_h.append(decode+derate)

    for b, e in median_entries_s_s.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        if "_l_" in b:
            demod_l_s_s.append(demod)
            descramb_l_s_s.append(descr)
            est_l_s_s.append(est)
            eq_l_s_s.append(eq)
            decode_l_s_s.append(decode+derate)
        else:
            demod_h_s_s.append(demod)
            descramb_h_s_s.append(descr)
            est_h_s_s.append(est)
            eq_h_s_s.append(eq)
            decode_h_s_s.append(decode+derate)

    for b, e in median_entries_h_s.items():
        decode = e[0]
        derate = e[1]
        demod = e[3]
        descr = e[2]
        eq = e[4]
        est = e[5]

        if "_l_" in b:
            demod_l_h_s.append(demod)
            descramb_l_h_s.append(descr)
            est_l_h_s.append(est)
            eq_l_h_s.append(eq)
            decode_l_h_s.append(decode+derate)
        else:
            demod_h_h_s.append(demod)
            descramb_h_h_s.append(descr)
            est_h_h_s.append(est)
            eq_h_h_s.append(eq)
            decode_h_h_s.append(decode+derate)
    
    x_axis = [f"{i} DUs" for i in dus]
    x_axis_shared = [f"{i} DUs" for i in dus[1:]]

    w, x, x_s = 0.3, np.arange(len(x_axis)), np.arange(len(x_axis_shared))

    demod_l_s = pad(demod_l_s)
    est_l_s = pad(est_l_s)
    eq_l_s = pad(eq_l_s)
    descramb_l_s = pad(descramb_l_s)
    decode_l_s = pad(decode_l_s)

    demod_h_s = pad(demod_h_s)
    est_h_s = pad(est_h_s)
    eq_h_s = pad(eq_h_s)
    descramb_h_s = pad(descramb_h_s)
    decode_h_s = pad(decode_h_s)

    demod_h_h = pad(demod_h_h)
    est_h_h = pad(est_h_h)
    eq_h_h = pad(eq_h_h)
    descramb_h_h = pad(descramb_h_h)
    decode_h_h = pad(decode_h_h)

    demod_l_h = pad(demod_l_h)
    est_l_h = pad(est_l_h)
    eq_l_h = pad(eq_l_h)
    descramb_l_h = pad(descramb_l_h)
    decode_l_h = pad(decode_l_h)

    demod_l_s_s = pad(demod_l_s_s)
    est_l_s_s = pad(est_l_s_s)
    eq_l_s_s = pad(eq_l_s_s)
    descramb_l_s_s = pad(descramb_l_s_s)
    decode_l_s_s = pad(decode_l_s_s)

    demod_h_s_s = pad(demod_h_s_s)
    est_h_s_s = pad(est_h_s_s)
    eq_h_s_s = pad(eq_h_s_s)
    descramb_h_s_s = pad(descramb_h_s_s)
    decode_h_s_s = pad(decode_h_s_s)

    demod_h_h_s = pad(demod_h_h_s)
    est_h_h_s = pad(est_h_h_s)
    eq_h_h_s = pad(eq_h_h_s)
    descramb_h_h_s = pad(descramb_h_h_s)
    decode_h_h_s = pad(decode_h_h_s)

    demod_l_h_s = pad(demod_l_h_s)
    est_l_h_s = pad(est_l_h_s)
    eq_l_h_s = pad(eq_l_h_s)
    descramb_l_h_s = pad(descramb_l_h_s)
    decode_l_h_s = pad(decode_l_h_s)

    fig, ax = plt.subplots()
    ax.bar(x - w/2, eq_l_h[:-1], width=w, label='Channel Equalisation', edgecolor='black', color='black')
    ax.bar(x - w/2, descramb_l_h[:-1], width=w, label='Descrambling', bottom=eq_l_h[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, demod_l_h[:-1], width=w, label='Demodulation', bottom=eq_l_h[:-1]+descramb_l_h[:-1], edgecolor='black', color='white')
    ax.bar(x - w/2, est_l_h[:-1], width=w, label='Channel Estimation', bottom=eq_l_h[:-1]+demod_l_h[:-1]+descramb_l_h[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x - w/2, decode_l_h[:-1], width=w, label='Decode+RateDematch', bottom=eq_l_h[:-1]+descramb_l_h[:-1]+est_l_h[:-1]+demod_l_h[:-1], edgecolor='black', color='dimgrey')

    ax.bar(x + w/2, eq_l_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, descramb_l_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, demod_l_s[:-1], width=w, label='_nolegend_',bottom=eq_l_s[:-1]+descramb_l_s[:-1], color='white', edgecolor='black')
    ax.bar(x + w/2, est_l_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s[:-1]+demod_l_s[:-1]+descramb_l_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x + w/2, decode_l_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s[:-1]+descramb_l_s[:-1]+est_l_s[:-1]+demod_l_s[:-1], edgecolor='black', color='dimgrey')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Time (us)')
    ax.legend()

    plt.savefig('/home/fatim/fatim/plots/PUSCH_LOW.png')

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - w/2, eq_h_h[:-1], width=w, label='Channel Equalisation', edgecolor='black', color='black')
    ax.bar(x - w/2, descramb_h_h[:-1], width=w, label='Descrambling', bottom=eq_h_h[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x - w/2, demod_h_h[:-1], width=w, label='Demodulation', bottom=eq_h_h[:-1]+descramb_h_h[:-1], edgecolor='black', color='white')
    ax.bar(x - w/2, est_h_h[:-1], width=w, label='Channel Estimation', bottom=eq_h_h[:-1]+demod_h_h[:-1]+descramb_h_h[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x - w/2, decode_h_h[:-1], width=w, label='Decode+RateDematch', bottom=eq_h_h[:-1]+descramb_h_h[:-1]+est_h_h[:-1]+demod_h_h[:-1], edgecolor='black', color='dimgrey')

    ax.bar(x + w/2, eq_h_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x + w/2, descramb_h_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x + w/2, demod_h_s[:-1], width=w, label='_nolegend_',bottom=eq_h_s[:-1]+descramb_h_s[:-1], color='white', edgecolor='black')
    ax.bar(x + w/2, est_h_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s[:-1]+demod_h_s[:-1]+descramb_h_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x + w/2, decode_h_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s[:-1]+descramb_h_s[:-1]+est_h_s[:-1]+demod_h_s[:-1], edgecolor='black', color='dimgrey')

    ax.set_xticks(x)
    ax.set_xticklabels(x_axis)
    ax.set_ylabel('Time (us)')
    ax.set_xlabel('DUs')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=14)
    plt.figtext(
        0.62, 0.55,
        "Hardware = Left Bar \nSoftware = Right Bar",
        ha="left",
        fontsize=14
    )
    plt.tight_layout()
    plt.savefig('/home/fatim/fatim/plots/PUSCH_HIGH.png')

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, eq_l_h_s[:-1], width=w, label='Channel Equalisation', edgecolor='black', color='black')
    ax.bar(x_s - w/2, descramb_l_h_s[:-1], width=w, label='Descrambling', bottom=eq_l_h_s[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x_s - w/2, demod_l_h_s[:-1], width=w, label='Demodulation', bottom=eq_l_h_s[:-1]+descramb_l_h_s[:-1], edgecolor='black', color='white')
    ax.bar(x_s - w/2, est_l_h_s[:-1], width=w, label='Channel Estimation', bottom=eq_l_h_s[:-1]+demod_l_h_s[:-1]+descramb_l_h_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x_s - w/2, decode_l_h_s[:-1], width=w, label='Decode+RateDematch', bottom=eq_l_h_s[:-1]+demod_l_h_s[:-1]+descramb_l_h_s[:-1]+est_l_h_s[:-1], edgecolor='black', color='dimgrey')

    ax.bar(x_s + w/2, eq_l_s_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x_s + w/2, descramb_l_s_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x_s + w/2, demod_l_s_s[:-1], width=w, label='_nolegend_',bottom=eq_l_s_s[:-1]+descramb_l_s_s[:-1], color='white', edgecolor='black')
    ax.bar(x_s + w/2, est_l_s_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s_s[:-1]+demod_l_s_s[:-1]+descramb_l_s_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x_s + w/2, decode_l_s_s[:-1], width=w, label='_nolegend_', bottom=eq_l_s_s[:-1]+demod_l_s_s[:-1]+descramb_l_s_s[:-1]+est_l_s_s[:-1], edgecolor='black', color='dimgrey')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Time (us)')
    ax.legend()
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/plots/PUSCH_SHARED_LOW.png')

    fig, ax = plt.subplots()

    ax.bar(x_s - w/2, eq_h_h_s[:-1], width=w, label='Channel Equalisation', edgecolor='black', color='black')
    ax.bar(x_s - w/2, descramb_h_h_s[:-1], width=w, label='Descrambling', bottom=eq_h_h_s[:-1], edgecolor='black', color='lightgrey')
    ax.bar(x_s - w/2, demod_h_h_s[:-1], width=w, label='Demodulation', bottom=eq_h_h_s[:-1]+descramb_h_h_s[:-1], edgecolor='black', color='white')
    ax.bar(x_s - w/2, est_h_h_s[:-1], width=w, label='Channel Estimation', bottom=eq_h_h_s[:-1]+demod_h_h_s[:-1]+descramb_h_h_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x_s - w/2, decode_h_h_s[:-1], width=w, label='Decode+RateDematch', bottom=eq_h_h_s[:-1]+demod_h_h_s[:-1]+descramb_h_h_s[:-1]+est_h_h_s[:-1], edgecolor='black', color='dimgrey')

    ax.bar(x_s + w/2, eq_h_s_s[:-1], width=w, label='_nolegend_', edgecolor='black', color='black')
    ax.bar(x_s + w/2, descramb_h_s_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s_s[:-1], color='lightgrey',edgecolor='black')
    ax.bar(x_s + w/2, demod_h_s_s[:-1], width=w, label='_nolegend_',bottom=eq_h_s_s[:-1]+descramb_h_s_s[:-1], color='white', edgecolor='black')
    ax.bar(x_s + w/2, est_h_s_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s_s[:-1]+demod_h_s_s[:-1]+descramb_h_s_s[:-1], edgecolor='black', color='white', hatch="x")
    ax.bar(x_s + w/2, decode_h_s_s[:-1], width=w, label='_nolegend_', bottom=eq_h_s_s[:-1]+demod_h_s_s[:-1]+descramb_h_s_s[:-1]+est_h_s_s[:-1], edgecolor='black', color='dimgrey')

    ax.set_xticks(x_s)
    ax.set_xticklabels(x_axis_shared)
    ax.set_ylabel('Time (us)')
    ax.legend()
    plt.tight_layout()

    plt.savefig('/home/fatim/fatim/plots/PUSCH_SHARED_HIGH.png')

def encoderdecoder():
    software_enc = defaultdict(lambda: [0]*5)
    hardware_enc = defaultdict(lambda: [0]*5)
    software_dec = defaultdict(lambda: [0]*5)
    hardware_dec = defaultdict(lambda: [0]*5)

    software_enc_s = defaultdict(lambda: [0]*5)
    hardware_enc_s = defaultdict(lambda: [0]*5)
    software_dec_s = defaultdict(lambda: [0]*5)
    hardware_dec_s = defaultdict(lambda: [0]*5)

    for k,v in metrics.items():
        du = 0
        for i in dus:
            if str(i) in k:
                du = i
                break
        load = ""
        if "_l_" in k:
            load = "l"
        else:
            load = "h"
        if "_s." in k:
            if "sw" in k:
                software_enc_s[load][dus.index(i)] = np.mean([x["encoder"]["avg_latency"] + x["rate"]["avg_latency"] for x in metrics[k] ])
                software_dec_s[load][dus.index(i)] = np.mean([x["decoder"]["avg_latency"] + x["derate"]["avg_latency"] for x in metrics[k] ])
            else:
                hardware_enc_s[load][dus.index(i)] = np.mean([x["encoder"]["avg_latency"] for x in metrics[k] ])
                hardware_dec_s[load][dus.index(i)] = np.mean([x["decoder"]["avg_latency"] for x in metrics[k] ])
        else:
            if "sw" in k:
                software_enc[load][dus.index(i)] = np.mean([x["encoder"]["avg_latency"] + x["rate"]["avg_latency"] for x in metrics[k] ])
                software_dec[load][dus.index(i)] = np.median([x["decoder"]["avg_latency"] + x["derate"]["avg_latency"] for x in metrics[k] ])
            else:
                hardware_enc[load][dus.index(i)] = np.mean([x["encoder"]["avg_latency"] for x in metrics[k] ])
                hardware_dec[load][dus.index(i)] = np.mean([x["decoder"]["avg_latency"] for x in metrics[k] ])

    print(hardware_enc_s)
    print(hardware_enc)

    fig, axes = plt.subplots(2, 2, figsize=(10, 4), sharey=True)
    axes[0,0].plot(dus, hardware_enc["h"], label="Hardware (High Load)", color="black")
    axes[0,0].plot(dus, software_enc["h"], label="Software (High Load)", color="darkgrey")
    axes[0,0].plot(dus, hardware_enc["l"], label="Hardware (Low Load)", marker="x", color="black")
    axes[0,0].plot(dus, software_enc["l"], label="Software (Low Load)", marker="x", color="darkgrey")
    axes[0,0].set_xticks(dus)
    axes[0,0].set_xlabel("DUs")
    axes[0,0].set_ylabel(f"Latency (us)")
    axes[0,0].set_title(f"Encoder Latency")

    axes[0,1].plot(dus, hardware_dec["h"], label="Hardware (High Load)", color="black")
    axes[0,1].plot(dus, software_dec["h"], label="Software (High Load)", color="darkgrey")
    axes[0,1].plot(dus, hardware_dec["l"], label="Hardware (Low Load)", marker="x", color="black")
    axes[0,1].plot(dus, software_dec["l"], label="Software (Low Load)", marker="x", color="darkgrey")
    axes[0,1].set_xticks(dus)
    axes[0,1].set_xlabel("DUs")
    axes[0,1].legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
    axes[0,1].set_title(f"Decoder Latency")

    axes[1,0].plot(dus, hardware_enc_s["h"], label="Hardware (High Load)", color="black")
    axes[1,0].plot(dus, software_enc_s["h"], label="Software (High Load)", color="darkgrey")
    axes[1,0].plot(dus, hardware_enc_s["l"], label="Hardware (Low Load)", marker="x", color="black")
    axes[1,0].plot(dus, software_enc_s["l"], label="Software (Low Load)", marker="x", color="darkgrey")
    axes[1,0].set_xticks(dus)
    axes[1,0].set_xlabel("DUs")
    axes[1,0].set_ylabel(f"Latency (us)")
    axes[1,0].set_title(f"Encoder Latency (Shared Cores)")

    axes[1,1].plot(dus, hardware_dec_s["h"], label="Hardware (High Load)", color="black")
    axes[1,1].plot(dus, software_dec_s["h"], label="Software (High Load)", color="darkgrey")
    axes[1,1].plot(dus, hardware_dec_s["l"], label="Hardware (Low Load)", marker="x", color="black")
    axes[1,1].plot(dus, software_dec_s["l"], label="Software (Low Load)", marker="x", color="darkgrey")
    axes[1,1].set_xticks(dus)
    axes[1,1].set_xlabel("DUs")
    axes[1,1].set_title(f"Decoder Latency (Shared Cores)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('/home/fatim/fatim/plots/new/EncDec.png')

pusch_plot()
pdsch_plot()
encoderdecoder()