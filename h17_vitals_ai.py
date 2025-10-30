#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract vital signs from HL7-like medical data
and analyze them using either OpenAI API (if available)
or local Ollama model (Llama 3) if offline or no quota.

Author: Swam Htet Zayar
"""

import json
import subprocess

try:
    from openai import OpenAI
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Optional if you ever add billing
    use_openai = True
except Exception:
    use_openai = False


# ---------------------- SAMPLE HL7 DATA ----------------------
hl7_data = """
OBX|1|ST|150456^MDC PULS_OXIM_SAT_02^MDC|1.1.1.1|100|%^%^UCUMIIIIIF||
OBX|2|ST|150488^MDC BLD PERF INDEX^MDC|1.1.1.1|3.46|%^%^UCUMIIIIIFIII||
OBX|3|ST|149530^MDC_PULS_OXIM_PULS_RATE^MDC|1.1.1.1|83|{beats>/min^UCUM||
OBX|4|ST|150344^MDC_TEMP~MDC|1.1.1.1|36.4|Cel^Cel~UCUM||
OBX|5|ST|151562^MDC_RESP_RATE^MDC|1.1.1.1|50|{breaths>/min^UCUM||
"""

# ---------------------- STEP 1: PARSE HL7 DATA ----------------------
vitals = {}

for line in hl7_data.splitlines():
    if line.startswith("OBX"):
        parts = line.split('|')
        if len(parts) < 6:
            continue
        test_name = parts[3].upper()
        value = parts[5].strip()
        if "TEMP" in test_name:
            vitals["Temperature (°C)"] = value
        elif "PULS_RATE" in test_name:
            vitals["Pulse Rate (bpm)"] = value
        elif "RESP_RATE" in test_name:
            vitals["Respiration Rate (breaths/min)"] = value
        elif "SAT_02" in test_name or "OXYM_SAT" in test_name:
            vitals["Oxygen Saturation (%)"] = value
        elif "PERF INDEX" in test_name:
            vitals["Perfusion Index (%)"] = value

# Save parsed vitals to JSON
with open("vitals.json", "w") as f:
    json.dump(vitals, f, indent=4)

print("✅ Extracted vital signs saved to vitals.json")

# ---------------------- STEP 2: BUILD PROMPT ----------------------
prompt = f"""
You are a medical AI assistant.
Analyze the following patient vital signs and summarize:
1. Whether each value is within normal range
2. Any possible abnormalities
3. Recommendations or next steps

Vital signs data:
{json.dumps(vitals, indent=2)}
"""

# ---------------------- STEP 3: ANALYZE USING AI ----------------------
def analyze_with_openai(prompt):
    """Use OpenAI API (if available and quota exists)."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("⚠️ OpenAI API not available:", e)
        return None


def analyze_with_ollama(prompt):
    """Use local Ollama model (Llama 3) as fallback."""
    print("💻 Using local Llama 3 model via Ollama...")
    response = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return response.stdout.strip()


# Try OpenAI first, fallback to Ollama if fails
if use_openai:
    analysis = analyze_with_openai(prompt)
    if not analysis:
        analysis = analyze_with_ollama(prompt)
else:
    analysis = analyze_with_ollama(prompt)

# ---------------------- STEP 4: DISPLAY OUTPUT ----------------------
print("\n🤖 AI Analysis:\n")
print(analysis)
