import os
import io
import datetime
import calendar
import importlib
import pandas as pd
import streamlit as st

import fuel_consumption_processor
import facility_status_processor
import air_prevention_processor
import chemicals_processor
import raw_materials_products_processor

importlib.reload(fuel_consumption_processor)
importlib.reload(facility_status_processor)
importlib.reload(air_prevention_processor)
importlib.reload(chemicals_processor)
importlib.reload(raw_materials_products_processor)

from fuel_consumption_processor import generate_fuel_consumption_excel
from facility_status_processor import process_facility_status
from air_prevention_processor import process_air_prevention
from chemicals_processor import generate_chemical_excel, parse_gas_inspection_file
from raw_materials_products_processor import parse_datagrid_excel, generate_raw_materials_excel, generate_products_excel
from pdf_parser import parse_water_quality_pdf
from excel_updater import update_excel_with_pdf_data
from outlet_hours_processor import process_outlet_operating_hours, save_outlet_excel_file
from air_quality_pdf_parser import parse_air_quality_pdf, parse_air_quality_pdf_records, get_available_year_months, filter_records_by_year_month
from air_quality_excel_updater import update_air_quality_excel
from data_validator import validate_excel_file

# Helper for Date & Facility Hours Editor UI
# -----------------------------------------------------------------------------
HOLIDAYS = [
    "20260101", "20260216", "20260217", "20260218", "20260301", "20260302",
    "20260505", "20260524", "20260525", "20260603", "20260606", "20260717",
    "20260803", "20260804", "20260805", "20260806", "20260807", "20260815",
    "20260924", "20260925", "20260926", "20261003", "20261005", "20261009", "20261225"
]

@st.cache_data
def get_facility_metadata(template_path, module_num=6):
    import openpyxl
    wb = openpyxl.load_workbook(template_path, data_only=True)
    ws = wb["Sheet1"]
    facilities = []
    
    start_r = 5 if module_num == 6 else 3
    end_r = 34 if module_num == 6 else 284
    
    for r in range(start_r, end_r + 1):
        code = str(ws.cell(r, 4).value or "").strip()
        proc = str(ws.cell(r, 3).value or "").strip()
        fac_name = str(ws.cell(r, 5).value or "").strip()
        sub_name = str(ws.cell(r, 6).value or "").strip()
        if code:
            facilities.append({
                "row": r,
                "code": code,
                "proc": proc,
                "fac_name": fac_name,
                "sub_name": sub_name
            })
    return facilities

def get_default_facility_hours(dt_str, fac_code, is_weekend):
    if is_weekend:
        return 0
    # Default weekday rules for pickling or general
    if fac_code in ("C-PP21001", "C-PP21002", "I-PP21001", "I-PP21002", "I-PP21003", "I-PP21004", "I-PP21005"):
        return 12
    elif fac_code in ("C-PP22001", "C-PP22002", "I-PP22001", "I-PP22002", "I-PP22003", "I-PP22004"):
        return 12
    return 24

