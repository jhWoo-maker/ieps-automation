import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Material Symbols font imports at top of <style>
imports_old = "@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');\n    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;600;700&display=swap');"

imports_new = """@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    @import url('https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');"""

if imports_old in content:
    content = content.replace(imports_old, imports_new)
    print("Added Material Symbols font imports.")

# 2. Add flexbox and icon CSS rules
css_addition = """
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
"""

# Insert css_addition before </style>
if "</style>" in content:
    content = content.replace("</style>", css_addition + "\n    </style>")
    print("Added flex layout and stIconMaterial CSS.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved app.py successfully.")
