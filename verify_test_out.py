import openpyxl

print("=== Checking test_9_out.xlsx ===")
wb9 = openpyxl.load_workbook("test_9_out.xlsx", data_only=True)
ws9 = wb9["9-원부원료 사용량"]
for r in range(4, 12):
    row_vals = [ws9.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r}:", row_vals)

ws9_2 = wb9["작성은 여기에"]
print("\n작성은 여기에:")
for r in range(2, 10):
    row_vals = [ws9_2.cell(r, c).value for c in range(1, 10)]
    print(f"Row {r}:", row_vals)

print("\n=== Checking test_12_out.xlsx ===")
wb12 = openpyxl.load_workbook("test_12_out.xlsx", data_only=True)
ws12 = wb12["12-제품생산량"]
for r in range(4, 7):
    row_vals = [ws12.cell(r, c).value for c in range(1, 9)]
    print(f"Row {r}:", row_vals)

ws12_2 = wb12["작성은 여기에"]
print("\n작성은 여기에:")
for r in range(2, 5):
    row_vals = [ws12_2.cell(r, c).value for c in range(1, 10)]
    print(f"Row {r}:", row_vals)
