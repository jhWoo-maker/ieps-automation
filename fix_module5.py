import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace Module 5 completely with clean 2-column layout and bottom full-width section
m5_old_start = text.find('elif "5. 배출구" in menu:')
m5_old_end = text.find('elif "6. 대기 방지시설" in menu:')

m5_clean_code = '''elif "5. 배출구" in menu:
    st.title("⏱️ 5. 배출구 가동시간")
    render_validation_results(5)
    with st.expander("🔍 작성완료 엑셀 파일 직접 업로드 및 검증 (오류 검토용)", expanded=False):
        uploaded_check_5 = st.file_uploader("검증할 '5. 배출구 가동시간' 엑셀 파일 선택", type=["xlsx", "xlsm"], key="check_file_5")
        if uploaded_check_5:
            check_path_5 = os.path.join(BASE_DIR, f"temp_check_5_{uploaded_check_5.name}")
            with open(check_path_5, "wb") as f:
                f.write(uploaded_check_5.getbuffer())
            st.session_state["module_files"][5] = check_path_5
            is_v5, errs5 = validate_excel_file(5, check_path_5)
            st.session_state["module_status"][5] = "normal" if is_v5 else "error"
            st.session_state["module_errors"][5] = [] if is_v5 else errs5
            st.rerun()
    render_work_manual(5)
    
    st.divider()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 파일 업로드")
        uploaded_sub = st.file_uploader("다운로드받으신 '설비별 가동현황' 엑셀(.xlsx)을 업로드하세요", type=["xlsx", "xls"], key="sub_excel")
        
    with col2:
        st.subheader("2️⃣ 엑셀 템플릿 선택")
        use_default_outlet = st.checkbox("기본 배출구 가동시간 템플릿 사용", value=True, key="outlet_tpl_check")
        
        uploaded_outlet_template = None
        if not use_default_outlet:
            uploaded_outlet_template = st.file_uploader("기준 배출구 가동시간 템플릿(.xlsx) 업로드", type=["xlsx"], key="outlet_tpl_file")

    st.divider()
    st.subheader("3️⃣ 배출구 가동시간 결과 확인 및 수동 수정")
    
    if uploaded_sub:
        temp_sub_path = "temp_sub_excel.xlsx"
        with open(temp_sub_path, "wb") as f:
            f.write(uploaded_sub.getbuffer())
            
        try:
            df_sub, df_outlet = process_outlet_operating_hours(temp_sub_path)
            st.session_state["module_status"][5] = "normal"
            st.success("✅ 설비 가동현황 데이터 처리 완료 및 배출구 가동시간 자동 매핑 완료!")
            
            st.info("💡 주말/공휴일 가동시간(#A1, #A2, #W1, #W2) 또는 #A15 등 변경이 필요한 경우 **표에서 숫자를 직접 클릭하여 수정**할 수 있습니다.")
            
            edited_df_outlet = st.data_editor(
                df_outlet,
                num_rows="fixed",
                use_container_width=True,
                height=450,
                column_config={
                    "No": st.column_config.NumberColumn("No", disabled=True),
                    "가동일자": st.column_config.NumberColumn("가동일자", disabled=True, format="%d"),
                    "배출구정보": st.column_config.TextColumn("배출구정보", disabled=True),
                    "시간": st.column_config.NumberColumn("가동시간 (시간)", min_value=0, max_value=24, step=1),
                    "분": st.column_config.NumberColumn("가동시간 (분)", min_value=0, max_value=59, step=1),
                    "비고": st.column_config.TextColumn("비고")
                }
            )
            
            st.divider()
            st.subheader("4️⃣ 최종 엑셀 파일 저장 및 다운로드")
            
            first_date = str(edited_df_outlet["가동일자"].iloc[0])
            month_str = int(first_date[4:6]) if len(first_date) >= 6 else 9
            out_excel_name = f"5.배출구_가동시간(26년_{month_str}월).xlsx"
            
            if st.button("🚀 '5. 배출구 가동시간' 엑셀 완성본 생성", type="primary", use_container_width=True):
                template_path = DEFAULT_OUTLET_TEMPLATE if use_default_outlet or not uploaded_outlet_template else "temp_outlet_tpl.xlsx"
                if uploaded_outlet_template and not use_default_outlet:
                    with open(template_path, "wb") as f:
                        f.write(uploaded_outlet_template.getbuffer())
                        
                temp_out_path = f"output_{out_excel_name}"
                save_outlet_excel_file(edited_df_outlet, template_path, temp_out_path)
                
                st.session_state["module_files"][5] = os.path.abspath(temp_out_path)
                st.balloons()
                st.success(f"🎉 '{out_excel_name}' 엑셀 파일 생성이 완료되었습니다!")
                
                with open(temp_out_path, "rb") as f:
                    file_bytes = f.read()
                    
                st.download_button(
                    label=f"📥 {out_excel_name} 다운로드",
                    data=file_bytes,
                    file_name=out_excel_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
        except Exception as e:
            st.session_state["module_status"][5] = "error"
            st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
    else:
        st.info("👈 위에서 '설비별 가동현황 조회_' 엑셀 파일(.xlsx)을 업로드하면 자동으로 가동시간이 계산됩니다.")

# -----------------------------------------------------------------------------
# 6. 대기 방지시설 운영현황 모듈 (자동화 완전 구동 중)
# -----------------------------------------------------------------------------
'''

text = text[:m5_old_start] + m5_clean_code + text[m5_old_end + len('elif "6. 대기 방지시설" in menu:\n'):]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Module 5 cleanly replaced.")
