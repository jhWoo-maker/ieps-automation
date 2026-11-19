import openpyxl

xlsm_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\template_4_facility_status.xlsm"
xlsx_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\template_4_facility_status.xlsx"

wb = openpyxl.load_workbook(xlsm_path, data_only=False)

# Save as .xlsx (openpyxl automatically strips VBA macros and saves pure xlsx XML)
wb.save(xlsx_path)
print(f"Successfully converted template to pure XLSX: {xlsx_path}")
