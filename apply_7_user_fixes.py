import re
import os

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove "원하시는 관리 항목을 선택하세요."
content = content.replace('st.sidebar.markdown("원하시는 관리 항목을 선택하세요.")\n', '')
content = content.replace('st.sidebar.markdown("원하시는 관리 항목을 선택하세요.")', '')

# 2. Remove "(주)세아제강 창원공장 안전환경팀 우정훈" and sidebar divider at bottom
sidebar_footer_pattern = r'st\.sidebar\.divider\(\)\s*st\.sidebar\.markdown\(\s*\'<div style="font-size: 13px; color: #2C4A35; font-weight: 700; padding: 6px 0;">\(주\)세아제강 창원공장 안전환경팀 우정훈</div>\',\s*unsafe_allow_html=True\s*\)'
content = re.sub(sidebar_footer_pattern, '', content)

# 3. Update CSS: Remove bold from sidebar radio labels (Item 2) + Fix file uploader overlapping text (Item 4)
new_style = """st.markdown(
    \"\"\"
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;600;700&display=swap');

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

    /* Streamlit 아이콘 & 파일 업로더 내 아이콘 폰트 복원 (overlap 방지) */
    [data-testid="stIcon"],
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
    </style>
    \"\"\",
    unsafe_allow_html=True
)"""

style_pattern = r'st\.markdown\(\s*"""\s*<style>.*?</style>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(style_pattern, new_style, content, flags=re.DOTALL)

# 4. Fix Item 5: Module 5 & Module 6 separation
# Ensure "elif "6. 대기" in menu:" is placed properly at root level of menu checking
old_m6_start = """# -----------------------------------------------------------------------------
# 6. 대기 방지시설 운영현황 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
    icon6_path = os.path.join(BASE_DIR, "icon_item6.png")"""

new_m6_start = """# -----------------------------------------------------------------------------
# 6. 대기 방지시설 운영현황 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
elif "6. 대기" in menu:
    icon6_path = os.path.join(BASE_DIR, "icon_item6.png")"""

content = content.replace(old_m6_start, new_m6_start)

# 5. Fix Item 6: Delete "검침: 0.00" in Module 8 (연료사용량)
content = content.replace('m2.metric("💨 BO-200 (산업용 보일러)", f"{sum_bo200_c:,.2f} ㎥", f"검침: {sum_bo200_r:,.2f}")', 'm2.metric("💨 BO-200 (산업용 보일러)", f"{sum_bo200_c:,.2f} ㎥")')
content = content.replace('m3.metric("💨 BO-300 (산업용 보일러)", f"{sum_bo300_c:,.2f} ㎥", f"검침: {sum_bo300_r:,.2f}")', 'm3.metric("💨 BO-300 (산업용 보일러)", f"{sum_bo300_c:,.2f} ㎥")')

# 6. Fix Item 7: Remove "👈 ... 업로드하세요 / 업로드하면 ..." info banners across modules
info_upload_patterns = [
    r'st\.info\("👈 왼쪽에서 대기 성적서 PDF 파일\(\.pdf\)을 업로드하세요\."\)',
    r'st\.info\("👈 왼쪽에서 수질 성적서 PDF 파일\(\.pdf\)을 업로드하세요\."\)',
    r'st\.info\("👈 왼쪽에서 \'5\. 배출구 가동시간\' 엑셀 파일\(\.xlsx\)을 업로드하면.*?"\)',
    r'st\.info\("👈 위에서 \'설비별 가동현황 조회_\' 엑셀 파일\(\.xlsx\)을 업로드하면 자동으로 가동시간이 계산됩니다\."\)',
    r'st\.info\("👈 왼쪽에서 \'5\. 배출구 가동시간\' 엑셀 파일\(\.xlsx\)을 업로드하면.*?"\)',
    r'st\.info\(f"👈 왼쪽에서 \{module_name\} 관련 원본 파일\(성적서/운영일지 등\)을 업로드하세요\."\)'
]

for pat in info_upload_patterns:
    content = re.sub(pat, '', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Applied all 7 requested modifications successfully!")
