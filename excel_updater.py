import openpyxl
from openpyxl.styles import Font
from pdf_parser import parse_water_quality_pdf

def update_excel_with_pdf_data(template_excel_path, pdf_file_path, output_excel_path=None):
    """
    수질 자가측정기록부 PDF 데이터를 엑셀 템플릿에 반영합니다.
    - 변수 항목 (측정일시, 측정농도): 빨간색 글자 (Font color='FF0000', bold=True)
    - 고정 항목 (공정명, 오염물질명, 기준치 등): 검은색 글자 (Font color='000000')
    """
    # 1. PDF 데이터 파싱
    parsed_pdf = parse_water_quality_pdf(pdf_file_path, target_location="#W1")
    date_code = parsed_pdf["sampling_date_code"]
    pdf_data = parsed_pdf["data"]
    
    if not date_code:
        raise ValueError("PDF에서 채취일시 정보를 추출하지 못했습니다.")
        
    # 2. 워크북 로드
    wb = openpyxl.load_workbook(template_excel_path)
    sheet_name = '2-수질 자가측정기록부'
    
    if sheet_name not in wb.sheetnames:
        sheet_name = wb.sheetnames[0]
        
    ws = wb[sheet_name]
    
    red_font = Font(name='맑은 고딕', size=10, color='FF0000', bold=True)
    black_font = Font(name='맑은 고딕', size=10, color='000000')
    
    updated_count = 0
    
    # 3. 엑셀 데이터 업데이트
    for row in range(5, ws.max_row + 1):
        item_name = ws.cell(row=row, column=5).value  # Col 5: 오염물질명
        if not item_name:
            continue
            
        item_name_str = str(item_name).strip()
        
        # 고정 열 검은색 폰트 설정
        for col in range(1, ws.max_column + 1):
            ws.cell(row=row, column=col).font = black_font
        
        # 측정일시 업데이트 (Col 1 - 빨간색)
        ws.cell(row=row, column=1).value = date_code
        ws.cell(row=row, column=1).font = red_font
        
        # 측정농도 업데이트 (Col 9 - 빨간색)
        if item_name_str in pdf_data:
            val = pdf_data[item_name_str]
            ws.cell(row=row, column=9).value = val
            ws.cell(row=row, column=9).font = red_font
            updated_count += 1
            
    # 4. 저장
    if not output_excel_path:
        month_str = int(date_code[4:6])
        output_excel_path = f"2.수질-자가측정기록부({month_str}월).xlsx"
        
    wb.save(output_excel_path)
    
    return {
        "output_path": output_excel_path,
        "date_code": date_code,
        "raw_date": parsed_pdf["raw_sampling_info"],
        "updated_count": updated_count,
        "data": pdf_data
    }
