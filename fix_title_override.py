import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix h1 and h1 children font-size override
old_h1_rule = """    /* 2. 메인 타이틀 (h1) 가독성 극대화 (32px Bold) */
    h1, [data-testid="stTitle"], div[data-testid="stMarkdownContainer"] h1, .stApp h1 {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #1B4D2E !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 12px !important;
        padding-top: 0px !important;
    }"""

new_h1_rule = """    /* 2. 메인 타이틀 (h1) 가독성 극대화 (34px Bold) - span 상속 방지 */
    h1, h1 *, [data-testid="stTitle"], [data-testid="stTitle"] *, div[data-testid="stMarkdownContainer"] h1, div[data-testid="stMarkdownContainer"] h1 * {
        font-size: 34px !important;
        font-weight: 800 !important;
        color: #1B4D2E !important;
        letter-spacing: -0.5px !important;
        line-height: 1.3 !important;
    }"""

content = content.replace(old_h1_rule, new_h1_rule)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Title font size 34px override fixed.")
