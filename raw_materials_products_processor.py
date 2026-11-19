import os
import openpyxl
import pandas as pd

def parse_datagrid_excel(file_path_or_df):
    """
    Parses DataGrid Excel file or DataFrame and returns raw material and product tonnage dicts.
    """
    if isinstance(file_path_or_df, pd.DataFrame):
        df_raw = file_path_or_df
    else:
        df_raw = pd.read_excel(file_path_or_df, header=None)

    # Initialize line map: code -> {'input_kg': float, 'good_kg': float}
    line_data = {}
    
    for idx, row in df_raw.iterrows():
        code = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        if code.startswith("PM3"):
            try:
                input_kg = float(row.iloc[3]) if pd.notna(row.iloc[3]) else 0.0
            except (ValueError, TypeError):
                input_kg = 0.0
                
            try:
                good_kg = float(row.iloc[4]) if pd.notna(row.iloc[4]) else 0.0
            except (ValueError, TypeError):
                good_kg = 0.0
                
            line_data[code] = {
                "input_kg": input_kg,
                "good_kg": good_kg
            }

    # Helper to get sum of input_kg in tons
    def get_input_tons(codes):
        tot = sum(line_data.get(c, {}).get("input_kg", 0.0) for c in codes)
        return round(tot / 1000.0, 3)

    # 1. Raw Materials Mapping (7 Processes)
    raw_materials = {
        "P-01-01": {
            "code": "P-01-01",
            "name": "소경 조관·교정·면취 공정(P60B, P60C, P60D, P60E)",
            "material": "스테인레스 코일",
            "amount": get_input_tons(["PM306", "PM307", "PM308", "PM309"]),
            "unit": "12"
        },
        "P-01-02": {
            "code": "P-01-02",
            "name": "중경 조관·교정·면취 공정(C100A)",
            "material": "스테인레스 코일",
            "amount": get_input_tons(["PM310"]),
            "unit": "12"
        },
        "P-01-03": {
            "code": "P-01-03",
            "name": "중경 조관·교정·면취 공정(C100B,P100A)",
            "material": "스테인레스 코일",
            "amount": get_input_tons(["PM311", "PM312"]),
            "unit": "12"
        },
        "P-01-04": {
            "code": "P-01-04",
            "name": "중경 조관·교정·면취 공정(P100B)",
            "material": "스테인레스 코일",
            "amount": get_input_tons(["PM313"]),
            "unit": "12"
        },
        "P-01-05": {
            "code": "P-01-05",
            "name": "대경 조관·교정·면취 공정(P200,C300,P400)",
            "material": "스테인레스 코일",
            "amount": get_input_tons(["PM314", "PM315", "PM316"]),
            "unit": "12"
        },
        "P-01-06": {
            "code": "P-01-06",
            "name": "특수관 조관·교정·면취 공정(T60A)",
            "material": "티타늄 스켈프",
            "amount": 0.0,
            "unit": "12"
        },
        "P-01-07": {
            "code": "P-01-07",
            "name": "특수관 조관·교정·면취 공정(T60B)",
            "material": "티타늄 스켈프",
            "amount": 0.0,
            "unit": "12"
        },
    }

    # 2. Product Production Mapping (2 Products)
    sts_good_tot = sum(item["good_kg"] for item in line_data.values())
    products = {
        "P1": {
            "code": "P1",
            "name": "STS PIPE\n(STAINLESS PIPE)",
            "category": "완제품",
            "amount": round(sts_good_tot / 1000.0, 3),
            "unit": "12"
        },
        "P2": {
            "code": "P2",
            "name": "TI PIPE\n(TITANIUM PIPE)",
            "category": "완제품",
            "amount": 0.0,
            "unit": "12"
        }
    }

    return raw_materials, products


def generate_raw_materials_excel(target_month_str, raw_materials_data, template_path, output_path):
    """
    Generates '9.원부원료_사용량({월}월).xlsx' file.
    target_month_str: e.g. "202610" or "202609"
    raw_materials_data: dict of process_code -> dict with 'amount'
    """
    wb = openpyxl.load_workbook(template_path)
    
    # 1. Sheet '9-원부원료 사용량'
    ws_main = wb["9-원부원료 사용량"]
    # Rows 5 to 11
    for r in range(5, 12):
        p_code = str(ws_main.cell(r, 2).value or "").strip()
        if p_code in raw_materials_data:
            val = raw_materials_data[p_code]["amount"]
            ws_main.cell(r, 1).value = str(target_month_str)
            ws_main.cell(r, 5).value = float(val)
            ws_main.cell(r, 6).value = "12"

    # 2. Sheet '작성은 여기에'
    ws_here = wb["작성은 여기에"]
    # Rows 3 to 9
    for r in range(3, 10):
        p_code = str(ws_here.cell(r, 3).value or "").strip()
        if p_code in raw_materials_data:
            val = raw_materials_data[p_code]["amount"]
            ws_here.cell(r, 2).value = int(target_month_str) if str(target_month_str).isdigit() else target_month_str
            ws_here.cell(r, 6).value = float(val)
            ws_here.cell(r, 7).value = "12"

    wb.save(output_path)
    return output_path


def generate_products_excel(target_month_str, products_data, template_path, output_path):
    """
    Generates '12.제품_생산량({월}월).xlsx' file.
    target_month_str: e.g. "202610" or "202609"
    products_data: dict of product_code -> dict with 'amount'
    """
    wb = openpyxl.load_workbook(template_path)

    # 1. Sheet '12-제품생산량'
    ws_main = wb["12-제품생산량"]
    # Rows 5 to 6
    for r in range(5, 7):
        p_code = str(ws_main.cell(r, 2).value or "").strip()
        if p_code in products_data:
            val = products_data[p_code]["amount"]
            ws_main.cell(r, 1).value = str(target_month_str)
            ws_main.cell(r, 5).value = float(val)
            ws_main.cell(r, 6).value = "12"

    # 2. Sheet '작성은 여기에'
    ws_here = wb["작성은 여기에"]
    # Rows 3 to 4
    for r in range(3, 5):
        p_code = str(ws_here.cell(r, 3).value or "").strip()
        if p_code in products_data:
            val = products_data[p_code]["amount"]
            ws_here.cell(r, 2).value = int(target_month_str) if str(target_month_str).isdigit() else target_month_str
            ws_here.cell(r, 6).value = float(val)
            ws_here.cell(r, 7).value = 12

    wb.save(output_path)
    return output_path
