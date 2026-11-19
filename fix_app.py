import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

target = '    st.divider()\n    st.session_state["module_status"][8] = "normal"'
target_crlf = '    st.divider()\r\n    st.session_state["module_status"][8] = "normal"'

text = text.replace(target_crlf, '    st.divider()').replace(target, '    st.divider()')

# Now add module 8 status in the right place:
fuel_target = 'elif "연료사용량" in menu:\n    st.title("🔥 8. 연료사용량")'
fuel_replacement = 'elif "연료사용량" in menu:\n    st.session_state["module_status"][8] = "normal"\n    st.title("🔥 8. 연료사용량")'

text = text.replace(fuel_target, fuel_replacement)

# Module 9 (기타화학물질)
chem_success = 'st.success(f"✅ 가스 점검표 파싱 완료! ({target_sheet_selected or \'기본\'} 시트)")'
chem_success_replacement = 'st.session_state["module_status"][9] = "normal"\n                st.success(f"✅ 가스 점검표 파싱 완료! ({target_sheet_selected or \'기본\'} 시트)")'
text = text.replace(chem_success, chem_success_replacement)

chem_err = 'st.error(f"❌ 가스 점검표 분석 중 오류: {ex}")'
chem_err_replacement = 'st.session_state["module_status"][9] = "error"\n                st.error(f"❌ 가스 점검표 분석 중 오류: {ex}")'
text = text.replace(chem_err, chem_err_replacement)

# Module 10 (원부원료)
dg_success = 'st.success("✅ DataGrid 엑셀 파싱 및 톤(ton) 환산 완료!")'
dg_success_replacement = 'st.session_state["module_status"][10] = "normal"\n            st.success("✅ DataGrid 엑셀 파싱 및 톤(ton) 환산 완료!")'
text = text.replace(dg_success, dg_success_replacement)

dg_err = 'st.error(f"❌ DataGrid 파일 처리 중 오류 발생: {e}")'
dg_err_replacement = 'st.session_state["module_status"][10] = "error"\n            st.error(f"❌ DataGrid 파일 처리 중 오류 발생: {e}")'
text = text.replace(dg_err, dg_err_replacement)

# Generic else handler for modules 3, 7, 11
generic_target = 'else:\n    module_name = menu\n    st.title(f"{module_name}")'
generic_replacement = '''else:
    module_name = menu
    st.title(f"{module_name}")
    for num, title in RAW_MENU_ITEMS:
        if title in module_name:
            if uploaded_file:
                st.session_state["module_status"][num] = "normal"
            break'''
text = text.replace(generic_target, generic_replacement)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated app.py with all module status updates cleanly!")
