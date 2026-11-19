import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the folder path constant and function
folder_code = '''
# -----------------------------------------------------------------------------
# 공유 드라이브 바로가기 폴더 설정
# -----------------------------------------------------------------------------
SHARED_FOLDER_PATH = r"G:\\공유 드라이브\\창원공장 안전환경파트\\손영준\\이전파일\\03. 환경\\0. 통합환경관리\\7. 통합환경관리 사후관리계획 입력자료\\이전제출"

def render_top_folder_shortcut():
    st.markdown(
        f\'\'\'
        <div style="background-color: #FFFFFF; border: 1px solid #C8E6C9; border-radius: 10px; padding: 10px 14px; box-shadow: 0 2px 6px rgba(46,125,50,0.08); margin-bottom: 12px;">
            <div style="font-size: 13.5px; font-weight: 700; color: #1B4D2E; display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                📁 <span>통합환경 사후관리계획 이전제출 폴더</span>
            </div>
            <div style="font-size: 11px; color: #444; word-break: break-all; background-color: #F4F9F5; padding: 4px 8px; border-radius: 4px; border: 1px solid #E0EFE3; margin-bottom: 6px;">
                <code>G:\\공유 드라이브\\창원공장 안전환경파트\\손영준\\이전파일\\03. 환경\\0. 통합환경관리\\7. 통합환경관리 사후관리계획 입력자료\\이전제출</code>
            </div>
        </div>
        \'\'\',
        unsafe_allow_html=True
    )
    if st.button("📂 탐색기로 이전제출 폴더 열기", key="btn_open_top_folder", type="secondary", use_container_width=True):
        try:
            import subprocess
            if os.path.exists(SHARED_FOLDER_PATH):
                subprocess.Popen(["explorer.exe", SHARED_FOLDER_PATH])
                st.toast("📂 '이전제출' 폴더가 Windows 탐색기로 열렸습니다!")
            else:
                st.error(f"❌ 지정된 폴더 경로를 찾을 수 없습니다:\\n{SHARED_FOLDER_PATH}")
        except Exception as e:
            st.error(f"❌ 폴더 열기 오류: {e}")
'''

# Insert folder_code before menu selection
if "# Update selected menu index" in content:
    content = content.replace("# Update selected menu index", folder_code + "\n\n# Update selected menu index")
    print("Inserted render_top_folder_shortcut definition.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved app.py.")
