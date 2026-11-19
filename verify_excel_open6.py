import win32com.client, os

file_path = os.path.abspath(r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\output_6.대기_방지시설_운영현황(26년_10월_31일).xlsm")

print(f"Testing opening XLSM file with Excel COM Automation: {file_path}")
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

try:
    wb = excel.Workbooks.Open(file_path)
    print("SUCCESS: Workbook opened cleanly with 0 errors!")
    ws_main = wb.Sheets("6-대기 방지시설 운영현황")
    print(f"Main sheet max row: {ws_main.UsedRange.Rows.Count}")
    print(f"Cell (5,1) [20261001 1st fac]: date={ws_main.Cells(5,1).Value}, code={ws_main.Cells(5,4).Value}, hrs={ws_main.Cells(5,7).Value}, kwh={ws_main.Cells(5,9).Value}")
    print(f"Cell (934,1) [20261031 last fac]: date={ws_main.Cells(934,1).Value}, code={ws_main.Cells(934,4).Value}, hrs={ws_main.Cells(934,7).Value}, kwh={ws_main.Cells(934,9).Value}")
    wb.Close(False)
except Exception as e:
    print(f"FAILED: Error opening file: {e}")
finally:
    excel.Quit()
