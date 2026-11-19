import os
import io
import datetime
import calendar
import openpyxl
from openpyxl.utils import get_column_letter

# 기본 설비 정보 정의
DEFAULT_FACILITIES = [
    {
        "code": "HM-01B",
        "process_code": "P-04-01",
        "process_name": "열처리 공정",
        "facility_id": "I-PP41001",
        "facility_name": "열처리로",
        "plant_id": "HM-01B",
        "fuel_code": "6",
        "fuel_name": "",
        "unit_code": "14",
        "unit_name": "㎥",
        "row_8_sheet": 5,
        "row_draft_sheet": 3,
        "note": "열처리로 사용량은 월별로 산출되기 때문에 월 사용량에서 가동시간을 나눠서 작성됨"
    },
    {
        "code": "BO-200",
        "process_code": "PU-02-01",
        "process_name": "스팀공급공정",
        "facility_id": "I-PU21002",
        "facility_name": "산업용 보일러",
        "plant_id": "BO-200",
        "fuel_code": "6",
        "fuel_name": "",
        "unit_code": "14",
        "unit_name": "㎥",
        "row_8_sheet": 6,
        "row_draft_raw": 4,
        "row_draft_calc": 5,
        "note": "2024.11.5부 2,3톤 보일러 폐쇄 (변경신고 완료)"
    },
    {
        "code": "BO-300",
        "process_code": "PU-02-01",
        "process_name": "스팀공급공정",
        "facility_id": "I-PU21003",
        "facility_name": "산업용 보일러",
        "plant_id": "BO-300",
        "fuel_code": "6",
        "fuel_name": "",
        "unit_code": "14",
        "unit_name": "㎥",
        "row_8_sheet": 7,
        "row_draft_raw": 7,
        "row_draft_calc": 8,
        "note": "2024.11.5부 2,3톤 보일러 폐쇄 (변경신고 완료)"
    }
]


def generate_fuel_consumption_excel(
    year: int,
    month: int,
    daily_data: dict,
    bo200_ratio: float = 1.288,
    bo300_ratio: float = 1.579,
    template_path: str = None,
    output_path: str = None
):
    """
    8. 연료사용량 엑셀 생성 함수
    :param year: 연도 (예: 2026)
    :param month: 월 (예: 10)
    :param daily_data: {
        'HM-01B': [day1..day31],
        'BO-200_raw': [day1..day31],
        'BO-200_final': [day1..day31],
        'BO-300_raw': [day1..day31],
        'BO-300_final': [day1..day31]
    }
    :param bo200_ratio: BO-200 보정계수 (기본 1.288)
    :param bo300_ratio: BO-300 보정계수 (기본 1.579)
    :param template_path: 템플릿 엑셀 파일 경로
    :param output_path: 출력 파일 경로 (None일 경우 BytesIO 반환)
    """
    if template_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, "template_8_fuel_consumption.xlsx")

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"연료사용량 템플릿 파일을 찾을 수 없습니다: {template_path}")

    wb = openpyxl.load_workbook(template_path)
    usage_month_str = f"{year}{month:02d}"
    num_days = calendar.monthrange(year, month)[1]

    # 1. '8-연료사용량' 시트 업데이트
    if "8-연료사용량" in wb.sheetnames:
        ws8 = wb["8-연료사용량"]
        
        # 년월 업데이트
        ws8["A5"] = usage_month_str
        ws8["A6"] = usage_month_str
        ws8["A7"] = usage_month_str

        # 열처리로 (HM-01B) - Row 5
        hm_vals = daily_data.get("HM-01B", [0] * 31)
        # BO-200 - Row 6
        bo200_vals = daily_data.get("BO-200_final", [0] * 31)
        # BO-300 - Row 7
        bo300_vals = daily_data.get("BO-300_final", [0] * 31)

        for day in range(1, 32):
            col = 10 + day  # 1일 = K열(11열)
            if day <= num_days:
                ws8.cell(row=5, column=col, value=float(hm_vals[day-1]) if hm_vals[day-1] != "" else 0)
                ws8.cell(row=6, column=col, value=float(bo200_vals[day-1]) if bo200_vals[day-1] != "" else 0)
                ws8.cell(row=7, column=col, value=float(bo300_vals[day-1]) if bo300_vals[day-1] != "" else 0)
            else:
                ws8.cell(row=5, column=col, value="")
                ws8.cell(row=6, column=col, value="")
                ws8.cell(row=7, column=col, value="")

    # 2. '작성은 여기에' 시트 업데이트
    if "작성은 여기에" in wb.sheetnames:
        ws_draft = wb["작성은 여기에"]

        # 년월 업데이트
        for r in [3, 4, 5, 7, 8]:
            ws_draft.cell(row=r, column=2, value=int(usage_month_str))

        bo200_raw = daily_data.get("BO-200_raw", [0] * 31)
        bo300_raw = daily_data.get("BO-300_raw", [0] * 31)

        for day in range(1, 32):
            col = 11 + day  # 1일 = L열(12열)
            col_letter = get_column_letter(col)

            if day <= num_days:
                # HM-01B (Row 3)
                ws_draft.cell(row=3, column=col, value=float(hm_vals[day-1]) if hm_vals[day-1] != "" else "")
                # BO-200 raw (Row 4)
                ws_draft.cell(row=4, column=col, value=float(bo200_raw[day-1]) if bo200_raw[day-1] != "" else 0)
                # BO-200 calc formula (Row 5)
                ws_draft.cell(row=5, column=col, value=f"={col_letter}4*{bo200_ratio}")
                # BO-300 raw (Row 7)
                ws_draft.cell(row=7, column=col, value=float(bo300_raw[day-1]) if bo300_raw[day-1] != "" else 0)
                # BO-300 calc formula (Row 8)
                ws_draft.cell(row=8, column=col, value=f"={col_letter}7*{bo300_ratio}")
            else:
                ws_draft.cell(row=3, column=col, value="")
                ws_draft.cell(row=4, column=col, value="")
                ws_draft.cell(row=5, column=col, value="")
                ws_draft.cell(row=7, column=col, value="")
                ws_draft.cell(row=8, column=col, value="")

    if output_path:
        wb.save(output_path)
        return output_path
    else:
        out_stream = io.BytesIO()
        wb.save(out_stream)
        out_stream.seek(0)
        return out_stream.getvalue()
