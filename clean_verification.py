import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update MODULE_MANUALS to remove "검증하세요"
old_manuals = """MODULE_MANUALS = {
    1: [
        "대기 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    2: [
        "수질 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    3: [
        "기타 자가측정기록부 PDF 파일을 업로드하세요(소음·진동, 비점오염, 악취 등)",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    4: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    5: [
        "설비별 가동현황 엑셀을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    6: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    7: [
        "원하시는 파일을 업로드 하세요"
    ],
    8: [
        "일자 별 연료사용량을 입력하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    9: [
        "가스 저장품 점검표 엑셀을 업로드 하세요",
        "고분자응집제, 소석회, 메탄올을 수기 입력하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    10: [
        "MES 창원공장 종합수율 조회 엑셀 파일을 추출 후 업로드 하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ],
    11: [
        "전기 사용량을 입력하세요",
        "에너지 사용량을 입력하세요",
        "엑셀을 추출하세요",
        "검증하세요"
    ]
}"""

new_manuals = """MODULE_MANUALS = {
    1: [
        "대기 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    2: [
        "수질 자가측정기록부 PDF 파일을 업로드하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    3: [
        "기타 자가측정기록부 PDF 파일을 업로드하세요(소음·진동, 비점오염, 악취 등)",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    4: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    5: [
        "설비별 가동현황 엑셀을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    6: [
        "배출구 가동시간 파일을 먼저 완성하세요",
        "배출구 가동시간 파일을 업로드 하세요",
        "IEPS에 첨부 할 템플릿 파일을 등록하세요",
        "엑셀을 추출하세요"
    ],
    7: [
        "원하시는 파일을 업로드 하세요"
    ],
    8: [
        "일자 별 연료사용량을 입력하세요",
        "엑셀을 추출하세요"
    ],
    9: [
        "가스 저장품 점검표 엑셀을 업로드 하세요",
        "고분자응집제, 소석회, 메탄올을 수기 입력하세요",
        "엑셀을 추출하세요"
    ],
    10: [
        "MES 창원공장 종합수율 조회 엑셀 파일을 추출 후 업로드 하세요",
        "엑셀을 추출하세요"
    ],
    11: [
        "전기 사용량을 입력하세요",
        "에너지 사용량을 입력하세요",
        "엑셀을 추출하세요"
    ]
}"""

content = content.replace(old_manuals, new_manuals)

# 2. Make render_validation_results do nothing
old_val_fn = """def render_validation_results(item_num):
    status = st.session_state["module_status"].get(item_num, "pending")
    errors = st.session_state["module_errors"].get(item_num, [])
    
    if status == "normal":
        st.success("✅ **[ 정상 ]** 작성지침 및 수식/범위 오류 검증을 통과하였습니다.")
    elif status == "error":
        st.error(f"⚠️ **[ 오류 ]** 작성지침 검증 결과 **{len(errors)}개**의 오류가 발견되었습니다:")
        for err in errors:
            st.markdown(f"- ❌ **{err}**")
    else:
        st.info("ℹ️ **[ 검증 전 ]** 파일 업로드 또는 생성 후 하단의 **'🔍 데이터 검증하기'** 버튼을 누르면 오류 검증이 수행됩니다.")"""

new_val_fn = """def render_validation_results(item_num):
    pass"""

content = content.replace(old_val_fn, new_val_fn)

# 3. get_badge_label return pure title
old_badge_label = """def get_badge_label(item_num, title):
    status = st.session_state["module_status"].get(item_num, "pending")
    if status == "normal":
        return f"{title} :green-background[ 정상 ]"
    elif status == "error":
        return f"{title} :orange-background[ 오류 ]"
    else:
        return f"{title} :gray-background[ 검증 전 ]\""""

new_badge_label = """def get_badge_label(item_num, title):
    return title"""

content = content.replace(old_badge_label, new_badge_label)

# 4. Remove sidebar validation button
old_sidebar_btn = """st.sidebar.divider()

if st.sidebar.button("🔍 데이터 검증하기", key="sidebar_validate_btn", use_container_width=True):
    for mod_i in range(1, 12):
        fpath = st.session_state["module_files"].get(mod_i)
        if fpath and os.path.exists(fpath):
            is_val, errs = validate_excel_file(mod_i, fpath)
            if is_val:
                st.session_state["module_status"][mod_i] = "normal"
                st.session_state["module_errors"][mod_i] = []
            else:
                st.session_state["module_status"][mod_i] = "error"
                st.session_state["module_errors"][mod_i] = errs
    st.rerun()"""

content = content.replace(old_sidebar_btn, "")

# 5. Remove all expanders starting with 'with st.expander("🔍 작성완료 엑셀 파일 직접 업로드 및 검증'
# Let's use regex to remove these blocks
pattern = r'^\s*with st\.expander\("🔍 작성완료 엑셀 파일 직접 업로드 및 검증.*?\n(?=\s*render_work_manual|\s*st\.divider|\s*col1, col2|\s*st\.subheader|\s*if|\s*#)'
# Let's be careful with regex multiline matching
# Alternatively, line-by-line parsing to remove expander blocks

lines = content.split('\n')
new_lines = []
skip = False
skip_indent = 0

for line in lines:
    if 'with st.expander("🔍 작성완료 엑셀 파일 직접 업로드 및 검증' in line:
        skip = True
        skip_indent = len(line) - len(line.lstrip())
        continue
    if skip:
        if line.strip() == '':
            continue
        current_indent = len(line) - len(line.lstrip())
        if current_indent > skip_indent:
            continue
        else:
            skip = False
    new_lines.append(line)

final_content = '\n'.join(new_lines)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_content)

print("Finished cleaning verification logic.")
