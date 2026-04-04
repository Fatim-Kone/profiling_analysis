import re
import sys
import statistics
from collections import defaultdict
from datetime import datetime
import json
import os

jobs_n = [1, 2, 4, 6, 8]
mode = ["h", "l"]

def parse_time_us(time_str):
        """Extract time in microseconds from string like 't=43.4us'"""
        match = re.search(r't=(\d+\.?\d*)us', time_str)
        if match:
            return float(match.group(1))
        return None
    
def parse_sinr(line):
    """Extract SINR in dB"""
    match = re.search(r'sinr=(-?\d+\.?\d*)dB', line)
    if match:
        return float(match.group(1))
    return None

def parse_prb(line):
        """Extract number of PRBs"""
        match = re.search(r'prb=\[(\d+),\s*(\d+)\)', line)
        if match:
            return int(match.group(2)) - int(match.group(1))
        return None

def parse_iter(line):
        """Extract decoder iterations"""
        match = re.search(r'iter=(\d+\.?\d*)', line)
        if match:
            return float(match.group(1))
        return None
    
def parse_tbs(line):
    """Extract TBS (transport block size)"""
    match = re.search(r'tbs=(\d+)', line)
    if match:
        return int(match.group(1))
    return None
    
def parse_mod(line):
        """Extract modulation scheme"""
        match = re.search(r'mod=(\w+)', line)
        if match:
            return match.group(1)
        return None

def parse_timestamp(line):
    """Extract timestamp"""
    match = re.match(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+)', line)
    if match:
        return match.group(1)
    return None

def parse_mean_latency(line):
    """Extract mean latency time"""
    match = re.search(r'mean_latency=(\d+\.?\d*)usec', line)
    if match:
        return float(match.group(1))
    return None

def parse_max_latency(line):
    """Extract max latency time"""
    match = re.search(r'max_latency=(\d+\.?\d*)usec', line)
    if match:
        return float(match.group(1))
    return None

def parse_latency_hist(line):
    """Extract latency histogram """
    match = re.search(r'latency_hist=(\[[^\]]*\])', line)
    if match:
        return eval(match.group(1))
    return None

def parse_dl_ok(line):
    """Extract ok"""
    match = re.search(r'dl_nof_ok=(\d+\.?\d*)', line)
    if match:
        return int(match.group(1))
    return None

def parse_ul_ok(line):
    """Extract ok"""
    match = re.search(r'ul_nof_ok=(\d+\.?\d*)', line)
    if match:
        return int(match.group(1))
    return None

def parse_dl_nok(line):
    """Extract nok"""
    match = re.search(r'dl_nof_nok=(\d+\.?\d*)', line)
    if match:
        return int(match.group(1))
    return None

def parse_ul_nok(line):
    """Extract nok"""
    match = re.search(r'ul_nof_nok=(\d+\.?\d*)', line)
    if match:
        return int(match.group(1))
    return None

def parse_prbs(line):
    """Extract PRBs"""
    match = re.search(r'nof_prbs=(\d+\.?\d*)', line)
    if match:
        return int(match.group(1))
    return None

def parse_dl_brate(line):
    """Extract Downlink Bitrate"""
    match = re.search(r'dl_brate=(\d+\.?\d*)(.)bps', line)
    if match:
        if (match.group(2) == "M"):
            return float(match.group(1)) 
        elif (match.group(2) == "K"):
            return float(match.group(1)) / 1024 
        elif (match.group(2) == "G"):
            return float(match.group(1)) * 1024 
    return None

def parse_ul_brate(line):
    """Extract Uplink Bitrate"""
    match = re.search(r'ul_brate=(\d+\.?\d*)(.)bps', line)
    if match:
        if (match.group(2) == "M"):
            return float(match.group(1))
        elif (match.group(2) == "K"):
            return float(match.group(1)) / 1024
        elif (match.group(2) == "G"):
            return float(match.group(1)) * 1024
    return None

