import re
import pdfplumber

def parse_air_quality_pdf_records(pdf_file_path):
    """
    대기 자가측정기록부 PDF의 모든 페이지/레코드를 추출합니다.
    """
    records = []
    pollutant_list = [
        '질소산화물', '먼지', '니켈화합물', '크로뮴화합물', '암모니아', 
        '시안화수소', '이화탄소', '플루오린화합물', '구리화합물', '비소화합물', 
        '납화합물', '아연화합물', '카드뮴화합물', '염화수소', '입자성물질'
    ]
    
    with pdfplumber.open(pdf_file_path) as pdf:
        for idx, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            
            # 1. 배출구(굴뚝) 번호 파싱
            m_out = re.search(r"NO\.\d+\s*(A\d+)", text, re.IGNORECASE)
            if not m_out:
                m_out = re.search(r"(#?A\d{1,2})", text, re.IGNORECASE)
            
            if not m_out:
                continue
                
            raw_outlet = m_out.group(1).upper()
            outlet_code = raw_outlet if raw_outlet.startswith("#") else "#" + raw_outlet
            
            # 2. 채취일시 파싱 (채취 종료일자/시간 기준 YYYYMMDDHHMM)
            date_code = None
            m_dt = re.search(r"(\d{4})[.\s-]*(\d{1,2})[.\s-]*(\d{1,2})\s*\d{1,2}:\d{2}\s*~\s*(\d{1,2}):(\d{2})", text)
            if m_dt:
                y, m, d, hh, mm = m_dt.groups()
                date_code = f"{y}{int(m):02d}{int(d):02d}{hh}{mm}"
            else:
                m_date = re.search(r"(\d{4})\s*-\s*(\d{2})\s*-\s*(\d{2})", text)
                m_time = re.search(r"~\s*(\d{2}):(\d{2})", text)
                if m_date and m_time:
                    y, m, d = m_date.groups()
                    hh, mm = m_time.groups()
                    date_code = f"{y}{m}{d}{hh}{mm}"

            # 연월 추출 ("2026년 09월" 형태)
            year_month = "기타/미지정"
            if date_code and len(date_code) >= 6:
                y_str = date_code[:4]
                m_str = date_code[4:6]
                year_month = f"{y_str}년 {m_str}월"

            # 3. 굴뚝 제원 (높이, 내경)
            stack_height, stack_dia = None, None
            m_h = re.search(r"([\d.]+)\s*m\s+([\d.]+)\s*m", text)
            if m_h:
                try:
                    stack_height = float(m_h.group(1))
                    stack_dia = float(m_h.group(2))
                except ValueError:
                    pass

            # 4. 현장기상 (날씨, 기온, 습도, 기압, 풍향, 풍속)
            weather_val, temp_val, humidity_val, pressure_val, wind_dir_val, wind_speed_val = "맑음", None, None, None, None, None
            m_w = re.search(r"([가-힣]+)\s*([\d.]+)\s*℃\s*([\d.]+)\s*%\s*([\d.]+)\s*(?:mmHg)?\s*([가-힣\s]+)\s*([\d.]+)\s*m/sec", text)
            if m_w:
                weather_val = m_w.group(1).strip()
                try:
                    temp_val = float(m_w.group(2))
                    humidity_val = float(m_w.group(3))
                    pressure_val = float(m_w.group(4))
                    wind_dir_val = m_w.group(5).strip().replace("풍", "").strip()
                    wind_speed_val = float(m_w.group(6))
                except ValueError:
                    pass

            # 5. 배출가스 (실측산소, 표준산소, 배출가스량, 수분, 온도, 유속)
            o2_real_val, o2_std_val, flow_rate_val = None, 0, None
            m_g1 = re.search(r"([\d.]+)\s*%\s*([-\d.]+)?\s*%\s*([\d.]+)\s*S㎥/분\s*([\d.]+)\s*S㎥/분", text)
            if m_g1:
                try:
                    o2_real_val = float(m_g1.group(1))
                    std_raw = m_g1.group(2)
                    o2_std_val = float(std_raw) if std_raw and std_raw != "-" else 0
                    flow_rate_val = float(m_g1.group(4))
                except ValueError:
                    pass
            
            moisture_val, temp_gas_val, vel_gas_val = None, None, None
            m_g2 = re.search(r"([\d.]+)\s*%\s*([\d.]+)\s*℃\s*([\d.]+)\s*m/sec", text)
            if m_g2:
                try:
                    moisture_val = float(m_g2.group(1))
                    temp_gas_val = float(m_g2.group(2))
                    vel_gas_val = float(m_g2.group(3))
                except ValueError:
                    pass
                        
            page_data = {
                "page": idx + 1,
                "outlet": outlet_code,
                "sampling_date_code": date_code,
                "year_month": year_month,
                "stack_height": stack_height,
                "stack_dia": stack_dia,
                "weather": weather_val,
                "temp": temp_val,
                "humidity": humidity_val,
                "pressure": pressure_val,
                "wind_dir": wind_dir_val,
                "wind_speed": wind_speed_val,
                "flow_rate": flow_rate_val,
                "vel_gas": vel_gas_val,
                "temp_gas": temp_gas_val,
                "moisture": moisture_val,
                "o2_std": o2_std_val,
                "o2_real": o2_real_val,
                "pollutants": {}
            }
            
            # 6. 측정분석결과 (오염물질별 농도값)
            block_m = re.search(r"측\s*정\s*항\s*목.*?\n(.*?)분\s*석\s*결\s*과", text, re.DOTALL)
            if block_m:
                lines = [l.strip() for l in block_m.group(1).split("\n") if l.strip()]
                curr_pollutant = None
                for l in lines:
                    for p in pollutant_list:
                        if p in l:
                            curr_pollutant = p
                            break
                    if curr_pollutant:
                        if "불검출" in l or "지정기준 미만" in l or "지정기준미만" in l:
                            page_data["pollutants"][curr_pollutant] = 0
                            curr_pollutant = None
                        elif "이하" in l:
                            parts = l.split("이하")
                            if len(parts) > 1:
                                m_val = re.search(r"^(\d+(?:\.\d+)?)", parts[1].strip())
                                if m_val:
                                    try:
                                        val_num = float(m_val.group(1))
                                        page_data["pollutants"][curr_pollutant] = int(val_num) if val_num.is_integer() else val_num
                                    except ValueError:
                                        page_data["pollutants"][curr_pollutant] = 0
                                    curr_pollutant = None
                                    
            records.append(page_data)
            
    return records

