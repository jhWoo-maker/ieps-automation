import openpyxl

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\template_4_facility_status.xlsm"
wb = openpyxl.load_workbook(file_path, data_only=True)
ws_sheet1 = wb["Sheet1"]
ws_main = wb["4-배출시설운영사항"]

print("Sheet1 max_row:", ws_sheet1.max_row)
print("4-배출시설운영사항 max_row:", ws_main.max_row)

print("\nChecking repeating 282 facility metadata template in Sheet1 (rows 3..284):")
sample_facilities = []
for r in range(3, 285):
    fac_code = ws_sheet1.cell(r, 4).value
    fac_name = ws_sheet1.cell(r, 5).value
    sample_facilities.append((fac_code, fac_name))

print(f"Total 282 facility block length: {len(sample_facilities)}")
print("First 3 facilities:", sample_facilities[:3])
print("Last 3 facilities:", sample_facilities[-3:])
