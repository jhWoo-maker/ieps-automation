import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_style = """st.markdown(
    \"\"\"
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@300;400;500;600&display=swap');

    /* 부드러운 고급 Pretendard & Gothic A1 폰트 및 안티앨리어싱 적용 */
    html, body, p, div, label, h1, h2, h3, h4, h5, h6, input, select, textarea, button, span {
        font-family: 'Pretendard', 'Gothic A1', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif !important;
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

    /* 폰트 크기 30% 확대 (가독성 향상) */
    
    /* 1. 메인 타이틀 (h1) (19px -> 25px) */
    h1, [data-testid="stTitle"] {
        font-size: 25px !important;
        font-weight: 600 !important;
        color: #1B4D2E !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 8px !important;
        padding-top: 0px !important;
    }

    /* 2. 서브헤더 (1️⃣, 2️⃣, 3️⃣) (14.5px -> 19px) */
    h2, h3, [data-testid="stSubheader"] {
        font-size: 19px !important;
        font-weight: 600 !important;
        color: #2E7D32 !important;
        letter-spacing: -0.2px !important;
        margin-top: 6px !important;
        margin-bottom: 8px !important;
    }

    /* 3. 본문 텍스트 & 라벨 크기 (13px -> 16px) */
    p, label, div.stMarkdown, span {
        font-size: 16px !important;
        font-weight: 400 !important;
        line-height: 1.55 !important;
    }

    /* 4. 사이드바 라벨 (13px -> 16px) */
    div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] span {
        font-size: 15.5px !important;
        color: #1B4D2E !important;
        font-weight: 500 !important;
    }

    /* 친환경 사업장 배경 & 사이드바 테마 */
    .stApp {
        background-color: #F7FBF8 !important;
    }

    div[data-testid="stSidebar"] {
        background-color: #EEF4F0 !important;
        border-right: 1px solid #D2E4D6 !important;
    }

    /* 버튼 크기 및 폰트 (13px -> 15.5px) */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border-radius: 7px !important;
        border: none !important;
        font-size: 15.5px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        box-shadow: 0 1px 4px rgba(46, 125, 50, 0.12) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 3px 8px rgba(46, 125, 50, 0.2) !important;
    }

    /* 파일 업로더 적정 사이즈 */
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
        margin-top: 12px !important;
        margin-bottom: 12px !important;
    }
    </style>
    \"\"\",
    unsafe_allow_html=True
)"""

pattern = r'st\.markdown\(\s*"""\s*<style>.*?</style>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(pattern, new_style, content, flags=re.DOTALL)

# Update render_work_manual function to +30% size
old_render_manual = """def render_work_manual(item_num):
    steps = MODULE_MANUALS.get(item_num, [])
    if not steps:
        return
    items_html = "".join([f"<li>{step}</li>" for step in steps])
    st.markdown(
        f'''
        <div style="background-color: #EBF5ED; border-left: 3px solid #2E7D32; padding: 10px 14px; border-radius: 6px; margin-top: 6px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(46, 125, 50, 0.06);">
            <div style="font-weight: 600; font-size: 13.5px; color: #1B4D2E; margin-bottom: 5px; display: flex; align-items: center; gap: 5px;">
                🌿 <span style="letter-spacing: -0.2px;">작업 매뉴얼</span>
            </div>
            <ol style="margin: 0; padding-left: 18px; color: #2C4A35; line-height: 1.5; font-size: 12.5px;">
                {items_html}
            </ol>
        </div>
        ''',
        unsafe_allow_html=True
    )"""

new_render_manual = """def render_work_manual(item_num):
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
    )"""

content = content.replace(old_render_manual, new_render_manual)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Font sizes increased by 30%.")
