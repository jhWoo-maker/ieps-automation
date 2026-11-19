import openpyxl
import pandas as pd

src_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879084020_bb99170c.xlsx'
user_done_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879088149_866f4de8.xlsx'

wb_src = openpyxl.load_workbook(src_file, data_only=True)
ws_src = wb_src['DataGrid Data']

src_data = []
for r in range(2, ws_src.max_row + 1):
    d = ws_src.cell(r, 2).value
    code = ws_src.cell(r, 3).value
    name = ws_src.cell(r, 4).value
    t_tot = ws_src.cell(r, 7).value
    if d and code:
        src_data.append({
            'date': str(d)[:10].replace('-', ''),
            'code': str(code).strip(),
            'name': str(name).strip(),
            't_tot': t_tot
        })

df_src = pd.DataFrame(src_data)

wb_user = openpyxl.load_workbook(user_done_file, data_only=True)
ws_user = wb_user['5-배출구가동시간']

user_data = []
for r in range(5, ws_user.max_row + 1):
    d = ws_user.cell(r, 1).value
    outlet = ws_user.cell(r, 2).value
    hh = ws_user.cell(r, 3).value
    mm = ws_user.cell(r, 4).value
    if d and outlet:
        user_data.append({
            'date': str(d),
            'outlet': str(outlet).strip(),
            'hh': hh,
            'mm': mm
        })

df_user = pd.DataFrame(user_data)

# Let's inspect 20260901 in detail
print("=== 2026-09-01 RAW SOURCE DATA ===")
print(df_src[df_src['date'] == '20260901'][['code', 'name', 't_tot']])

print("\n=== 2026-09-01 USER MANUAL EXCEL DATA ===")
print(df_user[df_user['date'] == '20260901'])
