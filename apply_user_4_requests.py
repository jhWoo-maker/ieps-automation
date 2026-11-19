import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update style block with bold for all fonts, 32px title, and badge styling
new_style = """st.markdown(
    \"\"\"
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@600;700;800&display=swap');

    /* 모든 글꼴 bold 설정 & Pretendard/Gothic A1 적용 */
    html, body, p, div, label, h1, h2, h3, h4, h5, h6, input, select, textarea, button, span, ol, li {
        font-family: 'Pretendard', 'Gothic A1', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 700 !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }

    /* Streamlit 아이콘 폰트 유지 */
    [data-testid="stIcon"],
    [class*="Material"],
    [class*="material"],
    i.material-icons,
    [data-testid="collapsedControl"] *,
    [data-testid="stSidebarCollapseButton"] * {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }

    /* 사이드바 메뉴 뱃지 전용 스타일 */
    span.stMarkdownColoredBackground {
        border-radius: 10px !important;
        padding: 2px 7px !important;
        font-size: 11px !important;
        font-weight: 800 !important;
    }
    
    /* [ 검증 전 ] 뱃지 스타일: 진한 회색(#4A5568) 배경 & 선명한 흰색 글자 */
    span.stMarkdownColoredBackground[style*="245, 244, 242"],
    span.stMarkdownColoredBackground[style*="gray"],
    span.stMarkdownColoredBackground[style*="grey"] {
        background-color: #4A5568 !important;
        color: #FFFFFF !important;
    }

    /* 2. 메인 타이틀 (h1) 가독성 극대화 (32px Bold) */
    h1, [data-testid="stTitle"] {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #1B4D2E !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 12px !important;
        padding-top: 0px !important;
    }

    /* 서브헤더 (1️⃣, 2️⃣, 3️⃣) (20px Bold) */
    h2, h3, [data-testid="stSubheader"] {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #2E7D32 !important;
        letter-spacing: -0.3px !important;
        margin-top: 8px !important;
        margin-bottom: 10px !important;
    }

    /* 본문 텍스트 & 라벨 크기 (15.5px Bold) */
    p, label, div.stMarkdown, span {
        font-size: 15.5px !important;
        font-weight: 700 !important;
        line-height: 1.55 !important;
    }

    /* 사이드바 라벨 (15px Bold) */
    div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] span {
        font-size: 15px !important;
        color: #1B4D2E !important;
        font-weight: 700 !important;
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

    /* 파일 업로더 */
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
    </style>
    \"\"\",
    unsafe_allow_html=True
)"""

pattern = r'st\.markdown\(\s*"""\s*<style>.*?</style>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(pattern, new_style, content, flags=re.DOTALL)

# 2. Restore get_badge_label function
old_get_badge = """def get_badge_label(item_num, title):
    return title"""

new_get_badge = """def get_badge_label(item_num, title):
    status = st.session_state["module_status"].get(item_num, "pending")
    if status == "normal":
        return f"{title} :green-background[ 정상 ]"
    elif status == "error":
        return f"{title} :orange-background[ 오류 ]"
    else:
        return f"{title} :gray-background[ 검증 전 ]\""""

content = content.replace(old_get_badge, new_get_badge)

# 3. Add sidebar footer text: (주)세아제강 창원공장 안전환경팀 우정훈
old_sidebar_end = """menu = RAW_MENU_ITEMS[st.session_state["menu_index"]][1]"""

new_sidebar_end = """menu = RAW_MENU_ITEMS[st.session_state["menu_index"]][1]

st.sidebar.divider()
st.sidebar.markdown(
    '<div style="font-size: 13px; color: #2C4A35; font-weight: 700; padding: 6px 0;">(주)세아제강 창원공장 안전환경팀 우정훈</div>',
    unsafe_allow_html=True
)"""

if old_sidebar_end in content and "(주)세아제강 창원공장 안전환경팀 우정훈" not in content:
    content = content.replace(old_sidebar_end, new_sidebar_end)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied 4 user requests successfully.")
