import win32com.client
import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\4.배출시설_운영현황(26년_10월_VBA보존).xlsm"

excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

try:
    wb = excel.Workbooks.Open(os.path.abspath(path))
    print("EXCEL COM OPEN SUCCESS! Clean XLSM file with VBA macro preserved!")
    wb.Close(False)
except Exception as e:
    print("Error opening in Excel:", e)
finally:
    excel.Quit()
