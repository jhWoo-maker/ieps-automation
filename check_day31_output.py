import openpyxl

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\output_october_31days.xlsm"
wb = openpyxl.load_workbook(path, data_only=True)
ws_sheet1 = wb["Sheet1"]

print("Row 8462 (Last row of day 30):", [ws_sheet1.cell(8462, col).value for col in (1, 2, 4, 5, 9, 12, 13)])
print("Row 8463 (First row of day 31):", [ws_sheet1.cell(8463, col).value for col in (1, 2, 4, 5, 9, 12, 13)])
print("Row 8744 (Last row of day 31):", [ws_sheet1.cell(8744, col).value for col in (1, 2, 4, 5, 9, 12, 13)])
