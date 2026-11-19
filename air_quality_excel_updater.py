import openpyxl
from openpyxl.styles import Font

def update_air_quality_excel(template_path, outlets_data, output_path):
    """
    파싱된 대기 자가측정기록부 PDF 데이터를 기존 작성 템플릿(1.대기-자가측정기록부(9월).xlsx)에 업데이트합니다.
    - 변수 항목(추출값): 빨간색 글자 (Font color='FF0000', bold=True)
    - 고정 항목(양식텍스트): 검은색 글자 (Font color='000000')
    
    [열 매핑]
    Col 1 (A): 측정일시 (YYYYMMDDHHMM - 채취종료시간 기준) [변수 - RED]
    Col 2 (B): 공정번호 [고정 - BLACK]
    Col 3 (C): 공정명 [고정 - BLACK]
    Col 4 (D): 배출구번호 (#A1, #A2 등) [고정 - BLACK]
    Col 5 (E): 사업장관리번호 [고정 - BLACK]
    Col 6 (F): 기상 [변수 - RED]
    Col 7 (G): 기온(℃) [변수 - RED]
    Col 8 (H): 습도(%) [변수 - RED]
    Col 9 (I): 기압(mmHg) [변수 - RED]
    Col 10 (J): 풍향 [변수 - RED]
    Col 11 (K): 풍속(m/sec) [변수 - RED]
    Col 12 (L): 배출가스량(S㎥/min) [변수 - RED]
    Col 13 (M): 배출구 높이(m) [고정 - BLACK]
    Col 14 (N): 상부굴뚝 내경(m) [고정 - BLACK]
    Col 15 (O): 측정공 위치 내경(m) [고정 - BLACK]
    Col 16 (P): 배출가스 유속(m/s) [변수 - RED]
    Col 17 (Q): 배출가스 온도(℃) [변수 - RED]
    Col 18 (R): 수분함량(%) [변수 - RED]
    Col 19 (S): 표준산소농도(%) [변수 - RED]
    Col 20 (T): 실측산소농도(%) [변수 - RED]
    Col 21 (U): 오염물질코드 [고정 - BLACK]
    Col 22 (V): 오염물질명 [고정 - BLACK]
    Col 23 (W): 측정농도 [변수 - RED]
    Col 24 (X): 단위 [고정 - BLACK]
    """
    wb = openpyxl.load_workbook(template_path)
    
    target_sheets = [s for s in ['1-대기 자가측정기록부', '작성은 여기서'] if s in wb.sheetnames]
    
    red_font = Font(name='맑은 고딕', size=10, color='FF0000', bold=True)
    black_font = Font(name='맑은 고딕', size=10, color='000000')
    
    # 변수 열 인덱스 (1, 6, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 23)
    red_cols = {1, 6, 7, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 23}
    
    updated_rows = 0
    for sheet_name in target_sheets:
        ws = wb[sheet_name]
        for r in range(5, ws.max_row + 1):
            outlet_val = str(ws.cell(r, 4).value or '').strip()
            pollutant_val = str(ws.cell(r, 22).value or '').strip()
            
            if not outlet_val:
                continue
                
            # 기본 폰트 색상 적용 (고정=검은색, 변수=빨간색)
            for c in range(1, 25):
                cell = ws.cell(r, c)
                if c in red_cols:
                    cell.font = red_font
                else:
                    cell.font = black_font
                
            if outlet_val in outlets_data:
                info = outlets_data[outlet_val]
                
                # 1. 측정일시 (YYYYMMDDHHMM)
                if info.get('sampling_date_code'):
                    ws.cell(r, 1).value = str(info['sampling_date_code'])
                    ws.cell(r, 1).font = red_font
                    
                # 6~11: 현장기상 (기상, 기온, 습도, 기압, 풍향, 풍속)
                if info.get('weather') is not None:
                    ws.cell(r, 6).value = str(info['weather'])
                    ws.cell(r, 6).font = red_font
                if info.get('temp') is not None:
                    ws.cell(r, 7).value = info['temp']
                    ws.cell(r, 7).font = red_font
                if info.get('humidity') is not None:
                    ws.cell(r, 8).value = info['humidity']
                    ws.cell(r, 8).font = red_font
                if info.get('pressure') is not None:
                    ws.cell(r, 9).value = info['pressure']
                    ws.cell(r, 9).font = red_font
                if info.get('wind_dir') is not None:
                    ws.cell(r, 10).value = str(info['wind_dir'])
                    ws.cell(r, 10).font = red_font
                if info.get('wind_speed') is not None:
                    ws.cell(r, 11).value = info['wind_speed']
                    ws.cell(r, 11).font = red_font
                    
                # 12: 배출가스량
                if info.get('flow_rate') is not None:
                    ws.cell(r, 12).value = info['flow_rate']
                    ws.cell(r, 12).font = red_font
                    
                # 16~20: 배출가스 유속, 온도, 수분함량, 표준/실측 산소농도
                if info.get('vel_gas') is not None:
                    ws.cell(r, 16).value = info['vel_gas']
                    ws.cell(r, 16).font = red_font
                if info.get('temp_gas') is not None:
                    ws.cell(r, 17).value = info['temp_gas']
                    ws.cell(r, 17).font = red_font
                if info.get('moisture') is not None:
                    ws.cell(r, 18).value = info['moisture']
                    ws.cell(r, 18).font = red_font
                if info.get('o2_std') is not None:
                    ws.cell(r, 19).value = info['o2_std']
                    ws.cell(r, 19).font = red_font
                if info.get('o2_real') is not None:
                    ws.cell(r, 20).value = info['o2_real']
                    ws.cell(r, 20).font = red_font
                    
                # 23: 오염물질별 측정농도
                pollutants = info.get('pollutants', {})
                if pollutant_val in pollutants:
                    ws.cell(r, 23).value = pollutants[pollutant_val]
                    ws.cell(r, 23).font = red_font
                    updated_rows += 1
                else:
                    ws.cell(r, 23).value = 0
                    ws.cell(r, 23).font = red_font
                    updated_rows += 1
                    
    wb.save(output_path)
    return updated_rows
