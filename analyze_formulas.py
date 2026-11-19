import openpyxl
import pandas as pd

src_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879084020_bb99170c.xlsx'
user_done_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879088149_866f4de8.xlsx'

wb_src = openpyxl.load_workbook(src_file, data_only=True)
ws_src = wb_src['DataGrid Data']

src_list = []
for r in range(2, ws_src.max_row + 1):
    d = ws_src.cell(r, 2).value
    code = ws_src.cell(r, 3).value
    t_tot = ws_src.cell(r, 7).value
    if d and code:
        src_list.append({
            'date': str(d)[:10].replace('-', ''),
            'code': str(code).strip(),
            't_tot': t_tot
        })
df_src = pd.DataFrame(src_list)

wb_user = openpyxl.load_workbook(user_done_file, data_only=True)
ws_user = wb_user['5-배출구가동시간']

user_list = []
for r in range(5, ws_user.max_row + 1):
    d = ws_user.cell(r, 1).value
    outlet = ws_user.cell(r, 2).value
    hh = ws_user.cell(r, 3).value
    mm = ws_user.cell(r, 4).value
    if d and outlet:
        user_list.append({
            'date': str(d),
            'outlet': str(outlet).strip(),
            'hh_user': hh,
            'mm_user': mm,
            'tot_user': (hh or 0)*60 + (mm or 0)
        })
df_user = pd.DataFrame(user_list)

# Map outlets to src code
# Outlet #A9 (PM306), #A10 (PM307), #A3 (PM308), #A4 (PM309), #A6 (PM310), #A7 (PM311/PM312), #A8 (PM313), #A11 (PM314), #A12 (PM315), #A5 (PM316)
code_map = {
    '#A9': 'PM306',
    '#A10': 'PM307',
    '#A3': 'PM308',
    '#A4': 'PM309',
    '#A6': 'PM310',
    '#A8': 'PM313',
    '#A11': 'PM314',
    '#A12': 'PM315',
    '#A5': 'PM316',
}

for outlet, code in code_map.items():
    sub_user = df_user[df_user['outlet'] == outlet]
    merged = pd.merge(sub_user, df_src[df_src['code'] == code], on='date', how='inner')
    merged['diff_mins'] = merged['tot_user'] - merged['t_tot']
    print(f"\n=== Outlet {outlet} (Code {code}) Mins Difference (User Tot - Source Tot) ===")
    print(merged[['date', 't_tot', 'hh_user', 'mm_user', 'tot_user', 'diff_mins']].head(10))
