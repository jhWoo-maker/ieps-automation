import openpyxl
from openpyxl.styles import Font
import os
import re

CHEMICAL_MASTER = [
    {"no": 1, "code": "P-01", "process": "조관·교정·면취 공정", "name": "수소", "unit_code": "1", "unit_name": "m3", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "ERP(SAP)입고량 기준"},
    {"no": 2, "code": "P-01", "process": "조관·교정·면취 공정", "name": "아르곤", "unit_code": "14", "unit_name": "kg", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"},
    {"no": 3, "code": "P-01", "process": "조관·교정·면취 공정", "name": "조관유", "unit_code": "14", "unit_name": "ℓ", "default_qty": 300.0, "is_gas": False, "is_fixed": True, "remark": "ERP(SAP)입고량 기준(1CAN=20L)"},
    {"no": 4, "code": "P-01", "process": "조관·교정·면취 공정", "name": "질소", "unit_code": "14", "unit_name": "kg", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"},
    {"no": 5, "code": "P-01", "process": "조관·교정·면취 공정", "name": "현상액", "unit_code": "14", "unit_name": "ℓ", "default_qty": 0.0, "is_gas": False, "is_fixed": True, "remark": "에이원 기술검사 입고량 기준"},
    {"no": 6, "code": "P-02", "process": "산처리 공정", "name": "과산화수소", "unit_code": "14", "unit_name": "kg", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"},
    {"no": 7, "code": "P-02", "process": "산처리 공정", "name": "불산", "unit_code": "14", "unit_name": "kg", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"},
    {"no": 8, "code": "P-02", "process": "산처리 공정", "name": "질산", "unit_code": "14", "unit_name": "kg", "default_qty": 0.0, "is_gas": True, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"},
    {"no": 9, "code": "PU-02", "process": "스팀 공급 공정", "name": "산소제거제", "unit_code": "14", "unit_name": "kg", "default_qty": 30.0, "is_gas": False, "is_fixed": True, "remark": "월평균기준(정량탱크)"},
    {"no": 10, "code": "PU-02", "process": "스팀 공급 공정", "name": "청관제", "unit_code": "14", "unit_name": "ℓ", "default_qty": 5.0, "is_gas": False, "is_fixed": True, "remark": "월평균기준(정량탱크)"},
    {"no": 11, "code": "PW-02-01", "process": "폐수 처리 공정", "name": "고분자응집제", "unit_code": "14", "unit_name": "kg", "default_qty": 20.0, "is_gas": False, "is_fixed": False, "remark": "수질오염 방지시설 운영일지 기준"},
    {"no": 12, "code": "PW-02-01", "process": "폐수 처리 공정", "name": "소석회", "unit_code": "12", "unit_name": "톤", "default_qty": 97.54, "is_gas": False, "is_fixed": False, "remark": "ERP(SAP)입고량 기준"},
    {"no": 13, "code": "PW-02-01", "process": "폐수 처리 공정", "name": "메탄올", "unit_code": "12", "unit_name": "톤", "default_qty": 0.41, "is_gas": False, "is_fixed": False, "remark": "화학물질 사용 관리대장 기준(유량계)"}
]

FIXED_CHEMICAL_VALUES = {
    "조관유": 300.0,
    "현상액": 0.0,
    "산소제거제": 30.0,
    "청관제": 5.0
}

def get_gas_sheets(gas_file_path):
    """List available monthly sheets in gas inspection Excel file."""
    wb = openpyxl.load_workbook(gas_file_path, read_only=True, data_only=True)
    sheets = []
    for s in wb.sheetnames:
        if re.match(r"^\d{4}\.\d{1,2}$", s.strip()):
            sheets.append(s.strip())
    wb.close()
    return sheets

def parse_gas_inspection_file(gas_file_path, sheet_name=None):
    """
    Parse monthly totals for hazardous gases from Gas Inspection Checklist.
    Returns dict: {'수소': val, '아르곤': val, '질소': val, '과산화수소': val, '불산': val, '질산': val}
    """
    wb = openpyxl.load_workbook(gas_file_path, data_only=True)
    
    if not sheet_name or sheet_name not in wb.sheetnames:
        month_sheets = [s for s in wb.sheetnames if re.match(r"^\d{4}\.\d{1,2}$", s.strip())]
        if month_sheets:
            sheet_name = month_sheets[0]
        else:
            sheet_name = wb.sheetnames[0]
            
    ws = wb[sheet_name]
    
    # Ar (Col 5 / E)
    ar_val = ws.cell(45, 5).value or ws.cell(49, 5).value
    if ar_val is None or not isinstance(ar_val, (int, float)):
        ar_val = sum(ws.cell(r, 5).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 5).value, (int, float)))
        
    # N2 (Col 10 / J)
    n2_val = ws.cell(45, 10).value or ws.cell(49, 10).value
    if n2_val is None or not isinstance(n2_val, (int, float)):
        n2_val = sum(ws.cell(r, 10).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 10).value, (int, float)))
        
    # H2 (Col 14 / N or Col 19 / S)
    h2_val = ws.cell(45, 14).value
    if h2_val is None or not isinstance(h2_val, (int, float)):
        h2_val = sum(ws.cell(r, 19).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 19).value, (int, float)))
        
    # H2O2 (Col 14 / N)
    h2o2_val = ws.cell(42, 14).value
    if h2o2_val is None or not isinstance(h2o2_val, (int, float)):
        h2o2_val = sum(ws.cell(r, 14).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 14).value, (int, float)))
        
    # HF (Col 24 / X or Col 25 / Y)
    hf_val = ws.cell(44, 24).value
    if hf_val is None or not isinstance(hf_val, (int, float)):
        hf_val = sum(ws.cell(r, 25).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 25).value, (int, float)))
        
    # HNO3 (Col 30 / AD or Col 31 / AE)
    hno3_val = ws.cell(44, 30).value
    if hno3_val is None or not isinstance(hno3_val, (int, float)):
        hno3_val = sum(ws.cell(r, 31).value or 0 for r in range(9, 42) if isinstance(ws.cell(r, 31).value, (int, float)))

    wb.close()
    
    return {
        "수소": float(h2_val or 0.0),
        "아르곤": float(ar_val or 0.0),
        "질소": float(n2_val or 0.0),
        "과산화수소": float(h2o2_val or 0.0),
        "불산": float(hf_val or 0.0),
        "질산": float(hno3_val or 0.0)
    }

