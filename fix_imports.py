app_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where the main logic starts after imports (e.g., "# Helper for Date & Facility Hours Editor UI" or "HOLIDAYS =")
cut_idx = 0
for i, line in enumerate(lines):
    if "# Helper for Date & Facility Hours Editor UI" in line or "HOLIDAYS = [" in line:
        cut_idx = i
        break

rest_of_code = "".join(lines[cut_idx:])

clean_imports = """import os
import io
import datetime
import calendar
import importlib
import pandas as pd
import streamlit as st

import fuel_consumption_processor
import facility_status_processor
import air_prevention_processor

importlib.reload(fuel_consumption_processor)
importlib.reload(facility_status_processor)
importlib.reload(air_prevention_processor)

from fuel_consumption_processor import generate_fuel_consumption_excel
from facility_status_processor import process_facility_status
from air_prevention_processor import process_air_prevention
from pdf_parser import parse_water_quality_pdf
from excel_updater import update_excel_with_pdf_data
from outlet_hours_processor import process_outlet_operating_hours, save_outlet_excel_file
from air_quality_pdf_parser import parse_air_quality_pdf
from air_quality_excel_updater import update_air_quality_excel

"""

full_code = clean_imports + rest_of_code

with open(app_path, "w", encoding="utf-8") as f:
    f.write(full_code)

print("Fixed imports in app.py successfully!")
