import openpyxl

path_5 = r'C:/Users/user/.gemini/antigravity/brain/81e1ecc0-b6d4-4dfb-b472-1363863e8c8d/.user_uploaded/media_1794876967939_8154c29f.xlsx'
wb_5 = openpyxl.load_workbook(path_5, data_only=True)
ws_5 = wb_5['작성은 여기서']

path_sub = r'C:/Users/user/.gemini/antigravity/brain/81e1ecc0-b6d4-4dfb-b472-1363863e8c8d/.user_uploaded/media_1794876762540_4f2b1a86.xlsx'
wb_sub = openpyxl.load_workbook(path_sub, data_only=True)
ws_sub = wb_sub['DataGrid Data']

# 설비별 가동현황 딕셔너리 구축: { ('2026-09-01', 설비코드): 총시간(분) }
sub_data = {}
for r in range(2, ws_sub.max_row+1):
    dt = str(ws_sub.cell(r, 2).value).strip() # '2026-09-01'
    code = str(ws_sub.cell(r, 3).value).strip() # 'PM306'
    name = str(ws_sub.cell(r, 4).value).strip() # '2" 조관 작업장(P60B)'
    t_tot = ws_sub.cell(r, 7).value or 0
    sub_data[(dt, code)] = t_tot
    sub_data[(dt, name)] = t_tot

print("=== 2026년 9월 1일 (#A1 ~ #A16, #W1, #W2) 매핑 비교 분석 ===")
for r in range(3, ws_5.max_row+1):
    dt = ws_5.cell(r, 2).value
    outlet = str(ws_5.cell(r, 3).value).strip()
    hh = ws_5.cell(r, 4).value or 0
    mm = ws_5.cell(r, 5).value or 0
    note = ws_5.cell(r, 6).value
    
    if dt == 20260901:
        s_dt = f"{str(dt)[:4]}-{str(dt)[4:6]}-{str(dt)[6:]}"
        tot_m = hh * 60 + mm
        print(f"배출구: {outlet:5s} | 기록시간: {hh:2d}시간 {mm:2d}분 (총 {tot_m:4d}분)")