def get_available_year_months(records):
    """
    레코드 리스트에서 고유 연월("2026년 09월" 등) 목록을 정렬하여 반환합니다.
    """
    ym_set = set()
    for r in records:
        ym = r.get("year_month")
        if ym and ym != "기타/미지정":
            ym_set.add(ym)
            
    sorted_ym = sorted(list(ym_set))
    if not sorted_ym:
        sorted_ym = ["전체"]
    return sorted_ym

def filter_records_by_year_month(records, selected_year_month=None):
    """
    선택한 연월의 레코드만 추출하여 outlet별 outlets_data 딕셔너리로 구축합니다.
    """
    outlets_data = {}
    for r in records:
        if selected_year_month and selected_year_month != "전체":
            if r.get("year_month") != selected_year_month:
                continue
        outlets_data[r["outlet"]] = r
    return outlets_data

def parse_air_quality_pdf(pdf_file_path, selected_year_month=None):
    """
    대기 자가측정기록부 PDF 파싱 메인 함수:
    (outlets_data, available_year_months, all_records) 튜플을 반환합니다.
    """
    all_records = parse_air_quality_pdf_records(pdf_file_path)
    available_ym = get_available_year_months(all_records)
    
    # 기본 선택 연월이 없으면 첫 번째(또는 최신) 연월 지정
    if not selected_year_month and available_ym:
        selected_year_month = available_ym[0]
        
    outlets_data = filter_records_by_year_month(all_records, selected_year_month)
    return outlets_data, available_ym, all_records
