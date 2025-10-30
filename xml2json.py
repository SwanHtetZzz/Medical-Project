#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 17:17:03 2025

@author: theintthu
"""

import xmltodict
import json

# --- Step 1: Read XML file ---
with open("test.xml", "r") as xml_file:
    xml_data = xml_file.read()

# --- Step 2: Convert XML to Python dictionary ---
dict_data = xmltodict.parse(xml_data)

# --- Step 3: Convert dictionary to JSON string ---
json_data = json.dumps(dict_data, indent=4)

# --- Step 4: Save JSON to a file ---
with open("data.json", "w") as json_file:
    json_file.write(json_data)

print("✅ XML file has been successfully converted to JSON format!")
