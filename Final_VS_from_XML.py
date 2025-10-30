#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 18:35:40 2025

@author: theintthu
"""

import re

# HL7-like data
hl7_data = """
OBR|1|1^1^1^IS0|1^1^1^ISOIVITALS^Vital Signs^VSMI||20250625114042.0000+0500|20250625114236.0000+0500
OBX|1|ST|150456^MDC PULS_OXIM_SAT_02^MDC|1.1.1.1|100|%^%^UCUMIIIIIF||20250625114236.0000+0500|11/00:40:97:6l
OBX|2|ST|150488^MDC BLD PERF INDEX^MDC|1.1.1.1|3.46|%^%^UCUMIIIIIFIII20250625114236.0000+0500||1/00:40:97:6b:2
OBX|3|ST|149530^MDC_PULS_OXIM_PULS_RATE^MDC|1.1.1.1|83|{beats>/min^{beats›/min^UCUM|I|I|F|I|20250625114236.0000
OBX|4|ST|150344^MDC_TEMP~MDC|1.1.1.1|36.4|Cel^Cel~UCUMIIIIIF|I|20250625114049.0000+0500|1/100:40:97:6b:25:59|/460
OBX|5|ST|151562^MDC_RESP_RATE^MDC|1.1.1.1|50|{breaths>/min^{breaths>/min^UCUM|I|I|F|||20250625114042.0000+0500|1
"""

# Initialize dictionary for vital signs
vitals = {}

# Process each line
for line in hl7_data.splitlines():
    if line.startswith("OBX"):
        parts = line.split('|')
        if len(parts) < 6:
            continue
        test_name = parts[3].upper()
        value = parts[5].strip()

        # Identify and extract each vital
        if "TEMP" in test_name:
            vitals["Temp"] = f"{value} °C"
        elif "PULS_RATE" in test_name or "PULS_OXIM_PULS_RATE" in test_name:
            vitals["Pulse"] = value
        elif "RESP_RATE" in test_name:
            vitals["Resp"] = value
        elif "SAT_02" in test_name or "OXYM_SAT" in test_name:
            vitals["O2 Sats"] = f"{value} %"
        elif "BLD PERF" in test_name or "PERF INDEX" in test_name:
            vitals["Blood PI"] = f"{value} %"

# Print formatted vital signs
print("Extracted Vital Signs:")
for key, val in vitals.items():
    print(f"{key}: {val}")
