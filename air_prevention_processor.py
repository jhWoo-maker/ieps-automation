import os
import openpyxl
import pandas as pd
from datetime import datetime, timedelta

HOLIDAYS = [
    "20260101",
    "20260216", "20260217", "20260218",
    "20260301", "20260302",
    "20260505",
    "20260524", "20260525",
    "20260603", "20260606",
    "20260717",
    "20260803", "20260804", "20260805", "20260806", "20260807",
    "20260815",
    "20260924", "20260925", "20260926",
    "20261003", "20261005", "20261009",
    "20261225"
]

CODE_D_MAP = {
    "C-PP11001": (1170.37, 1.51), "C-PP11005": (1170.37, 1.51),
    "C-PP11002": (2134.97, 1.17), "C-PP11006": (2134.97, 1.17),
    "C-PP11003": (1611.98, 2.53), "C-PP11007": (1611.98, 2.53),
    "C-PP11004": (1773.53, 2.52), "C-PP11008": (1773.53, 2.52),
    "C-PP12001": (274.64, 4.77),  "C-PP12002": (274.64, 4.77),
    "C-PP13001": (133.28, 5.89),  "C-PP13002": (133.28, 5.89),
    "C-PP14001": (80.11, 8.15),   "C-PP14002": (80.11, 8.15),
    "C-PP15001": (111.35, 5.13),  "C-PP15004": (111.35, 5.13),
    "C-PP15002": (85.28, 4.84),   "C-PP15005": (85.28, 4.84),
    "C-PP15003": (85.28, 4.34),   "C-PP15006": (85.28, 4.34),
    "C-PP16001": (40.03, 4.38),   "C-PP16002": (40.03, 4.38),
    "C-PP17001": (38.22, 1.6),    "C-PP17002": (38.22, 1.6),
}

def get_total_add_days(dt_str):
    date_obj = datetime.strptime(dt_str, "%Y%m%d").date()
    start_date = datetime(2026, 6, 1).date()
    if date_obj < start_date:
        return 0
    total_add = 0
    cur = start_date + timedelta(days=1)
    while cur <= date_obj:
        if cur.weekday() not in (5, 6):
            ds = cur.strftime("%Y%m%d")
            if ds not in HOLIDAYS:
                total_add += 1
        cur += timedelta(days=1)
    return total_add

def is_weekend_or_holiday(dt_str):
    date_obj = datetime.strptime(dt_str, "%Y%m%d").date()
    if date_obj.weekday() in (5, 6) or dt_str in HOLIDAYS:
        return True
    return False

def eval_expr(expr, row4_vals, evaluated_d_map):
    if expr is None:
        return 0
    if isinstance(expr, (int, float)):
        return expr
    expr_str = str(expr).strip()
    if not expr_str.startswith("="):
        try:
            return float(expr_str) if "." in expr_str else int(expr_str)
        except ValueError:
            return expr_str
    
    f = expr_str[1:].upper().replace("$", "")
    if f in ("AM4", "AN4", "AO4", "AP4", "AQ4", "AR4"):
        return row4_vals.get(f, 0)
    elif len(f) in (2, 3) and f.endswith("4"):
        col_name = f[:-1]
        col_idx = openpyxl.utils.column_index_from_string(col_name)
        return row4_vals.get(col_idx, 0)
    elif f == "LARGE(D282:D283,1)":
        return max(evaluated_d_map.get(282, 0), evaluated_d_map.get(283, 0))
    else:
        return 0

