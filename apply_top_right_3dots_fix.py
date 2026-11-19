import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update render_top_folder_shortcut function
old_fn = '''def render_top_folder_shortcut():
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
                st.error(f"❌ 지정된 폴더 경로를 찾을 수 없습니다:\\n{{SHARED_FOLDER_PATH}}")
        except Exception as e:
            st.error(f"❌ 폴더 열기 오류: {{e}}")'''

new_fn = '''def render_top_folder_shortcut():
    # 고정 위치 마커 및 우측 상단 3점 메뉴 바로 왼쪽 팝오버/버튼 생성
    st.markdown('<span id="top_right_folder_marker"></span>', unsafe_allow_html=True)
    
    with st.popover("📁 이전제출 폴더 바로가기", use_container_width=False):
        st.markdown(
            f\'\'\'
            <div style="padding: 4px;">
                <div style="font-size: 14px; font-weight: 700; color: #1B4D2E; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
                    📁 <span>통합환경 사후관리계획 이전제출 폴더</span>
                </div>
                <div style="font-size: 11.5px; color: #333; word-break: break-all; background-color: #F4F9F5; padding: 8px; border-radius: 6px; border: 1px solid #D2E4D6; margin-bottom: 10px;">
                    <code>G:\\공유 드라이브\\창원공장 안전환경파트\\손영준\\이전파일\\03. 환경\\0. 통합환경관리\\7. 통합환경관리 사후관리계획 입력자료\\이전제출</code>
                </div>
            </div>
            \'\'\',
            unsafe_allow_html=True
        )
        if st.button("📂 Windows 탐색기로 폴더 열기", key="btn_open_top_folder", type="primary", use_container_width=True):
            try:
                import subprocess
                if os.path.exists(SHARED_FOLDER_PATH):
                    subprocess.Popen(["explorer.exe", SHARED_FOLDER_PATH])
                    st.toast("📂 '이전제출' 폴더가 Windows 탐색기로 열렸습니다!")
                else:
                    st.error(f"❌ 지정된 폴더 경로를 찾을 수 없습니다:\\n{SHARED_FOLDER_PATH}")
            except Exception as e:
                st.error(f"❌ 폴더 열기 오류: {e}")'''

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("Updated render_top_folder_shortcut to popover with marker.")
else:
    print("old_fn not found!")

# Add CSS positioning for top_right_folder_marker in style block
css_rule = '''
    /* 우측 상단 3점 메뉴 바로 왼쪽에 폴더 바로가기 버튼 배치 */
    div[data-testid="stElementContainer"]:has(#top_right_folder_marker),
    div[data-testid="stPopover"]:has(#top_right_folder_marker) {
        position: fixed !important;
        top: 10px !important;
        right: 60px !important;
        z-index: 999999 !important;
        width: auto !important;
    }
'''

if "</style>" in content:
    content = content.replace("</style>", css_rule + "\n    </style>")
    print("Added top_right_folder_marker CSS rule.")

# Remove top header columns if we want title to take full width and button floating at top right
old_hdr_split = '''# 우측 상단 폴더 바로가기 및 타이틀 나란히 배치
hdr_col1, hdr_col2 = st.columns([2.2, 1.8])
with hdr_col1:
    st.title(menu)
with hdr_col2:
    render_top_folder_shortcut()'''

new_hdr_split = '''# 타이틀 출력 및 우측 상단 3점 메뉴 옆 폴더 바로가기 고정 배치
st.title(menu)
render_top_folder_shortcut()'''

if old_hdr_split in content:
    content = content.replace(old_hdr_split, new_hdr_split)
    print("Updated header placement.")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved app.py.")
