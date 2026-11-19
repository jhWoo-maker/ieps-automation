import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the style block with the new IEPS Noto Sans KR Eco-friendly theme
new_style_block = """st.markdown(
    \"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

    /* IEPS 웹 표준 Noto Sans KR 폰트 적용 */
    html, body, [class*="css"], [class*="st-"], .stMarkdown, button, input, select, textarea {
        font-family: 'Noto Sans KR', 'Pretendard', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', '맑은 고딕', sans-serif !important;
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

    div[data-testid="stSidebar"] span, div[data-testid="stSidebar"] label {
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

# Replace old style block
pattern = r'st\.markdown\(\s*"""\s*<style>.*?</style>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(pattern, new_style_block, content, flags=re.DOTALL)

# Update render_work_manual function to eco-friendly styling
old_render_manual = """def render_work_manual(item_num):
    steps = MODULE_MANUALS.get(item_num, [])
    if not steps:
        return
    items_html = "".join([f"<li>{step}</li>" for step in steps])
    st.markdown(
        f'''
        <div style="background-color: #F8F9FA; border-left: 4px solid #946CEE; padding: 12px 16px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-weight: bold; font-size: 15px; color: #111; margin-bottom: 6px;">📋 작업 매뉴얼</div>
            <ol style="margin: 0; padding-left: 20px; color: #333; line-height: 1.6; font-size: 14px;">
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
        <div style="background-color: #EBF5ED; border-left: 4px solid #2E7D32; padding: 14px 18px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px; box-shadow: 0 2px 6px rgba(46, 125, 50, 0.08);">
            <div style="font-weight: 700; font-size: 15px; color: #1B4D2E; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                🌿 <span style="letter-spacing: -0.3px;">작업 매뉴얼</span>
            </div>
            <ol style="margin: 0; padding-left: 20px; color: #2C4A35; line-height: 1.65; font-size: 14px;">
                {items_html}
            </ol>
        </div>
        ''',
        unsafe_allow_html=True
    )"""

content = content.replace(old_render_manual, new_render_manual)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully applied IEPS Noto Sans KR font & Eco-Friendly Workplace theme!")