# 페이지 기본 설정
st.set_page_config(
    page_title="세아제강 환경/공정 관리 통합 대시보드",
    page_icon="🏭",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* 기본 Pretendard & Gothic A1 폰트 설정 및 안티앨리어싱 */
    html, body, p, div, label, h1, h2, h3, h4, h5, h6, input, select, textarea, button, span, ol, li {
        font-family: 'Pretendard', 'Gothic A1', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }

    /* 사이드바 메뉴 1~11번 항목 Bold 제거 (Normal/Medium 500 설정) */
    div[data-testid="stSidebar"] label,
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] p {
        font-size: 15px !important;
        color: #1B4D2E !important;
        font-weight: 500 !important;
    }

    /* 메인 우측 영역 헤더 및 주요 본문 Bold 유지 */
    h1, h1 *, [data-testid="stTitle"], [data-testid="stTitle"] * {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #1B4D2E !important;
        letter-spacing: -0.5px !important;
        line-height: 1.3 !important;
    }

    h2, h3, [data-testid="stSubheader"] {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #2E7D32 !important;
        letter-spacing: -0.3px !important;
        margin-top: 8px !important;
        margin-bottom: 10px !important;
    }

    /* 본문 주요 텍스트 굵게 */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {
        font-size: 15.5px !important;
        font-weight: 600 !important;
    }

    /* Streamlit 아이콘, Expander, Metric 및 파일 업로더 아이콘 폰트 복원 (overlap 완전 방지) */
    [data-testid="stIcon"],
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"],
    [class*="Material"],
    [class*="material"],
    i.material-icons,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarCollapseButton"] *,
    div[data-testid="stFileUploader"] button span:first-child,
    div[data-testid="stFileUploader"] button i,
    div[data-testid="stFileUploader"] svg {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-weight: normal !important;
    }

    /* st.metric 카드 배경 흰색 및 테두리 구분 설정 */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D2E4D6 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }

    /* 파일 업로더 중복 폰트 겹침(uploadUpload) 완전 수정 */
    div[data-testid="stFileUploader"] button {
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* 사이드바 메뉴 뱃지 스타일 */
    span.stMarkdownColoredBackground {
        border-radius: 10px !important;
        padding: 2px 7px !important;
        font-size: 11px !important;
        font-weight: 700 !important;
    }
    
    /* [ 검증 전 ] 뱃지 스타일 */
    span.stMarkdownColoredBackground[style*="245, 244, 242"],
    span.stMarkdownColoredBackground[style*="gray"],
    span.stMarkdownColoredBackground[style*="grey"] {
        background-color: #4A5568 !important;
        color: #FFFFFF !important;
    }

    /* 친환경 사업장 배경 & 사이드바 테마 */
    .stApp {
        background-color: #F7FBF8 !important;
    }

    div[data-testid="stSidebar"] {
        background-color: #EEF4F0 !important;
        border-right: 1px solid #D2E4D6 !important;
    }

    /* 버튼 크기 및 폰트 */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 7px !important;
        border: none !important;
        font-size: 15.5px !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        box-shadow: 0 1px 4px rgba(46, 125, 50, 0.12) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 3px 8px rgba(46, 125, 50, 0.2) !important;
    }

    /* 파일 업로더 상자 */
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #A5D6A7 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }

    /* 데이터프레임 테마 */
    div[data-testid="stDataFrame"] {
        border: 1px solid #D2E4D6 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
    }

    /* 구분선 간격 */
    hr {
        border-color: #D2E4D6 !important;
        margin-top: 14px !important;
        margin-bottom: 14px !important;
    }
    
    /* Expander summary flex layout - prevent text overlap */
    details summary,
    [data-testid="stExpander"] details summary {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }

    [data-testid="stIconMaterial"],
    [data-testid="stIcon"],
    [data-testid="stExpanderToggleIcon"] {
        font-family: 'Material Symbols Outlined', 'Material Symbols Rounded', 'Material Icons' !important;
        font-weight: normal !important;
        font-style: normal !important;
        display: inline-block !important;
        line-height: 1 !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        word-wrap: normal !important;
        white-space: nowrap !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    
    /* 우측 상단 3점 메뉴(⋮) 바로 왼쪽에 이전제출 폴더 버튼 고정 배치 */
    div[data-testid="stPopover"] {
        position: fixed !important;
        top: 10px !important;
        right: 55px !important;
        z-index: 999999 !important;
        width: auto !important;
    }

    div[data-testid="stPopover"] button[data-testid="stPopoverButton"] {
        background-color: #FFFFFF !important;
        color: #1B4D2E !important;
        border: 1px solid #C8E6C9 !important;
        border-radius: 8px !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        padding: 4px 12px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
        height: 36px !important;
        display: flex !important;
        align-items: center !important;
    }

    div[data-testid="stPopover"] button[data-testid="stPopoverButton"]:hover {
        background-color: #EBF5ED !important;
        border-color: #2E7D32 !important;
        color: #2E7D32 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AIR_TEMPLATE = os.path.join(BASE_DIR, "template_1_air_quality.xlsx")
DEFAULT_WATER_TEMPLATE = os.path.join(BASE_DIR, "template_2_water_quality.xlsx")
DEFAULT_OUTLET_TEMPLATE = os.path.join(BASE_DIR, "template_5_outlet_hours.xlsx")
DEFAULT_FACILITY_TEMPLATE = os.path.join(BASE_DIR, "template_4_facility_status.xlsm")
DEFAULT_AIR_PREVENTION_TEMPLATE = os.path.join(BASE_DIR, "template_6_air_prevention.xlsm")
DEFAULT_CHEM_TEMPLATE = os.path.join(BASE_DIR, "template_10_chemicals.xlsx")
DEFAULT_RAW_MATERIALS_TEMPLATE = os.path.join(BASE_DIR, "template_9_raw_materials.xlsx")
DEFAULT_PRODUCTS_TEMPLATE = os.path.join(BASE_DIR, "template_12_products.xlsx")

# -----------------------------------------------------------------------------
# 세션 상태 및 검증 상태 관리
# -----------------------------------------------------------------------------
if "module_status" not in st.session_state:
    st.session_state["module_status"] = {i: "pending" for i in range(1, 12)}

if "module_files" not in st.session_state:
    st.session_state["module_files"] = {}

if "module_errors" not in st.session_state:
    st.session_state["module_errors"] = {i: [] for i in range(1, 12)}


MODULE_MANUALS = {
    1: [
        "대기 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    2: [
        "수질 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    3: [
        "기타 자가측정기록부 PDF 파일을 업로드하세요(소음·진동, 비점오염, 악취 등)",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    4: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    5: [
        "설비별 가동현황 엑셀을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    6: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    7: [
        "원하시는 파일을 업로드 하세요"
    ],
    8: [
        "일자 별 연료사용량을 입력하세요",
        "엑셀을 추출하세요"
    ],
    9: [
        "가스 저장품 점검표 엑셀을 업로드 하세요",
        "고분자응집제, 소석회, 메탄올을 수기 입력하세요",
        "엑셀을 추출하세요"
    ],
    10: [
        "MES 창원공장 종합수율 조회 엑셀 파일을 추출 후 업로드 하세요",
        "엑셀을 추출하세요"
    ],
    11: [
        "전기 사용량을 입력하세요",
        "에너지 사용량을 입력하세요",
        "엑셀을 추출하세요"
    ]
}

def render_work_manual(item_num):
    steps = MODULE_MANUALS.get(item_num, [])
    if not steps:
        return
    items_html = "".join([f"<li>{step}</li>" for step in steps])
    st.markdown(
        f'''
        <div style="background-color: #EBF5ED; border-left: 4px solid #2E7D32; padding: 12px 16px; border-radius: 8px; margin-top: 8px; margin-bottom: 16px; box-shadow: 0 1px 5px rgba(46, 125, 50, 0.07);">
            <div style="font-weight: 600; font-size: 17px; color: #1B4D2E; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                🌿 <span style="letter-spacing: -0.2px;">작업 매뉴얼</span>
            </div>
            <ol style="margin: 0; padding-left: 20px; color: #2C4A35; line-height: 1.6; font-size: 15.5px;">
                {items_html}
            </ol>
        </div>
        ''',
        unsafe_allow_html=True
    )

def render_validation_results(item_num):
    pass

if "menu_index" not in st.session_state:
    st.session_state["menu_index"] = 0

RAW_MENU_ITEMS = [
    (1, "☁️ 1. 대기-자가측정기록부"),
    (2, "💧 2. 수질-자가측정기록부"),
    (3, "📋 3. 기타-자가측정기록부"),
    (4, "🏭 4. 배출시설 운영현황"),
    (5, "⏱️ 5. 배출구 가동시간"),
    (6, "💨 6. 대기 방지시설 운영현황"),
    (7, "🌊 7. 폐수처리시설(수질방지시설)"),
    (8, "🔥 8. 연료사용량"),
    (9, "🧪 9. 기타화학물질 사용량"),
    (10, "📦 10. 원부원료 사용량 및 제품 생산량"),
    (11, "⚡ 11. 에너지 사용량")
]

def get_badge_label(item_num, title):
    status = st.session_state["module_status"].get(item_num, "pending")
    if status == "normal":
        return f"{title} :green-background[ 정상 ]"
    elif status == "error":
        return f"{title} :orange-background[ 오류 ]"
    else:
        return f"{title} :gray-background[ 검증 전 ]"

import base64

def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = os.path.join(BASE_DIR, "seah_logo.png")
if os.path.exists(logo_path):
    img_b64 = get_image_base64(logo_path)
    st.sidebar.markdown(
        f'''
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; margin-top: -10px;">
            <img src="data:image/png;base64,{img_b64}" style="width: 36px; height: 36px; object-fit: contain;">
            <span style="font-size: 20px; font-weight: bold; color: #111;">IEPS 메뉴</span>
        </div>
        ''',
        unsafe_allow_html=True
    )
else:
    st.sidebar.title("🏭 IEPS 메뉴")


menu_options = [get_badge_label(num, title) for num, title in RAW_MENU_ITEMS]
curr_idx = min(st.session_state["menu_index"], len(menu_options) - 1)

menu_selected = st.sidebar.radio(
    "메뉴 선택",
    menu_options,
    index=curr_idx,
    key="sidebar_menu_radio"
)


# -----------------------------------------------------------------------------
# 공유 드라이브 바로가기 폴더 설정
# -----------------------------------------------------------------------------
SHARED_FOLDER_PATH = r"G:\공유 드라이브\창원공장 안전환경파트\손영준\이전파일\03. 환경\0. 통합환경관리\7. 통합환경관리 사후관리계획 입력자료\이전제출"

def render_top_folder_shortcut():
    st.markdown('<span id="top_right_folder_marker"></span>', unsafe_allow_html=True)
    with st.popover("📁 IEPS 폴더", use_container_width=False):
        if st.button("📂 폴더 이동", key="btn_open_top_folder", type="primary", use_container_width=True):
            try:
                import subprocess
                if os.path.exists(SHARED_FOLDER_PATH):
                    subprocess.Popen(["explorer.exe", SHARED_FOLDER_PATH])
                    st.toast("📂 IEPS 폴더가 Windows 탐색기로 열렸습니다!")
                else:
                    st.error(f"❌ 지정된 폴더 경로를 찾을 수 없습니다:\n{SHARED_FOLDER_PATH}")
            except Exception as e:
                st.error(f"❌ 폴더 열기 오류: {e}")

for idx, opt in enumerate(menu_options):
    if opt == menu_selected:
        st.session_state["menu_index"] = idx
        break

menu = RAW_MENU_ITEMS[st.session_state["menu_index"]][1]

# 타이틀 출력 및 우측 상단 3점 메뉴 옆 폴더 바로가기 고정 배치
st.title(menu)
render_top_folder_shortcut()






# -----------------------------------------------------------------------------
# 1. 대기-자가측정기록부 모듈 (자동화 구동 중)
# -----------------------------------------------------------------------------
if "1. 대기-" in menu:
    # st.title("☁️ 1. 대기-자가측정기록부")
    render_validation_results(1)
    render_work_manual(1)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_air_pdf = st.file_uploader("대기 측정기록부 PDF 파일 선택", type=["pdf"], key="air_pdf")
        
    with col2:
        st.subheader("2️⃣ 엑셀 템플릿 파일")
        use_default_air = st.checkbox("기본 자가측정기록부 템플릿 사용", value=True, key="air_tpl_check")
        
        uploaded_air_excel = None
        if not use_default_air:
            uploaded_air_excel = st.file_uploader("기준 엑셀 템플릿(.xlsx) 업로드", type=["xlsx"], key="air_excel")

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
    if uploaded_air_pdf:
        temp_air_pdf_path = "temp_air_uploaded.pdf"
        with open(temp_air_pdf_path, "wb") as f:
            f.write(uploaded_air_pdf.getbuffer())
            
        try:
            all_air_records = parse_air_quality_pdf_records(temp_air_pdf_path)
            
            if all_air_records:
                available_ym = get_available_year_months(all_air_records)
                
                # 연/월 선택 콤보박스
                col_ym1, col_ym2 = st.columns([1, 2])
                with col_ym1:
                    selected_ym = st.selectbox(
                        "📅 추출 대상 연월 선택",
                        options=available_ym,
                        index=0,
                        key="air_ym_select",
                        help="PDF 성적서 내에 여러 월의 성적서가 포함되어 있을 경우, 추출할 대상 월을 선택하세요."
                    )
                    
                parsed_air = filter_records_by_year_month(all_air_records, selected_ym)
                
                if parsed_air:
                    st.session_state["module_status"][1] = "normal"
                    with col_ym2:
                        st.success(f"✅ [{selected_ym}] 파싱 완료! ({len(parsed_air)}개 배출구: {', '.join(parsed_air.keys())})")
                    
                    preview_list = []
                    sample_dt_code = None
                    for outlet, data in parsed_air.items():
                        dt = data.get("sampling_date_code", "-")
                        if dt and dt != "-" and not sample_dt_code:
                            sample_dt_code = dt
                        
                        weather = data.get("weather", "-")
                        temp = data.get("temp", "-")
                        humidity = data.get("humidity", "-")
                        pressure = data.get("pressure", "-")
                        wind_dir = data.get("wind_dir", "-")
                        wind_speed = data.get("wind_speed", "-")
                        flow_rate = data.get("flow_rate", "-")
                        vel_gas = data.get("vel_gas", "-")
                        temp_gas = data.get("temp_gas", "-")
                        moisture = data.get("moisture", "-")
                        o2_real = data.get("o2_real", "-")
                        
                        for pol, val in data.get("pollutants", {}).items():
                            preview_list.append({
                                "배출구": outlet,
                                "측정일시": dt,
                                "기상": weather,
                                "기온(℃)": temp,
                                "습도(%)": humidity,
                                "기압": pressure,
                                "풍향": wind_dir,
                                "풍속": wind_speed,
                                "유량": flow_rate,
                                "유속": vel_gas,
                                "가스온도": temp_gas,
                                "수분(%)": moisture,
                                "실측O2(%)": o2_real,
                                "오염물질명": pol,
                                "측정농도": val
                            })
                            
                    df_air_preview = pd.DataFrame(preview_list)
                    st.dataframe(df_air_preview, use_container_width=True, height=340)
                    
                    if st.button("🚀 대기 자가측정기록부 엑셀 자동 생성", type="primary", use_container_width=True):
                        if use_default_air and os.path.exists(DEFAULT_AIR_TEMPLATE):
                            template_path = DEFAULT_AIR_TEMPLATE
                        elif uploaded_air_excel:
                            template_path = "temp_air_template.xlsx"
                            with open(template_path, "wb") as f:
                                f.write(uploaded_air_excel.getbuffer())
                        else:
                            st.error("엑셀 템플릿 파일이 지정되지 않았습니다.")
                            st.stop()
                            
                        month_num = 9
                        if selected_ym and "월" in selected_ym:
                            try:
                                m_part = selected_ym.split("년")[1].replace("월", "").strip()
                                month_num = int(m_part)
                            except Exception:
                                month_num = 9
                        elif sample_dt_code and len(sample_dt_code) >= 6:
                            try:
                                month_num = int(sample_dt_code[4:6])
                            except ValueError:
                                month_num = 9
                                
                        output_filename = f"1.대기-자가측정기록부({month_num}월).xlsx"
                        output_filepath = os.path.join(BASE_DIR, output_filename)
                        
                        updated_count = update_air_quality_excel(template_path, parsed_air, output_filepath)
                        
                        st.balloons()
                        st.success(f"🎉 [{selected_ym}] '{output_filename}' 파일이 성공적으로 생성되었습니다! (총 {updated_count}개 행 업데이트 완료)")
                        
                        with open(output_filepath, "rb") as f:
                            file_bytes = f.read()
                            
                        st.download_button(
                            label=f"📥 {output_filename} 다운로드",
                            data=file_bytes,
                            file_name=output_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                else:
                    st.warning(f"⚠️ 선택하신 [{selected_ym}]에 해당하는 데이터가 없습니다.")
            else:
                st.session_state["module_status"][1] = "error"
                st.warning("⚠️ PDF에서 대기 측정 데이터를 찾을 수 없습니다. 파일 양식을 확인해 주세요.")
        except Exception as e:
            st.session_state["module_status"][1] = "error"
            st.error(f"❌ PDF 처리 중 오류 발생: {e}")
# -----------------------------------------------------------------------------
# 2. 수질-자가측정기록부 모듈 (구동 중)
# -----------------------------------------------------------------------------
elif "2. 수질" in menu:
    # st.title("💧 2. 수질-자가측정기록부")
    render_validation_results(2)
    render_work_manual(2)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_pdf = st.file_uploader("수질 측정기록부 PDF 파일 선택", type=["pdf"], key="water_pdf")
        
    with col2:
        st.subheader("2️⃣ 엑셀 템플릿 파일")
        use_default = st.checkbox("기본 자가측정기록부 템플릿 사용", value=True, key="water_tpl_check")
        
        uploaded_excel = None
        if not use_default:
            uploaded_excel = st.file_uploader("기준 엑셀 템플릿(.xlsx) 업로드", type=["xlsx"], key="water_excel")

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
    if uploaded_pdf:
        temp_pdf_path = "temp_uploaded.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
            
        try:
            parsed = parse_water_quality_pdf(temp_pdf_path, target_location="#W1")
            st.session_state["module_status"][2] = "normal"
            st.success("✅ PDF 파싱 완료! (#W1 폐수처리공정)")
            st.metric("채취일시 (적용 코드)", parsed["sampling_date_code"], help="종료 시각 기준 YYYYMMDDHHMM")
            st.info(f"📅 채취일시 원문: {parsed['raw_sampling_info']}")
            
            df_preview = pd.DataFrame([
                {"오염물질명": k, "방류수 농도(mg/l)": v} for k, v in parsed["data"].items()
            ])
            st.dataframe(df_preview, use_container_width=True, height=320)
            
            if st.button("🚀 자가측정기록부 엑셀 자동 생성", type="primary", use_container_width=True):
                if use_default and os.path.exists(DEFAULT_WATER_TEMPLATE):
                    template_path = DEFAULT_WATER_TEMPLATE
                elif uploaded_excel:
                    template_path = "temp_template.xlsx"
                    with open(template_path, "wb") as f:
                        f.write(uploaded_excel.getbuffer())
                else:
                    st.error("엑셀 템플릿 파일이 지정되지 않았습니다.")
                    st.stop()
                    
                month_num = int(parsed["sampling_date_code"][4:6])
                output_filename = f"2.수질-자가측정기록부({month_num}월).xlsx"
                
                res = update_excel_with_pdf_data(template_path, temp_pdf_path, output_filename)
                
                st.balloons()
                st.success(f"🎉 '{output_filename}' 파일이 성공적으로 생성되었습니다! (총 {res['updated_count']}개 항목 반영)")
                
                with open(output_filename, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"📥 {output_filename} 다운로드",
                    data=file_bytes,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        except Exception as e:
            st.session_state["module_status"][2] = "error"
            st.error(f"❌ PDF 처리 중 오류 발생: {e}")
# -----------------------------------------------------------------------------
# 4. 배출시설 운영현황 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
elif "4. 배출시설" in menu:
    fac_icon_path = os.path.join(BASE_DIR, "facility_icon.png")
    if os.path.exists(fac_icon_path):
        fac_img_b64 = get_image_base64(fac_icon_path)
        st.markdown(
            f'''
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <img src="data:image/png;base64,{fac_img_b64}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                <span style="font-size: 2.2rem; font-weight: 700; color: #111;">4. 배출시설 운영현황</span>
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        pass
        # st.title("🏭 4. 배출시설 운영현황")
    render_validation_results(4)
    st.markdown("'5. 배출구 가동시간' 엑셀 파일 또는 설비 가동현황 데이터를 업로드하면, 282개 전체 배출시설의 가동시간, 가동분, 운영인자 6개, 전산량(누적 평일 기준)이 주말/공휴일 및 요일별 규칙에 따라 자동 계산되어 Sheet1 및 4-배출시설운영사항에 작성됩니다.")
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_fac_sub = st.file_uploader("'5. 배출구 가동시간' 또는 '설비별 가동현황' 엑셀(.xlsx) 업로드", type=["xlsx", "xls"], key="fac_sub_excel")
        
        st.subheader("2️⃣ 기준 XLSM / XLSX 템플릿 선택")
        use_default_fac = st.checkbox("기본 '4. 배출시설 운영현황(신규- 26년 _9월).xlsm' 템플릿 사용", value=True, key="fac_tpl_check")
        
        uploaded_fac_template = None
        if not use_default_fac:
            uploaded_fac_template = st.file_uploader("원본 XLSM/XLSX 템플릿 파일 업로드", type=["xlsm", "xlsx"], key="fac_tpl_file")
            
        if "custom_fac4" not in st.session_state:
            st.session_state["custom_fac4"] = {}

        with st.expander("⚙️ 날짜별 가동시간 수정 (콤보박스 선택 및 좌측 기존 / 우측 수정시간)", expanded=False):
            # 1. Date ComboBox
            dates_list4 = [f"202610{d:02d}" for d in range(1, 32)]
            sel_date4 = st.selectbox("📅 조회 및 수정할 가동일자 선택", options=dates_list4, index=0, key="sel_date4")
            
            from datetime import datetime
            dt_obj4 = datetime.strptime(sel_date4, "%Y%m%d").date()
            weekday_kr4 = ["월", "화", "수", "목", "금", "토", "일"][dt_obj4.weekday()]
            is_wkd4 = dt_obj4.weekday() in (5, 6) or sel_date4 in HOLIDAYS
            st.info(f"선택 일자: **{sel_date4} ({weekday_kr4}요일)** | " + ("🔴 주말/공휴일 (기본 0시간)" if is_wkd4 else "🔵 평일"))

            filter_kw4 = st.text_input("🔍 공정명 / 시설명 / 코드 검색", value="", key="filter4")
            
            facs4_list = get_facility_metadata(DEFAULT_FACILITY_TEMPLATE, 4)
            if filter_kw4:
                facs4_list = [f for f in facs4_list if filter_kw4.lower() in f["code"].lower() or filter_kw4.lower() in f["proc"].lower() or filter_kw4.lower() in f["fac_name"].lower() or filter_kw4.lower() in f["sub_name"].lower()]

            table4_data = []
            for fac in facs4_list:
                f_code = fac["code"]
                def_h = get_default_facility_hours(sel_date4, f_code, is_wkd4)
                cur_h = st.session_state["custom_fac4"].get((sel_date4, f_code), def_h)
                table4_data.append({
                    "운영일자": sel_date4,
                    "시설관리번호": f_code,
                    "공정명": fac["proc"],
                    "배출시설명": f"{fac['fac_name']} ({fac['sub_name']})",
                    "기존 입력/계산 데이터 (시)": def_h,
                    "변경할 수정시간 (시)": cur_h
                })

            df_ed4 = pd.DataFrame(table4_data)
            edited_df4 = st.data_editor(
                df_ed4,
                column_config={
                    "운영일자": st.column_config.TextColumn(disabled=True),
                    "시설관리번호": st.column_config.TextColumn(disabled=True),
                    "공정명": st.column_config.TextColumn(disabled=True),
                    "배출시설명": st.column_config.TextColumn(disabled=True),
                    "기존 입력/계산 데이터 (시)": st.column_config.NumberColumn(disabled=True, help="기존 규칙/수식 원본 시간"),
                    "변경할 수정시간 (시)": st.column_config.NumberColumn(min_value=0, max_value=24, step=1, help="우측에서 직접 수정시간 입력")
                },
                disabled=["운영일자", "시설관리번호", "공정명", "배출시설명", "기존 입력/계산 데이터 (시)"],
                use_container_width=True,
                hide_index=True,
                key=f"ed4_{sel_date4}"
            )

            for idx, r in edited_df4.iterrows():
                fc = r["시설관리번호"]
                mh = r["변경할 수정시간 (시)"]
                oh = r["기존 입력/계산 데이터 (시)"]
                if mh != oh:
                    st.session_state["custom_fac4"][(sel_date4, fc)] = mh
                elif (sel_date4, fc) in st.session_state["custom_fac4"] and mh == oh:
                    del st.session_state["custom_fac4"][(sel_date4, fc)]

            if st.session_state["custom_fac4"]:
                st.success(f"✏️ 총 {len(st.session_state['custom_fac4']):,}개 항목에 수동 수정시간이 설정되었습니다.")
                if st.button("🗑️ 4번 수동 수정사항 전체 초기화", key="rst4"):
                    st.session_state["custom_fac4"] = {}
                    st.rerun()

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
        
    if uploaded_fac_sub:
        temp_fac_sub_path = "temp_fac_sub.xlsx"
        with open(temp_fac_sub_path, "wb") as f:
            f.write(uploaded_fac_sub.getbuffer())
            
        try:
            if use_default_fac and os.path.exists(DEFAULT_FACILITY_TEMPLATE):
                template_path = DEFAULT_FACILITY_TEMPLATE
            elif uploaded_fac_template:
                ext = os.path.splitext(uploaded_fac_template.name)[1].lower()
                template_path = f"temp_fac_template{ext}"
                with open(template_path, "wb") as f:
                    f.write(uploaded_fac_template.getbuffer())
            else:
                st.error("기준 엑셀 템플릿이 지정되지 않았습니다.")
                st.stop()
                
            is_template_xlsm = template_path.lower().endswith(".xlsm")
            ext_out = ".xlsm" if is_template_xlsm else ".xlsx"
            temp_output = f"temp_fac_output{ext_out}"

            with st.spinner("⏳ VBA 매크로 및 282개 배출시설 운영현황 (주말/공휴일/평일 인자 및 전산량) 계산 중..."):
                df_fac_prev, total_proc_rows = process_facility_status(temp_fac_sub_path, template_path, temp_output, custom_hours_map=st.session_state.get("custom_fac4"))
                
            fac_month = 9
            if not df_fac_prev.empty and "운영일자" in df_fac_prev.columns:
                first_dt = str(df_fac_prev["운영일자"].iloc[0])
                if len(first_dt) >= 6:
                    try:
                        fac_month = int(first_dt[4:6])
                    except ValueError:
                        fac_month = 9

            output_fac_filename = f"4.배출시설_운영현황(26년_{fac_month}월){ext_out}"
            output_fac_filepath = os.path.join(BASE_DIR, output_fac_filename)
            if os.path.exists(temp_output):
                os.replace(temp_output, output_fac_filepath)

            st.session_state["module_status"][6] = "normal"
            st.success(f"✅ 자동 계산 완료! (총 {total_proc_rows:,}개 레코드 생성)")
            st.dataframe(df_fac_prev, use_container_width=True, height=350)
            
            mime_type = "application/vnd.ms-excel.sheet.macroEnabled.12" if is_template_xlsm else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            if st.button(f"🚀 '4. 배출시설 운영현황' ({ext_out}) 파일 생성", type="primary", use_container_width=True):
                st.balloons()
                st.success(f"🎉 '{output_fac_filename}' 파일 작성이 완료되었습니다!")
                
                with open(output_fac_filepath, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"📥 {output_fac_filename} 다운로드",
                    data=file_bytes,
                    file_name=output_fac_filename,
                    mime=mime_type,
                    use_container_width=True
                )
        except Exception as e:
            st.session_state["module_status"][6] = "error"
            st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
# -----------------------------------------------------------------------------
# 5. 배출구 가동시간 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
elif "5. 배출구" in menu:
    # st.title("⏱️ 5. 배출구 가동시간")
    render_validation_results(5)
    render_work_manual(5)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_sub = st.file_uploader("다운로드받으신 '설비별 가동현황' 엑셀(.xlsx)을 업로드하세요", type=["xlsx", "xls"], key="sub_excel")
        
    with col2:
        st.subheader("2️⃣ 엑셀 템플릿 선택")
        use_default_outlet = st.checkbox("기본 배출구 가동시간 템플릿 사용", value=True, key="outlet_tpl_check")
        
        uploaded_outlet_template = None
        if not use_default_outlet:
            uploaded_outlet_template = st.file_uploader("기준 배출구 가동시간 템플릿(.xlsx) 업로드", type=["xlsx"], key="outlet_tpl_file")

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
    
    if uploaded_sub:
        temp_sub_path = "temp_sub_excel.xlsx"
        with open(temp_sub_path, "wb") as f:
            f.write(uploaded_sub.getbuffer())
            
        try:
            df_sub, df_outlet = process_outlet_operating_hours(temp_sub_path)
            st.session_state["module_status"][5] = "normal"
            st.success("✅ 설비 가동현황 데이터 처리 완료 및 배출구 가동시간 자동 매핑 완료!")
            
            st.info("💡 주말/공휴일 가동시간(#A1, #A2, #W1, #W2) 또는 #A15 등 변경이 필요한 경우 **표에서 숫자를 직접 클릭하여 수정**할 수 있습니다.")
            
            edited_df_outlet = st.data_editor(
                df_outlet,
                num_rows="fixed",
                use_container_width=True,
                height=450,
                column_config={
                    "No": st.column_config.NumberColumn("No", disabled=True),
                    "가동일자": st.column_config.NumberColumn("가동일자", disabled=True, format="%d"),
                    "배출구정보": st.column_config.TextColumn("배출구정보", disabled=True),
                    "시간": st.column_config.NumberColumn("가동시간 (시간)", min_value=0, max_value=24, step=1),
                    "분": st.column_config.NumberColumn("가동시간 (분)", min_value=0, max_value=59, step=1),
                    "비고": st.column_config.TextColumn("비고")
                }
            )
            
            st.divider()
            st.subheader("4️⃣ 최종 엑셀 파일 저장 및 다운로드")
            
            first_date = str(edited_df_outlet["가동일자"].iloc[0])
            month_str = int(first_date[4:6]) if len(first_date) >= 6 else 9
            out_excel_name = f"5.배출구_가동시간(26년_{month_str}월).xlsx"
            
            if st.button("🚀 '5. 배출구 가동시간' 엑셀 완성본 생성", type="primary", use_container_width=True):
                template_path = DEFAULT_OUTLET_TEMPLATE if use_default_outlet or not uploaded_outlet_template else "temp_outlet_tpl.xlsx"
                if uploaded_outlet_template and not use_default_outlet:
                    with open(template_path, "wb") as f:
                        f.write(uploaded_outlet_template.getbuffer())
                        
                temp_out_path = f"output_{out_excel_name}"
                save_outlet_excel_file(edited_df_outlet, template_path, temp_out_path)
                
                st.session_state["module_files"][5] = os.path.abspath(temp_out_path)
                st.balloons()
                st.success(f"🎉 '{out_excel_name}' 엑셀 파일 생성이 완료되었습니다!")
                
                with open(temp_out_path, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"📥 {out_excel_name} 다운로드",
                    data=file_bytes,
                    file_name=out_excel_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
        except Exception as e:
            st.session_state["module_status"][5] = "error"
            st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
# -----------------------------------------------------------------------------
# 6. 대기 방지시설 운영현황 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
elif "6. 대기" in menu:
    icon6_path = os.path.join(BASE_DIR, "icon_item6.png")
    if os.path.exists(icon6_path):
        icon6_b64 = get_image_base64(icon6_path)
        st.markdown(
            f'''
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <img src="data:image/png;base64,{icon6_b64}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                <span style="font-size: 2.2rem; font-weight: 700; color: #111;">6. 대기 방지시설 운영현황</span>
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        pass
        # st.title("💨 6. 대기 방지시설 운영현황")

    render_work_manual(6)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_prev_sub = st.file_uploader("'5. 배출구 가동시간' 또는 '설비별 가동현황' 엑셀(.xlsx) 업로드", type=["xlsx", "xls"], key="prev_sub_excel")
        
    with col2:
        st.subheader("2️⃣ 기준 XLSM / XLSX 템플릿 선택")
        use_default_prev = st.checkbox("기본 '6.대기 방지시설 운영현황(26년_9월).xlsm' 템플릿 사용", value=True, key="prev_tpl_check")
        
        uploaded_prev_template = None
        if not use_default_prev:
            uploaded_prev_template = st.file_uploader("원본 XLSM/XLSX 템플릿 파일 업로드", type=["xlsm", "xlsx"], key="prev_tpl_file")
            
        if "custom_prev6" not in st.session_state:
            st.session_state["custom_prev6"] = {}

        with st.expander("⚙️ 날짜별 가동시간 수정 (콤보박스 선택 및 좌측 기존 / 우측 수정시간)", expanded=False):
            # 1. Date ComboBox
            dates_list6 = [f"202610{d:02d}" for d in range(1, 32)]
            sel_date6 = st.selectbox("📅 조회 및 수정할 가동일자 선택", options=dates_list6, index=0, key="sel_date6")
            
            from datetime import datetime
            dt_obj6 = datetime.strptime(sel_date6, "%Y%m%d").date()
            weekday_kr6 = ["월", "화", "수", "목", "금", "토", "일"][dt_obj6.weekday()]
            is_wkd6 = dt_obj6.weekday() in (5, 6) or sel_date6 in HOLIDAYS
            st.info(f"선택 일자: **{sel_date6} ({weekday_kr6}요일)** | " + ("🔴 주말/공휴일 (기본 0시간)" if is_wkd6 else "🔵 평일"))

            filter_kw6 = st.text_input("🔍 공정명 / 시설명 / 코드 검색", value="", key="filter6")
            
            facs6_list = get_facility_metadata(DEFAULT_AIR_PREVENTION_TEMPLATE, 6)
            if filter_kw6:
                facs6_list = [f for f in facs6_list if filter_kw6.lower() in f["code"].lower() or filter_kw6.lower() in f["proc"].lower() or filter_kw6.lower() in f["fac_name"].lower() or filter_kw6.lower() in f["sub_name"].lower()]

            table6_data = []
            for fac in facs6_list:
                f_code = fac["code"]
                def_h = get_default_facility_hours(sel_date6, f_code, is_wkd6)
                cur_h = st.session_state["custom_prev6"].get((sel_date6, f_code), def_h)
                table6_data.append({
                    "운영일자": sel_date6,
                    "시설관리번호": f_code,
                    "공정명": fac["proc"],
                    "방지시설명": f"{fac['fac_name']} ({fac['sub_name']})",
                    "기존 입력/계산 데이터 (시)": def_h,
                    "변경할 수정시간 (시)": cur_h
                })

            df_ed6 = pd.DataFrame(table6_data)
            edited_df6 = st.data_editor(
                df_ed6,
                column_config={
                    "운영일자": st.column_config.TextColumn(disabled=True),
                    "시설관리번호": st.column_config.TextColumn(disabled=True),
                    "공정명": st.column_config.TextColumn(disabled=True),
                    "방지시설명": st.column_config.TextColumn(disabled=True),
                    "기존 입력/계산 데이터 (시)": st.column_config.NumberColumn(disabled=True, help="기존 규칙/수식 원본 시간"),
                    "변경할 수정시간 (시)": st.column_config.NumberColumn(min_value=0, max_value=24, step=1, help="우측에서 직접 수정시간 입력")
                },
                disabled=["운영일자", "시설관리번호", "공정명", "방지시설명", "기존 입력/계산 데이터 (시)"],
                use_container_width=True,
                hide_index=True,
                key=f"ed6_{sel_date6}"
            )

            for idx, r in edited_df6.iterrows():
                fc = r["시설관리번호"]
                mh = r["변경할 수정시간 (시)"]
                oh = r["기존 입력/계산 데이터 (시)"]
                if mh != oh:
                    st.session_state["custom_prev6"][(sel_date6, fc)] = mh
                elif (sel_date6, fc) in st.session_state["custom_prev6"] and mh == oh:
                    del st.session_state["custom_prev6"][(sel_date6, fc)]

            if st.session_state["custom_prev6"]:
                st.success(f"✏️ 총 {len(st.session_state['custom_prev6']):,}개 항목에 수동 수정시간이 설정되었습니다.")
                if st.button("🗑️ 6번 수동 수정사항 전체 초기화", key="rst6"):
                    st.session_state["custom_prev6"] = {}
                    st.rerun()

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
        
    if uploaded_prev_sub:
        temp_prev_sub_path = "temp_prev_sub.xlsx"
        with open(temp_prev_sub_path, "wb") as f:
            f.write(uploaded_prev_sub.getbuffer())
            
        try:
            if use_default_prev and os.path.exists(DEFAULT_AIR_PREVENTION_TEMPLATE):
                template_path = DEFAULT_AIR_PREVENTION_TEMPLATE
            elif uploaded_prev_template:
                ext = os.path.splitext(uploaded_prev_template.name)[1].lower()
                template_path = f"temp_prev_template{ext}"
                with open(template_path, "wb") as f:
                    f.write(uploaded_prev_template.getbuffer())
            else:
                st.error("기준 엑셀 템플릿이 지정되지 않았습니다.")
                st.stop()
                
            is_template_xlsm = template_path.lower().endswith(".xlsm")
            ext_out = ".xlsm" if is_template_xlsm else ".xlsx"
            temp_output = f"temp_prev_output{ext_out}"

            with st.spinner("⏳ VBA 매크로 및 30개 방지시설 운영현황 (주말/공휴일/평일 인자 및 전력사용량) 계산 중..."):
                df_prev_prev, total_proc_rows = process_air_prevention(temp_prev_sub_path, template_path, temp_output, custom_hours_map=st.session_state.get("custom_prev6"))
                
            prev_month = 9
            if not df_prev_prev.empty and "운영일자" in df_prev_prev.columns:
                first_dt = str(df_prev_prev["운영일자"].iloc[0])
                if len(first_dt) >= 6:
                    try:
                        prev_month = int(first_dt[4:6])
                    except ValueError:
                        prev_month = 9

            output_prev_filename = f"6.대기_방지시설_운영현황(26년_{prev_month}월){ext_out}"
            output_prev_filepath = os.path.join(BASE_DIR, output_prev_filename)
            if os.path.exists(temp_output):
                os.replace(temp_output, output_prev_filepath)

            st.session_state["module_status"][6] = "normal"
            st.success(f"✅ 자동 계산 완료! (총 {total_proc_rows:,}개 레코드 생성)")
            st.dataframe(df_prev_prev, use_container_width=True, height=350)
            
            mime_type = "application/vnd.ms-excel.sheet.macroEnabled.12" if is_template_xlsm else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            if st.button(f"🚀 '6. 대기 방지시설 운영현황' ({ext_out}) 파일 생성", type="primary", use_container_width=True):
                st.balloons()
                st.success(f"🎉 '{output_prev_filename}' 파일 작성이 완료되었습니다!")
                
                with open(output_prev_filepath, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"📥 {output_prev_filename} 다운로드",
                    data=file_bytes,
                    file_name=output_prev_filename,
                    mime=mime_type,
                    use_container_width=True
                )
        except Exception as e:
            st.session_state["module_status"][6] = "error"
            st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
# -----------------------------------------------------------------------------
# 8. 연료사용량 작성
# -----------------------------------------------------------------------------
elif "연료사용량" in menu:
    st.session_state["module_status"][8] = "normal"
    # st.title("🔥 8. 연료사용량")
    render_work_manual(8)
    render_validation_results(8)
    st.markdown(
        "대시보드 내에서 설비별/일자별 연료 사용량 수치를 입력 및 수정하고, "
        "통합환경관리 양식에 맞는 **표준 엑셀 파일(`8.연료사용량.xlsx`)**로 자동 생성합니다."
    )
    st.divider()

    # 현재 선택된 년월 (세션 상태에서 미리 가져옴)
    sel_year = st.session_state.get("fuel_year", 2026)
    sel_month = st.session_state.get("fuel_month", 10)
    num_days = calendar.monthrange(sel_year, sel_month)[1]

    bo200_ratio_val = 1.288
    bo300_ratio_val = 1.579

    # 세션 상태 초기화 (일자별 기본값)
    for d in range(1, 32):
        if f"fuel_hm01b_{d}" not in st.session_state:
            st.session_state[f"fuel_hm01b_{d}"] = 0.0
        if f"fuel_bo200_raw_{d}" not in st.session_state:
            st.session_state[f"fuel_bo200_raw_{d}"] = 0.0
        if f"fuel_bo300_raw_{d}" not in st.session_state:
            st.session_state[f"fuel_bo300_raw_{d}"] = 0.0

    # 1️⃣ 최상단: 월간 총 사용량 요약
    st.subheader("1️⃣ 월간 총 사용량 요약")
    sum_hm = sum(st.session_state.get(f"fuel_hm01b_{d}", 0.0) for d in range(1, num_days + 1))
    sum_bo200_r = sum(st.session_state.get(f"fuel_bo200_raw_{d}", 0.0) for d in range(1, num_days + 1))
    sum_bo200_c = sum_bo200_r * bo200_ratio_val
    sum_bo300_r = sum(st.session_state.get(f"fuel_bo300_raw_{d}", 0.0) for d in range(1, num_days + 1))
    sum_bo300_c = sum_bo300_r * bo300_ratio_val
    total_lng = sum_hm + sum_bo200_c + sum_bo300_c

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🔥 HM-01B (열처리로)", f"{sum_hm:,.2f} ㎥")
    m2.metric("💨 BO-200 (산업용 보일러)", f"{sum_bo200_c:,.2f} ㎥")
    m3.metric("💨 BO-300 (산업용 보일러)", f"{sum_bo300_c:,.2f} ㎥")
    m4.metric("🌐 총 LNG 사용량", f"{total_lng:,.2f} ㎥")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2️⃣ 일자별 연료 사용량 수치 입력 (바로 위에 년월 선택 배치)
    st.subheader("2️⃣ 일자별 연료 사용량 수치 입력 (Editable Table)")

    col_y, col_m, col_info = st.columns([1, 1, 2])
    with col_y:
        sel_year = st.selectbox("📅 사용연도 선택", options=[2025, 2026, 2027], index=1, key="fuel_year")
    with col_m:
        sel_month = st.selectbox("📅 사용월 선택", options=list(range(1, 13)), index=9, key="fuel_month")
    
    num_days = calendar.monthrange(sel_year, sel_month)[1]
    month_str = f"{sel_year}{sel_month:02d}"

    with col_info:
        st.info(f"💡 **선택 년월**: `{sel_year}년 {sel_month}월` (`{month_str}`, 총 {num_days}일)\n'8-연료사용량' 및 '작성은 여기에' 시트가 동시에 작성됩니다.")

    table_data = []
    days_ko = ["월", "화", "수", "목", "금", "토", "일"]

    for d in range(1, num_days + 1):
        dt = datetime.date(sel_year, sel_month, d)
        day_str = f"{sel_month}월 {d:02d}일 ({days_ko[dt.weekday()]})"
        
        hm_val = float(st.session_state.get(f"fuel_hm01b_{d}", 0.0))
        bo200_r = float(st.session_state.get(f"fuel_bo200_raw_{d}", 0.0))
        bo200_c = round(bo200_r * bo200_ratio_val, 2)
        bo300_r = float(st.session_state.get(f"fuel_bo300_raw_{d}", 0.0))
        bo300_c = round(bo300_r * bo300_ratio_val, 2)

        table_data.append({
            "일자": day_str,
            "일(Day)": d,
            "열처리로 HM-01B (㎥)": hm_val,
            "BO-200 검침값 (㎥)": bo200_r,
            "BO-200 보정사용량 (㎥)": bo200_c,
            "BO-300 검침값 (㎥)": bo300_r,
            "BO-300 보정사용량 (㎥)": bo300_c,
        })

    df_fuel = pd.DataFrame(table_data)

    edited_df = st.data_editor(
        df_fuel,
        column_config={
            "일자": st.column_config.TextColumn("일자", disabled=True, width="medium"),
            "일(Day)": st.column_config.NumberColumn("일", disabled=True, width="small"),
            "열처리로 HM-01B (㎥)": st.column_config.NumberColumn("열처리로 HM-01B (㎥)", min_value=0.0, step=1.0, format="%.2f"),
            "BO-200 검침값 (㎥)": st.column_config.NumberColumn("BO-200 검침값 (㎥)", min_value=0.0, step=1.0, format="%.2f"),
            "BO-200 보정사용량 (㎥)": st.column_config.NumberColumn("BO-200 보정사용량 (㎥)", disabled=True, format="%.2f"),
            "BO-300 검침값 (㎥)": st.column_config.NumberColumn("BO-300 검침값 (㎥)", min_value=0.0, step=1.0, format="%.2f"),
            "BO-300 보정사용량 (㎥)": st.column_config.NumberColumn("BO-300 보정사용량 (㎥)", disabled=True, format="%.2f"),
        },
        hide_index=True,
        use_container_width=True,
        height=420
    )

    for idx, row in edited_df.iterrows():
        d = int(row["일(Day)"])
        st.session_state[f"fuel_hm01b_{d}"] = float(row["열처리로 HM-01B (㎥)"])
        st.session_state[f"fuel_bo200_raw_{d}"] = float(row["BO-200 검침값 (㎥)"])
        st.session_state[f"fuel_bo300_raw_{d}"] = float(row["BO-300 검침값 (㎥)"])

    # 3️⃣ 엑셀 파일 생성 및 다운로드
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")

    if st.button("🚀 '8.연료사용량.xlsx' 파일 작성", type="primary", use_container_width=True):
        try:
            hm_list = [st.session_state.get(f"fuel_hm01b_{d}", 0.0) for d in range(1, 32)]
            bo200_r_list = [st.session_state.get(f"fuel_bo200_raw_{d}", 0.0) for d in range(1, 32)]
            bo200_c_list = [bo200_r_list[d-1] * bo200_ratio_val for d in range(1, 32)]
            bo300_r_list = [st.session_state.get(f"fuel_bo300_raw_{d}", 0.0) for d in range(1, 32)]
            bo300_c_list = [bo300_r_list[d-1] * bo300_ratio_val for d in range(1, 32)]

            daily_payload = {
                "HM-01B": hm_list,
                "BO-200_raw": bo200_r_list,
                "BO-200_final": bo200_c_list,
                "BO-300_raw": bo300_r_list,
                "BO-300_final": bo300_c_list
            }

            fuel_excel_bytes = generate_fuel_consumption_excel(
                year=sel_year,
                month=sel_month,
                daily_data=daily_payload,
                bo200_ratio=bo200_ratio_val,
                bo300_ratio=bo300_ratio_val,
                template_path=os.path.join(BASE_DIR, "template_8_fuel_consumption.xlsx")
            )

            out_filename = f"8.연료사용량({sel_month}월).xlsx"
            st.balloons()
            st.success(f"🎉 '{out_filename}' 파일 작성이 완료되었습니다!")

            st.download_button(
                label=f"📥 {out_filename} 다운로드",
                data=fuel_excel_bytes,
                file_name=out_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ 엑셀 파일 생성 중 오류 발생: {e}")



# -----------------------------------------------------------------------------
# 10. 기타화학물질 사용량 모듈
# -----------------------------------------------------------------------------
elif "기타화학물질 사용량" in menu or "기타화학물질" in menu:
    import chemicals_processor
    importlib.reload(chemicals_processor)
    from chemicals_processor import (
        CHEMICAL_MASTER,
        FIXED_CHEMICAL_VALUES,
        get_gas_sheets,
        parse_gas_inspection_file,
        generate_chemical_excel
    )

    icon9_path = os.path.join(BASE_DIR, "icon_item9.png")
    if os.path.exists(icon9_path):
        icon9_b64 = get_image_base64(icon9_path)
        st.markdown(
            f'''
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <img src="data:image/png;base64,{icon9_b64}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                <span style="font-size: 2.2rem; font-weight: 700; color: #111;">9. 기타화학물질 사용량</span>
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        pass
        # st.title("🧪 9. 기타화학물질 사용량")
    render_work_manual(9)
    render_validation_results(9)
    st.markdown(
        "가스 저장품 점검표(`2026년_10월_가스_저장품_점검표_양식.xlsx`)를 업로드하면, "
        "유해화학물질 6종(**수소, 아르곤, 질소, 과산화수소, 불산, 질산**)의 월간 사용량을 자동 집계하여 "
        "표준 엑셀 서식(`10.기타화학물질_사용량.xlsx`)의 **빨간색 글자 영역**에 반영하고 최신화합니다.<br>"
        "📌 **고정 항목**: **조관유(300ℓ), 현상액(0ℓ), 산소제거제(30kg), 청관제(5ℓ)**<br>"
        "✏️ **사용자 입력 항목**: **고분자응집제, 소석회, 메탄올** 사용량은 아래 수치 입력 상자에서 지정할 수 있습니다.",
        unsafe_allow_html=True
    )
    st.divider()

    c_y, c_m, c_info = st.columns([1, 1, 2])
    with c_y:
        sel_chem_year = st.selectbox("📅 작성 연도", options=[2025, 2026, 2027], index=1, key="chem_year")
    with c_m:
        sel_chem_month = st.selectbox("📅 작성 월", options=list(range(1, 13)), index=9, key="chem_month")
    
    target_ym_str = f"{sel_chem_year}{sel_chem_month:02d}"
    
    with c_info:
        st.info(f"💡 **선택 년월**: `{sel_chem_year}년 {sel_chem_month}월` (`{target_ym_str}`)\n`10-기타화학물질 사용량` 및 `작성은 여기에` 시트가 동시에 작성됩니다.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_gas_file = st.file_uploader(
            "가스 저장품 점검표 엑셀(.xlsx, .xls) 업로드",
            type=["xlsx", "xls"],
            key="gas_inspection_file"
        )
        
        target_sheet_selected = None
        extracted_gas = {}
        if uploaded_gas_file:
            temp_gas_path = "temp_gas_uploaded.xlsx"
            with open(temp_gas_path, "wb") as f:
                f.write(uploaded_gas_file.getbuffer())
            
            avail_sheets = get_gas_sheets(temp_gas_path)
            if avail_sheets:
                default_sheet_idx = 0
                expected_sheet_name = f"{sel_chem_year}.{sel_chem_month}"
                if expected_sheet_name in avail_sheets:
                    default_sheet_idx = avail_sheets.index(expected_sheet_name)
                
                target_sheet_selected = st.selectbox("📑 점검표 월 시트 선택", options=avail_sheets, index=default_sheet_idx)
            
            try:
                extracted_gas = parse_gas_inspection_file(temp_gas_path, sheet_name=target_sheet_selected)
                st.session_state["module_status"][9] = "normal"
                st.success(f"✅ 가스 점검표 파싱 완료! ({target_sheet_selected or '기본'} 시트)")
            except Exception as ex:
                st.session_state["module_status"][9] = "error"
                st.error(f"❌ 가스 점검표 분석 중 오류: {ex}")

    with col2:
        st.subheader("2️⃣ 템플릿 서식 확인")
        DEFAULT_CHEM_TEMPLATE = os.path.join(BASE_DIR, "template_10_chemicals.xlsx")
        use_default_chem_tpl = st.checkbox("기본 템플릿 사용 (`template_10_chemicals.xlsx`)", value=True, key="use_default_chem_tpl")
        uploaded_chem_tpl = None
        if not use_default_chem_tpl:
            uploaded_chem_tpl = st.file_uploader("사용자 템플릿 업로드 (.xlsx)", type=["xlsx"], key="user_chem_tpl")

    st.divider()

    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
    st.caption("고분자응집제, 소석회, 메탄올의 사용량을 아래 상자에서 입력하세요.")

    col_input1, col_input2, col_input3 = st.columns(3)
    with col_input1:
        poly_val = st.number_input(
            "🧪 고분자응집제 사용량 (kg)",
            min_value=0.0,
            value=float(st.session_state.get("poly_val", 20.0)),
            step=1.0,
            format="%.2f",
            key="poly_val"
        )
    with col_input2:
        lime_val = st.number_input(
            "🧪 소석회 사용량 (톤)",
            min_value=0.0,
            value=float(st.session_state.get("lime_val", 97.54)),
            step=0.01,
            format="%.2f",
            key="lime_val"
        )
    with col_input3:
        meoh_val = st.number_input(
            "🧪 메탄올 사용량 (톤)",
            min_value=0.0,
            value=float(st.session_state.get("meoh_val", 0.41)),
            step=0.01,
            format="%.2f",
            key="meoh_val"
        )

    st.divider()

    st.subheader("4️⃣ 기타화학물질 월간 사용량 종합 미리보기")
    st.caption("🔴 가스 6종: 점검표 자동 집계 | 🔒 고정 4종: 표준 고정값 | ✏️ 폐수처리 3종: 상단 입력값 반영")

    table_rows = []
    for item in CHEMICAL_MASTER:
        c_name = item["name"]
        
        if c_name in FIXED_CHEMICAL_VALUES:
            val = FIXED_CHEMICAL_VALUES[c_name]
            src = f"🔒 고정값 ({val:g} {item['unit_name']})"
        elif c_name == "고분자응집제":
            val = poly_val
            src = "✏️ 사용자 직접입력"
        elif c_name == "소석회":
            val = lime_val
            src = "✏️ 사용자 직접입력"
        elif c_name == "메탄올":
            val = meoh_val
            src = "✏️ 사용자 직접입력"
        elif c_name in extracted_gas and extracted_gas[c_name] > 0:
            val = extracted_gas[c_name]
            src = "🔴 가스점검표 자동집계"
        else:
            val = item["default_qty"]
            src = "✏️ 직접입력 가능"

        table_rows.append({
            "No": item["no"],
            "공정번호": item["code"],
            "공정명": item["process"],
            "화학물질명": c_name,
            "사용량": float(val),
            "단위": item["unit_name"],
            "구분": src,
            "비고": item["remark"]
        })

    df_chem = pd.DataFrame(table_rows)

    edited_chem_df = st.data_editor(
        df_chem,
        column_config={
            "No": st.column_config.NumberColumn("No", disabled=True, width="small"),
            "공정번호": st.column_config.TextColumn("공정번호", disabled=True, width="small"),
            "공정명": st.column_config.TextColumn("공정명", disabled=True, width="medium"),
            "화학물질명": st.column_config.TextColumn("화학물질명", disabled=True, width="medium"),
            "사용량": st.column_config.NumberColumn("사용량", min_value=0.0, step=0.01, format="%.2f"),
            "단위": st.column_config.TextColumn("단위", disabled=True, width="small"),
            "구분": st.column_config.TextColumn("구분", disabled=True, width="medium"),
            "비고": st.column_config.TextColumn("비고", disabled=True, width="large"),
        },
        hide_index=True,
        use_container_width=True,
        height=450
    )

    st.divider()

    st.subheader("5️⃣ 표준 엑셀 파일 생성 및 다운로드")
    if st.button("🚀 '10.기타화학물질_사용량.xlsx' 파일 추출", type="primary", use_container_width=True):
        try:
            final_chem_dict = {}
            for idx, row in edited_chem_df.iterrows():
                final_chem_dict[row["화학물질명"]] = float(row["사용량"])

            # Guarantee fixed items regardless of user edits in table
            for k, v in FIXED_CHEMICAL_VALUES.items():
                final_chem_dict[k] = v

            # Explicitly pass user entered values for poly, lime, meoh
            final_chem_dict["고분자응집제"] = float(poly_val)
            final_chem_dict["소석회"] = float(lime_val)
            final_chem_dict["메탄올"] = float(meoh_val)

            DEFAULT_CHEM_TEMPLATE = os.path.join(BASE_DIR, "template_10_chemicals.xlsx")
            if use_default_chem_tpl and os.path.exists(DEFAULT_CHEM_TEMPLATE):
                tpl_path = DEFAULT_CHEM_TEMPLATE
            elif uploaded_chem_tpl:
                tpl_path = "temp_chem_tpl.xlsx"
                with open(tpl_path, "wb") as f:
                    f.write(uploaded_chem_tpl.getbuffer())
            else:
                st.error("엑셀 템플릿 파일이 없습니다.")
                st.stop()

            out_filename = f"10.기타화학물질_사용량({sel_chem_month}월).xlsx"
            out_file_path = os.path.join(BASE_DIR, out_filename)

            generate_chemical_excel(
                target_month_str=target_ym_str,
                chemical_data_dict=final_chem_dict,
                template_path=tpl_path,
                output_path=out_file_path
            )

            with open(out_file_path, "rb") as f:
                excel_bytes = f.read()

            st.balloons()
            st.success(f"🎉 '{out_filename}' 생성 완료!")

            st.download_button(
                label=f"📥 {out_filename} 다운로드",
                data=excel_bytes,
                file_name=out_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ 엑셀 파일 생성 중 오류 발생: {e}")


# -----------------------------------------------------------------------------
# 11. 원부원료 사용량 및 제품 생산량 모듈 (자동화 구동 중)
# -----------------------------------------------------------------------------
elif "원부원료 사용량 및 제품 생산량" in menu or "원부원료" in menu or "제품 생산량" in menu:
    # st.title("📦 10. 원부원료 사용량 및 제품 생산량")
    render_validation_results(10)
    render_work_manual(10)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 월간 적용 일자 선택 & 파일 업로드")
        
        sel_month11 = st.selectbox("📅 적용 월 선택 (기본 10월)", options=list(range(1, 13)), index=9, key="sel_m11")
        sel_year11 = 2026
        target_ym11 = f"{sel_year11}{sel_month11:02d}"
        
        uploaded_datagrid = st.file_uploader("DataGrid 엑셀 파일(.xlsx) 업로드", type=["xlsx", "xls"], key="dg_excel_file")
        st.caption("※ DataGrid 파일 내 '조관수율-투입량(kg)'과 '조관수율-양품량(kg)'을 자동으로 추출하여 1000으로 나누어 '톤(ton)' 단위로 환산합니다.")

    with col2:
        st.subheader("2️⃣ 템플릿 파일 선택")
        use_default11 = st.checkbox("기본 9번(원부원료) 및 12번(제품생산량) 템플릿 사용", value=True, key="tpl11_check")
        
        uploaded_raw_template, uploaded_products_template = None, None
        if not use_default11:
            uploaded_raw_template = st.file_uploader("9번 원부원료 템플릿(.xlsx) 업로드", type=["xlsx"], key="raw_tpl_file")
            uploaded_products_template = st.file_uploader("12번 제품생산량 템플릿(.xlsx) 업로드", type=["xlsx"], key="products_tpl_file")

    st.divider()
    
    if uploaded_datagrid:
        try:
            raw_mats_parsed, products_parsed = parse_datagrid_excel(uploaded_datagrid)
            st.session_state["module_status"][10] = "normal"
            st.success("✅ DataGrid 엑셀 파싱 및 톤(ton) 환산 완료!")
        except Exception as e:
            st.session_state["module_status"][10] = "error"
            st.error(f"❌ DataGrid 파일 처리 중 오류 발생: {e}")
            raw_mats_parsed, products_parsed = None, None
    else:
        sample_dg_path = r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\.user_uploaded\media_1794890006306_1b57896b.xlsx"
        if os.path.exists(sample_dg_path):
            raw_mats_parsed, products_parsed = parse_datagrid_excel(sample_dg_path)
            st.info("💡 DataGrid 엑셀 파일을 업로드하면 수치가 자동 갱신됩니다. (현재 최근 파일 수치 연동 중)")
        else:
            raw_mats_parsed, products_parsed = None, None

    if raw_mats_parsed and products_parsed:
        st.subheader("3️⃣ 데이터 변환 및 자동 생성")
        
        tab1, tab2 = st.tabs(["📊 9. 원부원료 사용량 (7개 공정)", "🏭 12. 제품 생산량 (2개 제품)"])
        
        with tab1:
            st.markdown("##### 📌 원부원료 사용량 (조관수율 투입량 → 톤 환산)")
            df_rm_data = []
            for code, d in raw_mats_parsed.items():
                df_rm_data.append({
                    "공정코드": d["code"],
                    "공정명": d["name"],
                    "원료명": d["material"],
                    "사용량 (톤)": d["amount"],
                    "단위": "톤 (12)"
                })
            df_rm = pd.DataFrame(df_rm_data)
            edited_rm = st.data_editor(
                df_rm,
                column_config={
                    "공정코드": st.column_config.TextColumn(disabled=True),
                    "공정명": st.column_config.TextColumn(disabled=True),
                    "원료명": st.column_config.TextColumn(disabled=True),
                    "사용량 (톤)": st.column_config.NumberColumn(format="%.3f"),
                    "단위": st.column_config.TextColumn(disabled=True)
                },
                disabled=["공정코드", "공정명", "원료명", "단위"],
                use_container_width=True,
                hide_index=True,
                key="ed_rm_tab"
            )
            
        with tab2:
            st.markdown("##### 📌 제품 생산량 (조관수율 양품량 → 톤 환산)")
            df_pr_data = []
            for code, d in products_parsed.items():
                df_pr_data.append({
                    "제품코드": d["code"],
                    "제품명": d["name"].replace("\n", " "),
                    "제품구분": d["category"],
                    "생산량 (톤)": d["amount"],
                    "단위": "톤 (12)"
                })
            df_pr = pd.DataFrame(df_pr_data)
            edited_pr = st.data_editor(
                df_pr,
                column_config={
                    "제품코드": st.column_config.TextColumn(disabled=True),
                    "제품명": st.column_config.TextColumn(disabled=True),
                    "제품구분": st.column_config.TextColumn(disabled=True),
                    "생산량 (톤)": st.column_config.NumberColumn(format="%.3f"),
                    "단위": st.column_config.TextColumn(disabled=True)
                },
                disabled=["제품코드", "제품명", "제품구분", "단위"],
                use_container_width=True,
                hide_index=True,
                key="ed_pr_tab"
            )

        st.divider()
        st.subheader("4️⃣ 최종 엑셀 파일 추출")
        
        btn_col1, btn_col2 = st.columns([1, 1])
        
        final_rm_dict = {}
        for _, row in edited_rm.iterrows():
            c = row["공정코드"]
            final_rm_dict[c] = {"amount": float(row["사용량 (톤)"])}

        final_pr_dict = {}
        for _, row in edited_pr.iterrows():
            c = row["제품코드"]
            final_pr_dict[c] = {"amount": float(row["생산량 (톤)"])}

        with btn_col1:
            fn9 = f"9.원부원료_사용량({sel_month11}월).xlsx"
            out9_path = os.path.join(BASE_DIR, f"temp_{fn9}")
            tpl9_path = DEFAULT_RAW_MATERIALS_TEMPLATE if use_default11 or not uploaded_raw_template else "temp_raw_tpl.xlsx"
            if uploaded_raw_template and not use_default11:
                with open(tpl9_path, "wb") as f:
                    f.write(uploaded_raw_template.getbuffer())
                    
            generate_raw_materials_excel(target_ym11, final_rm_dict, tpl9_path, out9_path)
            
            with open(out9_path, "rb") as f:
                st.download_button(
                    label=f"📥 '{fn9}' 다운로드",
                    data=f.read(),
                    file_name=fn9,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )

        with btn_col2:
            fn12 = f"12.제품_생산량({sel_month11}월).xlsx"
            out12_path = os.path.join(BASE_DIR, f"temp_{fn12}")
            tpl12_path = DEFAULT_PRODUCTS_TEMPLATE if use_default11 or not uploaded_products_template else "temp_prod_tpl.xlsx"
            if uploaded_products_template and not use_default11:
                with open(tpl12_path, "wb") as f:
                    f.write(uploaded_products_template.getbuffer())
                    
            generate_products_excel(target_ym11, final_pr_dict, tpl12_path, out12_path)
            
            with open(out12_path, "rb") as f:
                st.download_button(
                    label=f"📥 '{fn12}' 다운로드",
                    data=f.read(),
                    file_name=fn12,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
# -----------------------------------------------------------------------------
# 나머지 모듈 범용 템플릿 화면 (확장 아키텍처)
# -----------------------------------------------------------------------------
else:
    module_name = menu
    curr_mod_num = 1
    for num, title in RAW_MENU_ITEMS:
        if title in module_name:
            curr_mod_num = num
            break
            
    # st.title(f"{module_name}")
    render_work_manual(curr_mod_num)
    render_validation_results(curr_mod_num)
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_file = st.file_uploader(f"{module_name} 관련 자료 업로드 (PDF, XLSX, CSV)", type=["pdf", "xlsx", "csv", "xls"], key=f"file_{module_name}")
        
    with col2:
        st.subheader("2️⃣ 엑셀 양식/템플릿 선택")
        st.file_uploader(f"기준 엑셀 템플릿 파일 업로드", type=["xlsx"], key=f"template_{module_name}")

    st.divider()
    st.subheader("3️⃣ 데이터 변환 및 자동 생성")
    if uploaded_file:
        st.success(f"✅ '{uploaded_file.name}' 파일 수신 완료!")
        st.warning("💡 해당 모듈의 샘플 PDF/엑셀 자료와 매핑 규칙을 공유해주시면, '2. 수질' 및 '5. 배출구' 모듈처럼 자동 파싱 및 엑셀 생성을 즉시 완성해드립니다.")
        st.button(f"🚀 {module_name} 엑셀 데이터 작성", type="primary", use_container_width=True, disabled=True)
