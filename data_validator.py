import os
import openpyxl

def validate_excel_file(module_num, file_path):
    """
    1~11번 관리항목 엑셀 파일 작성지침 및 수식/범위 오류 검증 함수.
    반환값: (is_valid: bool, errors: list[str])
    """
    if not file_path or not os.path.exists(file_path):
        return False, ["검증할 파일이 존재하지 않습니다. 파일을 먼저 생성하거나 업로드해주세요."]
    
    errors = []
    
    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
    except Exception as e:
        return False, [f"엑셀 파일을 읽는 중 오류가 발생했습니다: {str(e)}"]

    # Module 1: 대기-자가측정기록부
    if module_num == 1:
        sheet_name = '1-대기 자가측정기록부' if '1-대기 자가측정기록부' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 7).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")
            mins = ws.cell(r, 8).value
            if mins is not None and isinstance(mins, (int, float)):
                if mins < 0 or mins >= 60:
                    errors.append(f"H{r} 셀 오류! 가동분은 0~59분 범위 내여야 합니다 (입력값: {mins})")

    # Module 2: 수질-자가측정기록부
    elif module_num == 2:
        sheet_name = '2-수질 자가측정기록부' if '2-수질 자가측정기록부' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 7).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")

    # Module 3: 기타-자가측정기록부
    elif module_num == 3:
        ws = wb.active
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 7).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")

    # Module 4: 배출시설 운영현황
    elif module_num == 4:
        sheet_name = '4-배출시설운영사항' if '4-배출시설운영사항' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 7).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")

    # Module 5: 배출구 가동시간
    elif module_num == 5:
        sheet_name = '5-배출구가동시간' if '5-배출구가동시간' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 4).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"D{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")

    # Module 6: 대기 방지시설 운영현황
    elif module_num == 6:
        sheet_names_to_check = [s for s in ['6-대기 방지시설 운영현황', 'Sheet1'] if s in wb.sheetnames]
        for sname in sheet_names_to_check:
            ws = wb[sname]
            for r in range(5, ws.max_row + 1):
                # 가동시간 검증
                hrs = ws.cell(r, 7).value
                if hrs is not None and isinstance(hrs, (int, float)):
                    if hrs < 0 or hrs > 24:
                        errors.append(f"[{sname}] G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")
                # O:R 구간 작성 금지 검증 (O=15, P=16, Q=17, R=18)
                for col_idx in range(15, 19):
                    val = ws.cell(r, col_idx).value
                    if val is not None and str(val).strip() != "":
                        col_letter = openpyxl.utils.get_column_letter(col_idx)
                        errors.append(f"[{sname}] {col_letter}{r} 셀 오류! O~R열 구간에는 인자 값이 입력되면 안 됩니다 (입력값: {val})")

    # Module 7: 폐수처리시설(수질방지시설)
    elif module_num == 7:
        ws = wb.active
        for r in range(5, ws.max_row + 1):
            dt_val = ws.cell(r, 1).value
            if dt_val is None:
                continue
            hrs = ws.cell(r, 7).value
            if hrs is not None and isinstance(hrs, (int, float)):
                if hrs < 0 or hrs > 24:
                    errors.append(f"G{r} 셀 오류! 가동시간이 24시간을 초과합니다 (입력값: {hrs})")

    # Module 8: 연료사용량
    elif module_num == 8:
        sheet_name = '8-연료사용량' if '8-연료사용량' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            fuel_code = ws.cell(r, 9).value
            if fuel_code is None:
                continue
            for day_col in range(13, 44):
                val = ws.cell(r, day_col).value
                if val is not None and isinstance(val, (int, float)) and val < 0:
                    col_letter = openpyxl.utils.get_column_letter(day_col)
                    errors.append(f"{col_letter}{r} 셀 오류! 연료 사용량은 음수일 수 없습니다 (입력값: {val})")

    # Module 9: 기타화학물질 사용량
    elif module_num == 9:
        sheet_name = '10-기타화학물질 사용량' if '10-기타화학물질 사용량' in wb.sheetnames else wb.sheetnames[0]
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            chem_name = ws.cell(r, 6).value
            if chem_name is None:
                continue
            amount = ws.cell(r, 7).value
            if amount is not None and isinstance(amount, (int, float)) and amount < 0:
                errors.append(f"G{r} 셀 오류! 기타화학물질 사용량은 음수일 수 없습니다 (입력값: {amount})")

    # Module 10: 원부원료 사용량 및 제품 생산량
    elif module_num == 10:
        for sname in wb.sheetnames:
            if '원부원료' in sname or '제품' in sname or 'Sheet' in sname or '10-' in sname or '12-' in sname:
                ws = wb[sname]
                for r in range(5, ws.max_row + 1):
                    val = ws.cell(r, 7).value
                    if val is not None and isinstance(val, (int, float)) and val < 0:
                        errors.append(f"[{sname}] G{r} 셀 오류! 사용량/생산량은 음수일 수 없습니다 (입력값: {val})")

    # Module 11: 에너지 사용량
    elif module_num == 11:
        ws = wb.active
        for r in range(5, ws.max_row + 1):
            val = ws.cell(r, 7).value
            if val is not None and isinstance(val, (int, float)) and val < 0:
                errors.append(f"G{r} 셀 오류! 에너지 사용량은 음수일 수 없습니다 (입력값: {val})")

    # 공통 데이터 행 존재 검증
    ws_first = wb.active
    has_data = False
    for r in range(5, min(20, ws_first.max_row + 1)):
        if any(ws_first.cell(r, c).value is not None for c in range(1, 10)):
            has_data = True
            break
            
    if not has_data and not errors:
        errors.append("파일에 입력된 데이터 행이 없거나 비어 있습니다.")

    is_valid = (len(errors) == 0)
    return is_valid, errors
