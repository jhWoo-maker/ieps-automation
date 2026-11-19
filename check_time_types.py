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
    order_t = ws_src.cell(r, 6).value
    tot_t = ws_src.cell(r, 7).value
    real_t = ws_src.cell(r, 8).value
    if d and code:
        src_list.append({
            'date': str(d)[:10].replace('-', ''),
            'code': str(code).strip(),
            'order_t': order_t or 0,
            'tot_t': tot_t or 0,
            'real_t': real_t or 0
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
    note = ws_user.cell(r, 5).value
    if d and outlet:
        user_list.append({
            'date': str(d),
            'outlet': str(outlet).strip(),
            'hh_user': hh or 0,
            'mm_user': mm or 0,
            'tot_user': (hh or 0)*60 + (mm or 0),
            'note_user': note
        })
df_user = pd.DataFrame(user_list)

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
    sub_u = df_user[df_user['outlet'] == outlet]
    m = pd.merge(sub_u, df_src[df_src['code'] == code], on='date', how='left')
    m['match_tot'] = m['tot_user'] == m['tot_t']
    m['match_order'] = m['tot_user'] == m['order_t']
    m['match_real'] = m['tot_user'] == m['real_t']
    print(f"\n=== Outlet {outlet} (Code {code}) ===")
    print(f"Total days compared: {len(m)}")
    print(f"Match tot_t: {m['match_tot'].sum()}, Match order_t: {m['match_order'].sum()}, Match real_t: {m['match_real'].sum()}")
    diff_rows = m[~m['match_tot']]
    if len(diff_rows) > 0:
        print("Sample diff rows (date, user_hh:mm, tot_t, order_t, real_t):")
        for idx, r in diff_rows.head(5).iterrows():
            print(f"  Date: {r['date']} | User: {r['hh_user']}h {r['mm_user']}m ({r['tot_user']}m) | tot_t: {r['tot_t']}m | order_t: {r['order_t']}m | real_t: {r['real_t']}m")
