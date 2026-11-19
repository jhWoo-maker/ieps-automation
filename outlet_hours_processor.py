import openpyxl
from openpyxl.cell.cell import Cell
import pandas as pd
import datetime
import calendar
import holidays

# 한국 공휴일
KR_HOLIDAYS = holidays.KR()

OUTLET_EQUIP_MAP = {
    "#A3": ["PM308"],   # P60D
    "#A4": ["PM309"],   # P60E
    "#A5": ["PM316"],   # P400
    "#A6": ["PM310"],   # C100A
    "#A7": ["PM311", "PM312"],  # C100B, P100A 중 Max
    "#A8": ["PM313"],   # P100B
    "#A9": ["PM306"],   # P60B
    "#A10": ["PM307"],  # P60C
    "#A11": ["PM314"],  # P200
    "#A12": ["PM315"],  # C300
    "#A13": ["PM323"],  # T60B
    "#A16": ["PM322"],  # T60A
}

OUTLET_ORDER = [
    "#A1", "#A10", "#A11", "#A12", "#A13", "#A14", "#A15", "#A16",
    "#A2", "#A3", "#A4", "#A5", "#A6", "#A7", "#A8", "#A9",
    "#W1", "#W2"
]

def process_outlet_operating_hours(sub_excel_path_or_file):
    """
    '설비별 가동현황 조회_.xlsx'를 파싱하여
    해당 월 전체 날짜(주말 및 공휴일 포함)에 대해
    배출구별 가동시간 (#A1~#A16, #W1, #W2) 데이터프레임을 생성합니다.
    주말/공휴일 및 원본에 데이터가 없는 날짜는 기본 0시간 0분으로 작성합니다.
    """
    wb = openpyxl.load_workbook(sub_excel_path_or_file, data_only=True)
    ws = wb['DataGrid Data']
    
    records = []
    found_dates = []
    
    for r in range(2, ws.max_row + 1):
        dt_raw = ws.cell(r, 2).value
        code = ws.cell(r, 3).value
        name = ws.cell(r, 4).value
        t_tot = ws.cell(r, 7).value or 0
        
        if dt_raw and code:
            dt_str = str(dt_raw).strip()[:10]  # YYYY-MM-DD
            dt_date = datetime.datetime.strptime(dt_str, "%Y-%m-%d").date()
            found_dates.append(dt_date)
            
            hh = int(t_tot // 60)
            mm = int(t_tot % 60)
            
            records.append({
                "작업일자": dt_str,
                "date_obj": dt_date,
                "설비코드": str(code).strip(),
                "작업장": str(name).strip() if name else "",
                "총시간(분)": int(t_tot),
                "시간": hh,
                "분": mm
            })
            
    df_sub = pd.DataFrame(records)
    if not found_dates:
        raise ValueError("업로드된 엑셀 파일에서 유효한 가동현황 데이터를 찾을 수 없습니다.")
        
    # 1. 해당 월의 1일부터 말일까지의 전체 날짜(주말 및 공휴일 포함) 목록 생성
    first_date = min(found_dates)
    year = first_date.year
    month = first_date.month
    num_days = calendar.monthrange(year, month)[1]
    
    all_dates = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
    
    # 2. 날짜별 배출구 가동시간 레코드 생성
    outlet_rows = []
    no_counter = 1
    
    for d in all_dates:
        d_str = d.strftime("%Y-%m-%d")
        d_int = int(d.strftime("%Y%m%d"))
        
        is_weekend_or_holiday = (d.weekday() >= 5) or (d in KR_HOLIDAYS)
        
        # 해당 날짜의 설비 데이터 검색
        if not df_sub.empty and d in df_sub["date_obj"].values:
            day_sub = df_sub[df_sub["date_obj"] == d]
            equip_time_map = dict(zip(day_sub["설비코드"], day_sub["총시간(분)"]))
        else:
            equip_time_map = {}
            
        for outlet in OUTLET_ORDER:
            hh, mm = 0, 0
            note = None
            
            # #A1, #A2, #W1, #W2 : 평일에는 24시간 0분, 주말/공휴일에는 0시간 0분
            if outlet in ["#A1", "#A2", "#W1", "#W2"]:
                if is_weekend_or_holiday:
                    hh, mm = 0, 0
                else:
                    hh, mm = 24, 0
                    
            elif outlet == "#A14":
                hh, mm = 0, 0
                note = "2024.11.5부 2,3톤보일러폐쇄 변경신고완료"
                
            elif outlet == "#A15":
                hh, mm = 0, 0
                
            elif outlet in OUTLET_EQUIP_MAP:
                codes = OUTLET_EQUIP_MAP[outlet]
                max_tot = 0
                for c in codes:
                    tot = equip_time_map.get(c, 0)
                    if tot > max_tot:
                        max_tot = tot
                        
                hh = int(max_tot // 60)
                mm = int(max_tot % 60)
                
            outlet_rows.append({
                "No": no_counter,
                "가동일자": d_int,
                "배출구정보": outlet,
                "시간": hh,
                "분": mm,
                "비고": note
            })
            no_counter += 1
            
    df_outlet = pd.DataFrame(outlet_rows)
    return df_sub, df_outlet

def save_outlet_excel_file(df_outlet, template_5_path, output_path):
    """
    데이터프레임 결과를 템플릿 엑셀 파일('5.배출구_가동시간.xlsx')의 시트들에 채워 저장합니다.
    """
    wb = openpyxl.load_workbook(template_5_path)
    
    for sheet_name in ['5-배출구가동시간', '작성은 여기서']:
        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            
            start_row = 5 if sheet_name == '5-배출구가동시간' else 3
            
            # 기존 데이터 영역 청소
            for r in range(start_row, max(ws.max_row + 1, len(df_outlet) + start_row + 5)):
                for c in range(1, 7):
                    cell = ws.cell(r, c)
                    if isinstance(cell, Cell):
                        cell.value = None
                        
            # 새로운 데이터 작성
            for idx, row in df_outlet.iterrows():
                r_idx = idx + start_row
                if sheet_name == '5-배출구가동시간':
                    ws.cell(r_idx, 1).value = int(row["가동일자"])
                    ws.cell(r_idx, 2).value = row["배출구정보"]
                    ws.cell(r_idx, 3).value = int(row["시간"])
                    ws.cell(r_idx, 4).value = int(row["분"])
                    ws.cell(r_idx, 5).value = row["비고"] if pd.notna(row["비고"]) else None
                else: # 작성은 여기서
                    ws.cell(r_idx, 1).value = int(row["No"])
                    ws.cell(r_idx, 2).value = int(row["가동일자"])
                    ws.cell(r_idx, 3).value = row["배출구정보"]
                    ws.cell(r_idx, 4).value = int(row["시간"])
                    ws.cell(r_idx, 5).value = int(row["분"])
                    ws.cell(r_idx, 6).value = row["비고"] if pd.notna(row["비고"]) else None
                    
    wb.save(output_path)
    return output_path
