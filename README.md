# BIOS/UEFI Security Analysis Dashboard v2.0

A high-fidelity simulation and auditing framework designed for hardware security researchers to analyze the platform boot chain and identify firmware-level vulnerabilities.

## Core Capabilities
- **Boot Chain Auditing:** Step-by-step simulation of UEFI phases: **SEC (Security)**, **PEI (Pre-EFI Init)**, **DXE (Driver Execution)**, and **BDS (Boot Dev Select)**.
- **CHIPSEC Integration:** Automated platform security assessment covering **SMM_BWP**, **SPI Write Protection**, and **Secure Boot** configuration[cite: 2, 4].
- **Threat Intelligence:** Real-time detection of **UEFI Bootkits** (e.g., BlackLotus) and **SMM Rootkits** through signature matching and PCR attestation.
- **Anti-Forensic Analysis:** Integrated firmware dump inspection and hex viewer for identifying unauthorized code injections.
- **Dynamic Risk Scoring:** Algorithmic security scoring (0-100) based on NIST-aligned platform hardening standards.

## Technical Stack
- **Frontend:** HTML5, CSS3 (Cyber-grid theme), JavaScript (Smart Simulation Engine)[cite: 4].
- **Backend:** Python 3, PyQt5 (Desktop Application Framework)[cite: 4].
- **Engine:** QtWebEngine for high-performance dashboard rendering[cite: 4].

## How to Run
1. **Install Dependencies:**
   ```bash
   pip install PyQt5 PyQtWebEngine
Execute the Analyzer:

Bash
python main.py
