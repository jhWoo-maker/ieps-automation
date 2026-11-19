import re
import pdfplumber

ITEM_NAME_MAP = {
    "총유기탄소": "TOC",
    "수온": "온도",
    "용해성 철": "철",
    "용해성 망간": "망간",
}

def parse_water_quality_pdf(pdf_file_path, target_location="#W1"):
    """
    수질 측정기록부 PDF에서 target_location(#W1) 지점의 채취일시와 측정항목별 측정값을 추출합니다.
    """
    results = {
        "sampling_date_code": None,  # YYYYMMDDHHMM (예: 202610161100)
        "data": {},                  # { 오염물질명: 측정값_문자열 }
        "raw_sampling_info": ""      # 디버깅/확인용 채취일시 원문
    }
    
    with pdfplumber.open(pdf_file_path) as pdf:
        w1_pages = []
        
        # 1. target_location(#W1) 지점 페이지 찾기
        for page in pdf.pages:
            text = page.extract_text() or ""
            if target_location in text:
                w1_pages.append(page)
                
        if not w1_pages:
            raise ValueError(f"PDF에서 '{target_location}' 지점 페이지를 찾을 수 없습니다.")
            
        # 2. 첫번째 #W1 페이지에서 채취일시 추출
        for page in w1_pages:
            text = page.extract_text() or ""
            
            date_match = re.search(r"채취\s*일\s*:\s*(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일", text)
            time_match = re.search(r"채취\s*시간\s*:\s*(\d{1,2}:\d{2})\s*~\s*(\d{1,2}:\d{2})", text)
            
            if date_match and time_match:
                year, month, day = date_match.groups()
                end_time = time_match.group(2)  # 종료시각 (예: 11:00)
                time_digits = end_time.replace(":", "")
                
                results["sampling_date_code"] = f"{year}{int(month):02d}{int(day):02d}{time_digits}"
                results["raw_sampling_info"] = f"{year}-{int(month):02d}-{int(day):02d} {end_time}"
                break
                
        # 3. #W1 페이지들에서 측정항목 및 측정분석값 추출
        for page in w1_pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # 빈 열이나 None 제거하고 텍스트 정리
                    row_clean = [str(c).replace('\n', ' ').strip() if c is not None else '' for c in row]
                    
                    # Col 1 이 측정항목, Col 4 가 측정분석값 위치
                    if len(row_clean) > 4:
                        item_raw = row_clean[1]
                        val_raw = row_clean[4]
                        
                        # 무효 항목 제외
                        if not item_raw or item_raw in ["측정항목", "상호명(기관명)", "소재지(주소)", "대표자(의뢰인)", "환경기술인", "측정용도", "대상의명칭(측정지점)", "의뢰항목", "채취용기 및 수량", "채취자의견", "채취일시", "분석기간", "종합의견", "① 의 뢰 인", "④ 시 료 채 취", "⑤ 측 정 분 석 결 과"]:
                            continue
                            
                        if val_raw:
                            # 엑셀 오염물질 표준 이름 매핑
                            item_name = ITEM_NAME_MAP.get(item_raw, item_raw)
                            
                            # 값 정제: 단위 (mg/L, ℃, NTU) 제거
                            val_clean = val_raw
                            val_clean = re.sub(r"\s*(mg/L|℃|NTU)\s*", "", val_clean).strip()
                            if "불검출" in val_clean:
                                val_clean = "ND"
                                
                            results["data"][item_name] = val_clean
                            
    return results

if __name__ == "__main__":
    test_pdf = r"C:/Users/user/.gemini/antigravity/brain/81e1ecc0-b6d4-4dfb-b472-1363863e8c8d/.user_uploaded/media_1794874549741_0efffd23.pdf"
    res = parse_water_quality_pdf(test_pdf)
    print("채취일시 코드:", res["sampling_date_code"])
    print("원문 채취일시:", res["raw_sampling_info"])
    print(f"추출된 항목 개수: {len(res['data'])}")
    print("-" * 50)
    for k, v in res["data"].items():
        print(f"  {k:30s} -> {v}")
