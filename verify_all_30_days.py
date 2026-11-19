import openpyxl
from datetime import datetime, timedelta

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\template_4_facility_status.xlsm"

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

CODE_I_MAP = {
    "C-PP11001": (82.50, 8.25),
    "C-PP11002": (245.20, 24.52),
    "C-PP11003": (260.60, 26.06),
    "C-PP11004": (151.70, 15.17),
    "C-PP12001": (112.50, 11.25),
    "C-PP12002": (112.50, 11.25),
    "C-PP13001": (81.60, 8.16),
    "C-PP13002": (81.60, 8.16),
    "C-PP14001": (101.40, 10.14),
    "C-PP15001": (102.20, 10.22),
    "C-PP17001": (71.40, 7.14),
    "C-PP17002": (71.40, 7.14),
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

wb = openpyxl.load_workbook(file_path, data_only=True)
ws_match = wb["4번파일(매칭)"]
ws_here = wb["작성은 여기서(매칭)"]
ws_sheet1 = wb["Sheet1"]

# Read outlet hours map from 작성은 여기서(매칭)
outlet_hours_map = {}
for r in range(3, ws_here.max_row + 1):
    d_val = ws_here.cell(r, 2).value
    if not d_val:
        continue
    d_str = str(d_val).split(".")[0].strip()
    out_code = str(ws_here.cell(r, 3).value).strip()
    hrs = ws_here.cell(r, 4).value or 0
    mins = ws_here.cell(r, 5).value or 0
    outlet_hours_map[(d_str, out_code)] = (hrs, mins)

col_to_outlet = {}
for col in range(3, 46):
    val = ws_match.cell(2, col).value
    if val:
        col_to_outlet[col] = str(val).strip()

wb_raw = openpyxl.load_workbook(file_path, data_only=False)
ws_match_raw = wb_raw["4번파일(매칭)"]

# Pre-parse expressions for 282 rows
row_exprs = []
for r in range(6, 288):
    d_expr = ws_match_raw.cell(r, 4).value
    e_expr = ws_match_raw.cell(r, 5).value
    code_d = ws_match.cell(r, 4).value # facility code is Col D in Sheet1? Wait, let's check facility code
    row_exprs.append((r, d_expr, e_expr))

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

diffs = 0
total_checked = 0

sheet1_row_idx = 3

for day in range(1, 31):
    dt_str = f"202609{day:02d}"
    date_obj = datetime.strptime(dt_str, "%Y%m%d").date()
    is_weekend = (date_obj.weekday() in (5, 6)) or (dt_str in HOLIDAYS)
    
    # row4_vals
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

    # Fill outlet hours in row4_vals
    for col_idx, out_code in col_to_outlet.items():
        hrs, mins = outlet_hours_map.get((dt_str, out_code), (0, 0))
        row4_vals[col_idx] = hrs
        row4_vals[col_idx + 1] = mins
    
    # AR4
    row4_vals["AR4"] = outlet_hours_map.get((dt_str, "#W1"), (0, 0))[0]

    tot_add_days = get_total_add_days(dt_str)

    evaluated_d = {}
    
    for idx, (match_r, d_expr, e_expr) in enumerate(row_exprs):
        val_d = eval_expr(d_expr, row4_vals, evaluated_d)
        evaluated_d[match_r] = val_d
        val_e = eval_expr(e_expr, row4_vals, evaluated_d)
        if val_d >= 24:
            val_e = 0
        
        # Parameters (Col 15..20 in Sheet1)
        params = [ws_match.cell(match_r, srcStartCol + k).value for k in range(6)]
        
        # Check against Sheet1
        fac_code = ws_sheet1.cell(sheet1_row_idx, 4).value
        s1_hrs = ws_sheet1.cell(sheet1_row_idx, 12).value
        s1_mins = ws_sheet1.cell(sheet1_row_idx, 13).value
        
        # Check전산량 Col I (9)
        s1_col_i = ws_sheet1.cell(sheet1_row_idx, 9).value
        calc_i = None
        if fac_code in CODE_I_MAP:
            base, inc = CODE_I_MAP[fac_code]
            calc_i = round(base + (inc * tot_add_days), 2)
            
        total_checked += 1
        if s1_hrs != val_d or s1_mins != val_e:
            diffs += 1
            if diffs <= 10:
                print(f"Diff at Row {sheet1_row_idx} ({dt_str}, {fac_code}): Calc Hrs/Min=({val_d},{val_e}) vs Sheet1=({s1_hrs},{s1_mins})")
        if calc_i is not None and abs((s1_col_i or 0) - calc_i) > 0.01:
            diffs += 1
            if diffs <= 10:
                print(f"Diff Col I at Row {sheet1_row_idx} ({dt_str}, {fac_code}): Calc I={calc_i} vs Sheet1={s1_col_i}")

        sheet1_row_idx += 1

print(f"\nVerification Complete! Total checked: {total_checked}, Diffs found: {diffs}")
