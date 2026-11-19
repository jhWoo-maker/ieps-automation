import openpyxl

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\template_4_facility_status.xlsm"
wb = openpyxl.load_workbook(file_path, data_only=True)
ws_main = wb["4-배출시설운영사항"]

print("4-배출시설운영사항 Dimensions:", ws_main.max_row, "rows,", ws_main.max_column, "cols")
headers = [ws_main.cell(1, col).value for col in range(1, ws_main.max_column + 1)]
print("\nHeaders (Row 1):", headers)

print("\nSample Rows 2..6:")
for r in range(2, 7):
    row_vals = [ws_main.cell(r, col).value for col in range(1, ws_main.max_column + 1)]
    print(f"Row {r}:", row_vals)
