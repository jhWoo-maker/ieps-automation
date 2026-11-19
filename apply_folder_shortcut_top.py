import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace menu assignment to render top folder shortcut on the right
old_menu_block = '''menu = RAW_MENU_ITEMS[st.session_state["menu_index"]][1]'''

new_menu_block = '''menu = RAW_MENU_ITEMS[st.session_state["menu_index"]][1]

# 우측 상단 폴더 바로가기 헤더 배치
hdr_col1, hdr_col2 = st.columns([2.2, 1.8])
with hdr_col2:
    render_top_folder_shortcut()
'''

if old_menu_block in content:
    content = content.replace(old_menu_block, new_menu_block)
    print("Placed render_top_folder_shortcut in top header col2.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved app.py.")
