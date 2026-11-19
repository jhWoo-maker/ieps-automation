import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_style = """st.markdown(
    \"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

    /* IEPS 웹 표준 Noto Sans KR 폰트 적용 (아이콘 폰트 제외) */
    html, body, p, div, label, h1, h2, h3, h4, h5, h6, input, select, textarea {
        font-family: 'Noto Sans KR', 'Pretendard', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', '맑은 고딕', sans-serif;
    }

    /* Streamlit 아이콘 및 사이드바 토글 버튼 아이콘 폰트 복원 */
    [data-testid="stIcon"],
    [class*="Material"],
    [class*="material"],
    i.material-icons,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarCollapseButton"] * {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }

    /* 친환경 사업장 웹 디자인 배경 & 여백 */
    .stApp {
        background-color: #F7FBF8 !important;
    }

    /* 사이드바 친환경 숲 그린 테마 */
    div[data-testid="stSidebar"] {
        background-color: #EEF4F0 !important;
        border-right: 1px solid #D2E4D6 !important;
    }

    div[data-testid="stSidebar"] label {
        color: #1B4D2E !important;
        font-weight: 500 !important;
    }

    /* 타이틀 & 헤더 디자인 */
    h1 {
        color: #1B4D2E !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }

    h2, h3, [data-testid="stSubheader"] {
        color: #2E7D32 !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }

    /* 기본 버튼 & 주요 버튼 (친환경 에코 그린) */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 5px rgba(46, 125, 50, 0.15) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* 다운로드 버튼 스타일 */
    div.stDownloadButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #1B5E20 !important;
    }

    /* 파일 업로더 테마 */
    div[data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #A5D6A7 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        transition: border-color 0.2s ease !important;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #2E7D32 !important;
        background-color: #F4F9F5 !important;
    }

    /* 데이터프레임 / 테이블 카드 테마 */
    div[data-testid="stDataFrame"] {
        border: 1px solid #D2E4D6 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        background-color: #FFFFFF !important;
    }

    /* 구분선 및 카테고리 디바인더 */
    hr {
        border-color: #D2E4D6 !important;
    }

    /* 알림 박스 (Success, Info, Warning) 친환경 커스텀 */
    div[data-testid="stNotification"] {
        border-radius: 8px !important;
    }
    </style>
    \"\"\",
    unsafe_allow_html=True
)"""

pattern = r'st\.markdown\(\s*"""\s*<style>.*?</style>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(pattern, new_style, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Icon font styling updated.")