def process_air_prevention(sub_excel_path_or_df, template_path, output_path, pickling_small_hours=None, pickling_medium_large_hours=None, custom_hours_map=None):
    """
    6. 대기 방지시설 운영현황 자동화 처리 함수
    """
    is_xlsm = str(template_path).lower().endswith(".xlsm")
    wb = openpyxl.load_workbook(template_path, data_only=False, keep_vba=is_xlsm)
    ws_match_raw = wb["4번파일(매칭)"]
    ws_match_data = openpyxl.load_workbook(template_path, data_only=True)["4번파일(매칭)"]
    ws_here = wb["작성은 여기서(매칭)"]
    ws_sheet1 = wb["Sheet1"]
    ws_main = wb["6-대기 방지시설 운영현황"]

    # 1. Update '작성은 여기서(매칭)' if df or file provided
    if isinstance(sub_excel_path_or_df, pd.DataFrame):
        df_outlet = sub_excel_path_or_df
    elif isinstance(sub_excel_path_or_df, str) and os.path.exists(sub_excel_path_or_df):
        df_raw = pd.read_excel(sub_excel_path_or_df, header=None)
        data_rows = []
        for idx, row in df_raw.iterrows():
            val = str(row[0]).split(".")[0].strip()
            if len(val) == 8 and val.isdigit():
                data_rows.append({
                    "No": len(data_rows) + 1,
                    "가동일자": val,
                    "배출구정보": str(row[1]).strip(),
                    "시간": row[2] if pd.notna(row[2]) else 0,
                    "분": row[3] if pd.notna(row[3]) else 0,
                    "비고": row[4] if pd.notna(row[4]) else ""
                })
        if data_rows:
            df_outlet = pd.DataFrame(data_rows)
        else:
            df_outlet = pd.read_excel(sub_excel_path_or_df)
    else:
        df_outlet = None

    if df_outlet is not None and not df_outlet.empty:
        for r in range(3, ws_here.max_row + 1):
            ws_here.cell(r, 1).value = None
            ws_here.cell(r, 2).value = None
            ws_here.cell(r, 3).value = None
            ws_here.cell(r, 4).value = None
            ws_here.cell(r, 5).value = None
            ws_here.cell(r, 6).value = None

        r_idx = 3
        for _, row in df_outlet.iterrows():
            ws_here.cell(r_idx, 1, row.get("No", r_idx - 2))
            ws_here.cell(r_idx, 2, row.get("가동일자", ""))
            ws_here.cell(r_idx, 3, row.get("배출구정보", ""))
            ws_here.cell(r_idx, 4, row.get("시간", 0))
            ws_here.cell(r_idx, 5, row.get("분", 0))
            ws_here.cell(r_idx, 6, row.get("비고", ""))
            r_idx += 1

    # Re-read outlet hours map from ws_here
    outlet_hours_map = {}
    unique_dates = set()
    for r in range(3, ws_here.max_row + 1):
        d_val = ws_here.cell(r, 2).value
        if not d_val:
            continue
        d_str = str(d_val).split(".")[0].strip()
        if len(d_str) == 8 and d_str.isdigit():
            unique_dates.add(d_str)
        out_code = str(ws_here.cell(r, 3).value).strip()
        hrs = ws_here.cell(r, 4).value or 0
        mins = ws_here.cell(r, 5).value or 0
        outlet_hours_map[(d_str, out_code)] = (hrs, mins)

    sorted_dates = sorted(list(unique_dates))
    if not sorted_dates:
        sorted_dates = [f"202609{d:02d}" for d in range(1, 31)]

    # Col to outlet code mapping in 4번파일(매칭)
    col_to_outlet = {}
    for col in range(3, 46):
        val = ws_match_data.cell(2, col).value
        if val:
            col_to_outlet[col] = str(val).strip()

    # Pre-parse 30 facility rows in 4번파일(매칭) (rows 6..35)
    row_exprs = []
    for r in range(6, 36):
        d_expr = ws_match_raw.cell(r, 4).value
        e_expr = ws_match_raw.cell(r, 5).value
        # Correct template copy-paste error for air prevention facilities (CY-08, CY-09, BF-11)
        if r in (21, 22, 30) and str(d_expr).strip() == '24':
            d_expr = '='
        row_exprs.append((r, d_expr, e_expr))

    sheet1_row_idx = 5
    main_row_idx = 5

    preview_records = []

    for dt_str in sorted_dates:
        date_obj = datetime.strptime(dt_str, "%Y%m%d").date()
        is_weekend = is_weekend_or_holiday(dt_str)

        row4_vals = {}
        if is_weekend:
            row4_vals["AM4"] = 0
            row4_vals["AN4"] = 0
            row4_vals["AO4"] = 0
            row4_vals["AP4"] = 0
            row4_vals["AQ4"] = 0
            srcStartCol = 31
        else:
            row4_vals["AM4"] = 10
            row4_vals["AO4"] = 10
            row4_vals["AP4"] = 16
            if date_obj.weekday() == 4: # Friday
                row4_vals["AN4"] = 8
                row4_vals["AQ4"] = 16
            else:
                row4_vals["AN4"] = 12
                row4_vals["AQ4"] = 24
            srcStartCol = 38

        for col_idx, out_code in col_to_outlet.items():
            hrs, mins = outlet_hours_map.get((dt_str, out_code), (0, 0))
            row4_vals[col_idx] = hrs
            row4_vals[col_idx + 1] = mins

        row4_vals["AR4"] = outlet_hours_map.get((dt_str, "#W1"), (0, 0))[0]
        tot_add_days = get_total_add_days(dt_str)

        evaluated_d = {}

        for idx, (match_r, d_expr, e_expr) in enumerate(row_exprs):
            val_d = eval_expr(d_expr, row4_vals, evaluated_d)
            evaluated_d[match_r] = val_d
            val_e = eval_expr(e_expr, row4_vals, evaluated_d)

            # 1. Force 0 operating hours on weekends / holidays for all facilities
            if is_weekend:
                val_d = 0
                val_e = 0

            # 2. Facility code check for pickling custom hours on weekdays
            fac_code = str(ws_sheet1.cell(sheet1_row_idx, 4).value or ws_match_data.cell(match_r, 4).value or '').strip()
            
            if not is_weekend:
                if fac_code in ('C-PP21001', 'C-PP21002', 'I-PP21001', 'I-PP21002', 'I-PP21003', 'I-PP21004', 'I-PP21005'):
                    if pickling_small_hours is not None:
                        val_d = pickling_small_hours
                elif fac_code in ('C-PP22001', 'C-PP22002', 'I-PP22001', 'I-PP22002', 'I-PP22003', 'I-PP22004'):
                    if pickling_medium_large_hours is not None:
                        val_d = pickling_medium_large_hours

            # Date & Facility Specific User Override
            if custom_hours_map and (dt_str, fac_code) in custom_hours_map:
                val_d = custom_hours_map[(dt_str, fac_code)]

            if val_d >= 24:
                val_e = 0

            # Parameters from 4번파일(매칭)
            params = [ws_match_data.cell(match_r, srcStartCol + k).value for k in range(6)]

            # Copy metadata from template base rows if needed (Cols 15..19 remain empty, Col 20 gets '해당없음')
            base_s1_row = 5 + idx
            base_main_row = 5 + idx

            for meta_col in range(1, 38):
                if meta_col in (1, 7, 8, 9, 15, 16, 17, 18, 19):
                    continue
                if ws_sheet1.cell(sheet1_row_idx, meta_col).value is None:
                    ws_sheet1.cell(sheet1_row_idx, meta_col, ws_sheet1.cell(base_s1_row, meta_col).value)
                if ws_main.cell(main_row_idx, meta_col).value is None:
                    ws_main.cell(main_row_idx, meta_col, ws_main.cell(base_main_row, meta_col).value)

            # Facility code from Col D
            fac_code = ws_sheet1.cell(sheet1_row_idx, 4).value

            # Compute Col I (전력사용량)
            calc_i = None
            if fac_code in CODE_D_MAP:
                base, inc = CODE_D_MAP[fac_code]
                calc_i = round(base + (inc * tot_add_days), 2)

            # Update Sheet1
            ws_sheet1.cell(sheet1_row_idx, 1, int(dt_str))
            ws_sheet1.cell(sheet1_row_idx, 7, val_d)  # G: 가동시간
            ws_sheet1.cell(sheet1_row_idx, 8, val_e)  # H: 가동분
            if calc_i is not None:
                ws_sheet1.cell(sheet1_row_idx, 9, calc_i) # I: 전력사용량

            # Update 6-대기 방지시설 운영현황
            ws_main.cell(main_row_idx, 1, int(dt_str))
            ws_main.cell(main_row_idx, 7, val_d)
            ws_main.cell(main_row_idx, 8, val_e)
            if calc_i is not None:
                ws_main.cell(main_row_idx, 9, calc_i)

            if len(preview_records) < 50:
                fac_name = ws_sheet1.cell(sheet1_row_idx, 5).value
                preview_records.append({
                    "운영일자": dt_str,
                    "방지시설관리번호": fac_code,
                    "방지시설명": fac_name,
                    "가동시간(시)": val_d,
                    "가동시간(분)": val_e,
                    "전력사용량(kWh)": calc_i if calc_i is not None else "-",
                    "사용약품명": ws_main.cell(main_row_idx, 20).value or "해당없음"
                })

            sheet1_row_idx += 1
            main_row_idx += 1

    wb.save(output_path)
    df_preview = pd.DataFrame(preview_records)
    return df_preview, sheet1_row_idx - 5