def generate_chemical_excel(target_month_str, chemical_data_dict, template_path, output_path):
    """
    Populate aggregated/edited chemical usage data into target template and export.
    target_month_str: e.g., '202610'
    chemical_data_dict: dict mapping chemical name -> usage float/int
    """
    wb = openpyxl.load_workbook(template_path)
    
    year_month_num = int(target_month_str) if str(target_month_str).isdigit() else target_month_str
    
    # Force fixed chemical values
    for k, v in FIXED_CHEMICAL_VALUES.items():
        chemical_data_dict[k] = v

    # 1. Update Sheet 10-기타화학물질 사용량
    if '10-기타화학물질 사용량' in wb.sheetnames:
        ws1 = wb['10-기타화학물질 사용량']
        for r in range(5, 18):
            c_name = ws1.cell(r, 4).value
            if c_name:
                ws1.cell(r, 1).value = year_month_num
                if c_name in chemical_data_dict:
                    val = chemical_data_dict[c_name]
                    cell = ws1.cell(r, 5)
                    cell.value = float(val) if isinstance(val, (int, float)) else val
                    
                    orig_font = cell.font
                    # Red font for gas items and updated items
                    cell.font = Font(
                        color="FFFF0000",
                        name=orig_font.name if orig_font else "Calibri",
                        size=orig_font.size if orig_font else 11,
                        bold=orig_font.bold if orig_font else False
                    )

    # 2. Update Sheet 작성은 여기에
    if '작성은 여기에' in wb.sheetnames:
        ws2 = wb['작성은 여기에']
        for r in range(3, 15):
            c_name = ws2.cell(r, 5).value
            if c_name:
                ws2.cell(r, 2).value = year_month_num
                if c_name in chemical_data_dict:
                    val = chemical_data_dict[c_name]
                    cell = ws2.cell(r, 6)
                    cell.value = float(val) if isinstance(val, (int, float)) else val
                    orig_font = cell.font
                    cell.font = Font(
                        color="FFFF0000",
                        name=orig_font.name if orig_font else "Calibri",
                        size=orig_font.size if orig_font else 11,
                        bold=orig_font.bold if orig_font else False
                    )

    wb.save(output_path)
    wb.close()
    return output_path