def parse_phy(line):
    entry = {}
    dl_processing_max_latency = re.search(r'dl_processing_max_latency=(\d+\.?\d*)', line)
    if dl_processing_max_latency:
        entry["dl_max_latency"] = float(dl_processing_max_latency.group(1))
    ul_processing_max_latency = re.search(r'ul_processing_max_latency=(\d+\.?\d*)', line)
    if ul_processing_max_latency:
        entry["ul_max_latency"] = float(ul_processing_max_latency.group(1))
    dl_processing_avg_latency = re.search(r'dl_processing_avg_latency=(\d+\.?\d*)', line)
    if dl_processing_avg_latency:
        entry["dl_avg_latency"] = float(dl_processing_avg_latency.group(1))
    ul_processing_avg_latency = re.search(r'ul_processing_avg_latency=(\d+\.?\d*)', line)
    if ul_processing_avg_latency:
        entry["ul_avg_latency"] = float(ul_processing_avg_latency.group(1))
    return entry

def parse_ldpc(line):
    entry = {}
    cb_size = re.search(r'avg_cb_size=(\d+\.?\d*)', line)
    if cb_size:
        entry["b_size"] = float(cb_size.group(1))
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    max_latency = re.search(r'max_latency=(\d+\.?\d*)', line)
    if max_latency:
        entry["max_latency"] = float(max_latency.group(1))
    rate = re.search(r'code_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    avg_nof_cbs = re.search(r'avg_nof_cbs=(\d+\.?\d*)', line)
    if avg_nof_cbs:
        entry["avg_nof_cbs"] = float(avg_nof_cbs.group(1))
    if "Decoder" in line:
        nof_iter = re.search(r'avg_nof_iter=(\d+\.?\d*)', line)
        if nof_iter:
            entry["nof_iter"] = float(nof_iter.group(1))
    return entry

def parse_rate(line):
    entry = {}
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    max_latency = re.search(r'max_latency=(\d+\.?\d*)', line)
    if max_latency:
        entry["max_latency"] = float(max_latency.group(1))
    rate = re.search(r'proc_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    return entry

def parse_estimator(line):
    entry = {}
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    rate = re.search(r'proc_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    return entry

def parse_equalizer(line):
    entry = {}
    proc_rate = re.search(r'proc_rate_per_nof_layers=(\[[^\]]*\])', line)
    if proc_rate:
        entry["proc_rate_per_nof_layers"] = eval(proc_rate.group(1))
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    return entry

def parse_scramb(line):
    entry = {}
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    avg_init_time = re.search(r'avg_init_time=(\d+\.?\d*)', line)
    if avg_init_time:
        entry["avg_init_time"] = float(avg_init_time.group(1))
    avg_advance_rate = re.search(r'avg_advance_rate=(\d+\.?\d*)', line)
    if avg_advance_rate:
        entry["avg_advance_rate"] = float(avg_advance_rate.group(1))
    avg_gen_rate = re.search(r'avg_gen_rate=(\d+\.?\d*)', line)
    if avg_gen_rate:
        entry["avg_gen_rate"] = float(avg_gen_rate.group(1))
    return entry

def parse_modulation(line):
    entry = {}
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    qpsk = re.search(r'QPSK=(\d+\.?\d*)', line)
    if qpsk:
        entry["qpsk"] = float(qpsk.group(1))
    qam16 = re.search(r'16QAM=(\d+\.?\d*)', line)
    if qam16:
        entry["qam16"] = float(qam16.group(1))
    qam64 = re.search(r'64QAM=(\d+\.?\d*)', line)
    if qam64:
        entry["qam64"] = float(qam64.group(1))
    qam256 = re.search(r'256QAM=(\d+\.?\d*)', line)
    if qam256:
        entry["qam256"] = float(qam256.group(1))
    return entry

def parse_demux(line):
    entry = {}
    avg_init_time = re.search(r'avg_init_time=(\d+\.?\d*)', line)
    if avg_init_time:
        entry["avg_init_time"] = float(avg_init_time.group(1))
    avg_finish_time = re.search(r'avg_finish_time=(\d+\.?\d*)', line)
    if avg_finish_time:
        entry["avg_finish_time"] = float(avg_finish_time.group(1))
    rate = re.search(r'proc_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    return entry

def parse_pusch(line):
    entry = {}
    avg_data_latency = re.search(r'avg_data_latency=(\d+\.?\d*)', line)
    if avg_data_latency:
        entry["avg_data_latency"] = float(avg_data_latency.group(1))
    avg_uci_latency = re.search(r'avg_uci_latency=(\d+\.?\d*)', line)
    if avg_uci_latency:
        entry["avg_uci_latency"] = float(avg_uci_latency.group(1))
    rate = re.search(r'proc_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    return entry

def parse_pdsch(line):
    entry = {}
    avg_latency = re.search(r'avg_latency=(\d+\.?\d*)', line)
    if avg_latency:
        entry["avg_latency"] = float(avg_latency.group(1))
    max_latency = re.search(r'max_latency=(\d+\.?\d*)', line)
    if max_latency:
        entry["max_latency"] = float(max_latency.group(1))
    rate = re.search(r'proc_rate=(\d+\.?\d*)', line)
    if rate:
        entry["rate"] = float(rate.group(1))
    return entry

def parse_pusch_cpu(line):
    entry = {}
    upper_phy_ul = re.search(r'upper_phy_ul=(\d+\.?\d*)', line)
    if upper_phy_ul:
        entry["upper_phy_ul"] = float(upper_phy_ul.group(1))
    ul_fec = re.search(r'ul_fec=(\d+\.?\d*)', line)
    if ul_fec:
        entry["ul_fec"] = float(ul_fec.group(1))
    ldpc_dec = re.search(r'ldpc_dec=(\d+\.?\d*)', line)
    if ldpc_dec:
        entry["ldpc_dec"] = float(ldpc_dec.group(1))
    ldpc_rdm = re.search(r'ldpc_rdm=(\d+\.?\d*)', line)
    if ldpc_rdm:
        entry["ldpc_rdm"] = float(ldpc_rdm.group(1))
    pusch_scrambling = re.search(r'pusch_scrambling=(\d+\.?\d*)', line)
    if pusch_scrambling:
        entry["descarmbling"] = float(pusch_scrambling.group(1))
    demod_mapper = re.search(r'demod_mapper=(\d+\.?\d*)', line)
    if demod_mapper:
        entry["demod_mapper"] = float(demod_mapper.group(1))
    ul_precoding = re.search(r'ul_precoding=(\d+\.?\d*)', line)
    if ul_precoding:
        entry["ul_precoding"] = float(ul_precoding.group(1))
    return entry

def parse_pdsch_cpu(line):
    entry = {}
    upper_phy_dl = re.search(r'upper_phy_dl=(\d+\.?\d*)', line)
    if upper_phy_dl:
        entry["upper_phy_dl"] = float(upper_phy_dl.group(1))
    fec = re.search(r'fec=(\d+\.?\d*)', line)
    if fec:
        entry["fec"] = float(fec.group(1))
    ldpc_enc = re.search(r'ldpc_enc=(\d+\.?\d*)', line)
    if ldpc_enc:
        entry["ldpc_enc"] = float(ldpc_enc.group(1))
    ldpc_rm = re.search(r'ldpc_rm=(\d+\.?\d*)', line)
    if ldpc_rm:
        entry["ldpc_rm"] = float(ldpc_rm.group(1))
    pdsch_scrambling = re.search(r'pdsch_scrambling=(\d+\.?\d*)', line)
    if pdsch_scrambling:
        entry["scarmbling"] = float(pdsch_scrambling.group(1))
    mod_mapper = re.search(r'mod_mapper=(\d+\.?\d*)', line)
    if mod_mapper:
        entry["mod_mapper"] = float(mod_mapper.group(1))
    dl_layer_map = re.search(r'dl_layer_map=(\d+\.?\d*)', line)
    if dl_layer_map:
        entry["dl_layer_map"] = float(dl_layer_map.group(1))
    return entry

def parse_number(v):
    if v.endswith('k'):
        return int(float(v[:-1]) * 1000)
    elif v.endswith('M'):
        return int(float(v[:-1]) * 1_000_000)
    else:
        return int(float(v))

def parse_rlc(line):
    entry = {}
    hist = re.search(r'pdu_latency_hist=(\[[^\]]*\])', line)
    if hist:
        hist = hist.group(1).strip("[]").split()
        entry["histogram"] = [parse_number(v) for v in hist]
    tx_rate = re.search(r'TX=\[num_sdus=[\d\.kMG]+.*?sdu_rate=\s*(\d+\.?\d*)([kMG]?)bps', line)
    if tx_rate:
        rate = 0
        if (tx_rate.group(2) == "M"):
            rate = float(tx_rate.group(1))
        elif (tx_rate.group(2) == "K"):
            rate = float(tx_rate.group(1)) / 1024
        elif (tx_rate.group(2) == "G"):
            rate = float(tx_rate.group(1)) * 1024
        entry["tx_rate"] = rate
    rx_rate = re.search(r'RX=\[num_sdus=[\d\.kMG]+.*?sdu_rate=\s*(\d+\.?\d*)([kMG]?)bps', line)
    if rx_rate:
        rate = 0
        if (rx_rate.group(2) == "M"):
            rate = float(rx_rate.group(1))
        elif (rx_rate.group(2) == "K"):
            rate = float(rx_rate.group(1)) / 1024
        elif (rx_rate.group(2) == "G"):
            rate = float(rx_rate.group(1)) * 1024
        entry["rx_rate"] = rate
    return entry

def parse_mac(line):
    entry = {}
    avg_latency = re.search(r'wall_clock_latency=\[avg=(\d+\.?\d*)usec', line)
    if avg_latency:
        entry["wall_latency"] = float(avg_latency.group(1))
    dl_latency = re.search(r'dl_tti_req_latency=\[avg=(\d+\.?\d*)usec', line)
    if dl_latency:
        entry["dl_tti_latency"] = float(dl_latency.group(1))
    ul_latency = re.search(r'ul_tti_req_latency=\[avg=(\d+\.?\d*)usec', line)
    if dl_latency:
        entry["ul_tti_latency"] = float(ul_latency.group(1))
    slot_indication = re.search(r'slot_ind_latency=\[avg=(\d+\.?\d*)usec', line)
    if slot_indication:
        entry["slot_ind_latency"] = float(slot_indication.group(1))
    return entry

def parse_log(log_file):
    """Parse the entire log file"""
    pdsch_entries = []
    pusch_entries = []
    metrics = []
    metric_cell = []
    upper_du_metrics = []
    du_ul_stuck = [0]*len(log_file)
    du_dl_stuck = [0]*len(log_file)
    
    for i,l in enumerate(log_file):
        ul_stuck = 0
        dl_stuck = 0
        pod = re.search(r'pod(\d+)', l)
        with open(l, 'r') as f:
            current_metrics = defaultdict()
            extract_metric = False
            for line in f:
                line = line.strip()
                if 'PDSCH:' in line and 'rnti=' in line and not extract_metric:
                    entry = {
                        't': parse_time_us(line),
                        'tbs': parse_tbs(line),
                        'mod': parse_mod(line),
                    }
                    if entry['t'] and entry['tbs'] and entry['mod']:
                        pdsch_entries.append(entry)
                
                elif 'PUSCH:' in line and 'rnti=' in line and not extract_metric:
                    entry = {
                        't': parse_time_us(line),
                        'tbs': parse_tbs(line),
                        'mod': parse_mod(line),
                        'sinr': parse_sinr(line),
                    }
                    if entry['t'] and entry['tbs']  and entry['mod']:
                        pusch_entries.append(entry)
                elif 'METRICS' in line and 'RLC Metrics' in line and not extract_metric:
                    upper_du_metrics.append(parse_rlc(line))
                elif 'METRICS' in line and 'MAC cell' in line and not extract_metric:  
                    upper_du_metrics.append(parse_mac(line))
                elif 'METRICS' in line and 'Scheduler UE' in line and not extract_metric:
                    entry = {
                        'dl_brate': parse_dl_brate(line),
                        'ul_brate': parse_ul_brate(line),
                        'dl_ok' : parse_dl_ok(line),
                        'dl_nok': parse_dl_nok(line),
                        'ul_ok' : parse_ul_ok(line),
                        'ul_nok': parse_ul_nok(line),
                    }
                    metric_cell.append(entry)
                elif 'Upper PHY sector#0 metrics:' in line and not extract_metric:
                    extract_metric = True
                    current_metrics = defaultdict()
                    current_metrics["phy"] = parse_phy(line)
                elif extract_metric:
                    if 'LDPC Encoder:' in line:
                        current_metrics["encoder"] = parse_ldpc(line)
                    elif 'LDPC Rate matcher:' in line:
                        current_metrics["rate"] = parse_rate(line)
                    elif 'LDPC Decoder:' in line:
                        current_metrics["decoder"] = parse_ldpc(line)
                    elif 'LDPC Rate dematcher:' in line:
                        current_metrics["derate"] = parse_rate(line)
                    elif 'PUSCH chan. estimator:' in line:
                        current_metrics["estimator"] = parse_estimator(line)
                    elif 'PUSCH chan. equalizer:' in line:
                        current_metrics["equalizer"] = parse_equalizer(line)
                    elif 'PDSCH scrambling:' in line:
                        current_metrics["scrambling"] = parse_scramb(line)
                    elif 'Modulation rates:' in line:
                        current_metrics["mod"] = parse_modulation(line)
                    elif 'Demodulation rates:' in line:
                        current_metrics["demod"] = parse_modulation(line)
                    elif 'PUSCH scrambling:' in line:
                        current_metrics["descrambling"] = parse_scramb(line)
                    elif 'UL-SCH demux:' in line:
                        current_metrics["demux"] = parse_demux(line)
                    elif 'PUSCH Processor:' in line:
                        current_metrics["pusch"] = parse_pusch(line)
                        if current_metrics["pusch"]["avg_data_latency"] == 0:
                            ul_stuck += 1
                    elif 'PDSCH Processor:' in line:
                        current_metrics["pdsch"] = parse_pdsch(line)
                        if current_metrics["pdsch"]["avg_latency"] == 0:
                            dl_stuck += 1
                    elif 'UL:' in line:
                        current_metrics["pusch_cpu"] = parse_pusch_cpu(line)
                        extract_metric = False
                        metrics.append(current_metrics)
                    elif 'DL:' in line:
                        current_metrics["pdsch_cpu"] = parse_pdsch_cpu(line)
        du_dl_stuck[i] = dl_stuck
        du_ul_stuck[i] = ul_stuck
    return {
        "file": log_file[0],
        "pdsch": pdsch_entries,
        "pusch": pusch_entries,
        "metrics": metrics,
        "metrics_cell": metric_cell,
        "upper_du_metrics": upper_du_metrics,
        "dl_stuck": du_dl_stuck,
        "ul_stuck": du_ul_stuck
    } 

def parse(dir):
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for m in mode:
            for job in jobs_n:
                if m == "l":
                    sw_log_files = []
                    hw_log_files = []
                    for i in range(job):
                        sw_log_files.append(f"{dir}sw{job}_l_pod{i}.log")
                        hw_log_files.append(f"{dir}hw{job}_l_pod{i}.log")
                    data = parse_log(sw_log_files)
                    out.write(json.dumps(data) + "\n")
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")
                else:
                    sw_log_files = []
                    hw_log_files = []
                    for i in range(job):
                        sw_log_files.append(f"{dir}sw{job}_h_pod{i}.log")
                        if job != 10:
                            hw_log_files.append(f"{dir}hw{job}_h_pod{i}.log")
                    data = parse_log(sw_log_files)
                    out.write(json.dumps(data) + "\n")
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for m in mode:
            for job in jobs_n[1:]:
                if m == "l":
                    sw_log_files = []
                    hw_log_files = []
                    for i in range(job):
                        sw_log_files.append(f"{dir}sw{job}_l_pod{i}_s.log")
                        hw_log_files.append(f"{dir}hw{job}_l_pod{i}_s.log")
                    data = parse_log(sw_log_files)
                    out.write(json.dumps(data) + "\n")
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")
                else:
                    sw_log_files = []
                    hw_log_files = []
                    for i in range(job):
                        sw_log_files.append(f"{dir}sw{job}_h_pod{i}_s.log")
                        if job != 10:
                            hw_log_files.append(f"{dir}hw{job}_h_pod{i}_s.log")
                    data = parse_log(sw_log_files)
                    out.write(json.dumps(data) + "\n")
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")

def prb_parse(dir):
    prbs = [50, 100, 200, 250]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for prb in prbs:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{prb}_pod{i}.log")
                    hw_log_files.append(f"{dir}hw{job}_{prb}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for prb in prbs:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{prb}_pod{i}_s.log")
                    hw_log_files.append(f"{dir}hw{job}_{prb}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

def mcs_parse(dir):
    mcs = [0, 4, 5, 10, 11, 19, 20, 27]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for m in mcs:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{m}_pod{i}.log")
                    hw_log_files.append(f"{dir}hw{job}_{m}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for m in mcs:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{m}_pod{i}_s.log")
                    hw_log_files.append(f"{dir}hw{job}_{m}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

def iter_parse(dir):
    iters = [2, 6, 4, 8, 10]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for iter in iters:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{iter}_pod{i}.log")
                    hw_log_files.append(f"{dir}hw{job}_{iter}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for iter in iters:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{iter}_pod{i}_s.log")
                    hw_log_files.append(f"{dir}hw{job}_{iter}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

def trace_parse(dir):
    tracefiles = ["cqi_trace_Ujwal_01012023_1.txt", "cqi_trace_Ujwal_01012023_2.txt",  "cqi_trace_Ujwal_triangular_01062023_1.txt", "out_mac_realistic_spin_cqi.txt", "cqi_car_20mph_3min.txt", "random_1.txt"]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for file in tracefiles:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{file}_pod{i}.log")
                    hw_log_files.append(f"{dir}hw{job}_{file}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for file in tracefiles:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{file}_pod{i}_s.log")
                    hw_log_files.append(f"{dir}hw{job}_{file}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

def concur_parse(dir):
    concurs = [0, 2, 4, 8, 12]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for concur in concurs:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{concur}_pod{i}.log")
                    if concur > 0:
                        hw_log_files.append(f"{dir}hw{job}_{concur}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                if concur > 0:
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for concur in concurs:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{concur}_pod{i}_s.log")
                    if concur > 0:
                        hw_log_files.append(f"{dir}hw{job}_{concur}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                if concur > 0:
                    data = parse_log(hw_log_files)
                    out.write(json.dumps(data) + "\n")

def realue_parse(dir):
    open(f"{dir}parsed_logs_dl.jsonl", "w").close()
    with open(f"{dir}parsed_logs_dl.jsonl", "a") as out:
        data = parse_log([f"{dir}sw_dl_gnb.log"])
        out.write(json.dumps(data) + "\n")
        data = parse_log([f"{dir}hw_dl_gnb.log"])
        out.write(json.dumps(data) + "\n")

    open(f"{dir}parsed_logs_ul.jsonl", "w").close()
    with open(f"{dir}parsed_logs_ul.jsonl", "a") as out:
        data = parse_log([f"{dir}sw_ul_gnb.log"])
        out.write(json.dumps(data) + "\n")
        data = parse_log([f"{dir}hw_ul_gnb.log"])
        out.write(json.dumps(data) + "\n")
    
    open(f"{dir}parsed_logs_udp.jsonl", "w").close()
    with open(f"{dir}parsed_logs_udp.jsonl", "a") as out:
        data = parse_log([f"{dir}sw_dl_udp_gnb.log"])
        out.write(json.dumps(data) + "\n")
        data = parse_log([f"{dir}hw_dl_udp_gnb.log"])
        out.write(json.dumps(data) + "\n")

def e2e_parse(dir):
    mode = ["ul", "dl"]
    open(f"{dir}parsed_logs.jsonl", "w").close()
    with open(f"{dir}parsed_logs.jsonl", "a") as out:
        for m in mode:
            for job in jobs_n:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{m}_pod{i}.log")
                    hw_log_files.append(f"{dir}hw{job}_{m}_pod{i}.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")


    open(f"{dir}parsed_logs_shared.jsonl", "w").close()
    with open(f"{dir}parsed_logs_shared.jsonl", "a") as out:
        for m in mode:
            for job in jobs_n[1:]:
                sw_log_files = []
                hw_log_files = []
                for i in range(job):
                    sw_log_files.append(f"{dir}sw{job}_{m}_pod{i}_s.log")
                    hw_log_files.append(f"{dir}hw{job}_{m}_pod{i}_s.log")
                data = parse_log(sw_log_files)
                out.write(json.dumps(data) + "\n")
                data = parse_log(hw_log_files)
                out.write(json.dumps(data) + "\n")

#realue_parse("/home/fatim/fatim/realue_logs/")
#prb_parse("/home/fatim/fatim/prb_logs/")
#concur_parse("/home/fatim/fatim/concur_logs/pusch/")
#concur_parse("/home/fatim/fatim/concur_logs/pdsch/")
#trace_parse("/home/fatim/fatim/trace_logs/")
#parse("/home/fatim/fatim/smtpaired_logs/")
#parse("/home/fatim/fatim/smtcompete_logs/")
parse("/home/fatim/fatim/loadtesting_logs/")
#iter_parse("/home/fatim/fatim/iter_logs/")
#mcs_parse("/home/fatim/fatim/mcs_logs/")
#e2e_parse("/home/fatim/fatim/e2e_logs/")
#parse("/home/fatim/fatim/no_logs/")
#parse("/home/fatim/fatim/old_logs/")