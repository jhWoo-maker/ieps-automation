import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update CSS for stIconMaterial and stMetric
old_css_part = '''    /* Streamlit 아이콘 & 파일 업로더 내 아이콘 폰트 복원 (overlap 방지) */
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
    }'''

new_css_part = '''    /* Streamlit 아이콘, Expander, Metric 및 파일 업로더 아이콘 폰트 복원 (overlap 완전 방지) */
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
    }'''

if old_css_part in content:
    content = content.replace(old_css_part, new_css_part)
    print('Updated CSS in app.py')
else:
    print('old_css_part not found!')

# Update Module 4 description string
old_mod4_desc = '''st.markdown("**`5. 배출구 가동시간` 엑셀 파일** 또는 **설비 가동현황 데이터**를 업로드하면, **282개 전체 배출시설의 가동시간, 가동분, 운영인자 6개, 전산량(누적 평일 기준)**이 주말/공휴일 및 요일별 규칙에 따라 자동 계산되어 **Sheet1** 및 **4-배출시설운영사항**에 작성됩니다.")'''

new_mod4_desc = '''st.markdown("'5. 배출구 가동시간' 엑셀 파일 또는 설비 가동현황 데이터를 업로드하면, 282개 전체 배출시설의 가동시간, 가동분, 운영인자 6개, 전산량(누적 평일 기준)이 주말/공휴일 및 요일별 규칙에 따라 자동 계산되어 Sheet1 및 4-배출시설운영사항에 작성됩니다.")'''

if old_mod4_desc in content:
    content = content.replace(old_mod4_desc, new_mod4_desc)
    print('Updated Mod 4 description')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Written back to app.py successfully.')
