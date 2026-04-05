Profiling and Analysis Framework
# Overview
This repository contains the profiling, data collection, and analysis framework developed for my BSc thesis:

**“System-Level Analysis of Hardware Offloading in High-Performance Open RAN Deployments”**

It supports system-level evaluation of performance, scalability, and energy efficiency in Open RAN deployments using srsRAN Project.

## Features
- Python-based analysis and plotting
- Raw and processed experiment datasets

## Repository Structure
/analysis_scripts/ # Contains analysis scripts for each experiment, producing plots. Also contains script to analyse the results of eBPF scripts.
/concur_logs/ # Raw experiment logs from channel concurrency and parsed srsran logs
/smtpaired_logs/ # Raw experiment logs from smt enabled with sibling cores paired and parsed srsran logs
/smtcompete_logs/ # Raw experiment logs from csmt enabled with sibling cores competeing and parsed srsran logs
/loadtesting_logs/ # Raw experiment logs from load testing and parsed srsran logs
/mcs_logs/ # Raw experiment logs from mcs and parsed srsran logs
/iter_logs/ # Raw experiment logs from LDPC decoder iteration and parsed srsran logs
/trace_logs/ # Raw experiment logs from trace CQI patterns and parsed srsran logs
/prb_logs/ # Raw experiment logs from PRB and parsed srsran logs
/realue_logs/ # Raw experiment logs from real UE and parsed srsran logs
/e2e_logs/ # Raw experiment logs from end-to-end and parsed srsran logs
/no_logs/ # Raw experiment logs from no logging and parsed srsran logs
/old_logs/ # Raw experiment logs from per-function-call logging method and parsed srsran logs
/plots/ # Containing all plots shown in thesis and additional plots



