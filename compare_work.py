import sys
import os
import openpyxl
import pandas as pd

sys.path.append(r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation')
from outlet_hours_processor import process_outlet_operating_hours

src_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879084020_bb99170c.xlsx'
user_done_file = r'C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794879088149_866f4de8.xlsx'

# 1. Run current automation code
df_sub, df_auto = process_outlet_operating_hours(src_file)

# 2. Read user's actual excel sheet '5-배출구가동시간'
wb_user = openpyxl.load_workbook(user_done_file, data_only=True)
ws_user = wb_user['5-배출구가동시간']

user_rows = []
for r in range(5, ws_user.max_row + 1):
    d = ws_user.cell(r, 1).value
    outlet = ws_user.cell(r, 2).value
    hh = ws_user.cell(r, 3).value
    mm = ws_user.cell(r, 4).value
    note = ws_user.cell(r, 5).value
    if d and outlet:
        user_rows.append({
            'row_idx': r,
            '가동일자': int(d),
            '배출구정보': str(outlet).strip(),
            '시간': int(hh) if hh is not None else 0,
            '분': int(mm) if mm is not None else 0,
            '비고': str(note).strip() if note else None
        })

df_user = pd.DataFrame(user_rows)

print(f"=== 개수 비교 ===")
print(f"자동화 생성 행 수: {len(df_auto)}")
print(f"사용자 작성 행 수: {len(df_user)}")

# Merge to compare
merged = pd.merge(
    df_user, df_auto, 
    on=['가동일자', '배출구정보'], 
    suffixes=('_user', '_auto'),
    how='outer'
)

diffs = merged[
    (merged['시간_user'] != merged['시간_auto']) | 
    (merged['분_user'] != merged['분_auto'])
]

print(f"\n=== 가동시간(시간, 분) 차이 목록 (총 {len(diffs)}개) ===")
for idx, r in diffs.iterrows():
    d = r['가동일자']
    o = r['배출구정보']
    hu, mu = r['시간_user'], r['분_user']
    ha, ma = r['시간_auto'], r['분_auto']
    print(f"일자: {d}, 배출구: {o:<5} | 사용자: {hu:2d}시간 {mu:2d}분  vs  자동화: {ha:2d}시간 {ma:2d}분")

# Check missing rows or outlets
only_user = merged[merged['시간_auto'].isna()]
only_auto = merged[merged['시간_user'].isna()]
print(f"\n사용자 파일에만 존재하는 레코드: {len(only_user)}")
print(f"자동화 파일에만 존재하는 레코드: {len(only_auto)}")

# Check sheet '작성은 여기서' in user file
if '작성은 여기서' in wb_user.sheetnames:
    ws_w = wb_user['작성은 여기서']
    print(f"\n=== '작성은 여기서' 시트 행 수: {ws_w.max_row} ===")
