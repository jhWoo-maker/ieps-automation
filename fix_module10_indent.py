import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

m10_old_start = text.find('elif "원부원료 사용량 및 제품 생산량" in menu')
m10_old_end = text.find('# -----------------------------------------------------------------------------\n# 나머지 모듈')

m10_clean_code = '''elif "원부원료 사용량 및 제품 생산량" in menu or "원부원료" in menu or "제품 생산량" in menu:
    st.title("📦 10. 원부원료 사용량 및 제품 생산량")
    render_validation_results(10)
    with st.expander("🔍 작성완료 엑셀 파일 직접 업로드 및 검증 (오류 검토용)", expanded=False):
        uploaded_check_10 = st.file_uploader("검증할 '10. 원부원료 및 제품생산량' 엑셀 파일 선택", type=["xlsx", "xlsm"], key="check_file_10")
        if uploaded_check_10:
            check_path_10 = os.path.join(BASE_DIR, f"temp_check_10_{uploaded_check_10.name}")
            with open(check_path_10, "wb") as f:
                f.write(uploaded_check_10.getbuffer())
            st.session_state["module_files"][10] = check_path_10
            is_v10, errs10 = validate_excel_file(10, check_path_10)
            st.session_state["module_status"][10] = "normal" if is_v10 else "error"
            st.session_state["module_errors"][10] = [] if is_v10 else errs10
            st.rerun()
    render_work_manual(10)
    
    st.divider()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("1️⃣ 월간 적용 일자 선택 & 파일 업로드")
        
        sel_month11 = st.selectbox("📅 적용 월 선택 (기본 10월)", options=list(range(1, 13)), index=9, key="sel_m11")
        sel_year11 = 2026
        target_ym11 = f"{sel_year11}{sel_month11:02d}"
        
        uploaded_datagrid = st.file_uploader("DataGrid 엑셀 파일(.xlsx) 업로드", type=["xlsx", "xls"], key="dg_excel_file")
        st.caption("※ DataGrid 파일 내 '조관수율-투입량(kg)'과 '조관수율-양품량(kg)'을 자동으로 추출하여 1000으로 나누어 '톤(ton)' 단위로 환산합니다.")

    with col2:
        st.subheader("2️⃣ 템플릿 파일 선택")
        use_default11 = st.checkbox("기본 9번(원부원료) 및 12번(제품생산량) 템플릿 사용", value=True, key="tpl11_check")
        
        uploaded_raw_template, uploaded_products_template = None, None
        if not use_default11:
            uploaded_raw_template = st.file_uploader("9번 원부원료 템플릿(.xlsx) 업로드", type=["xlsx"], key="raw_tpl_file")
            uploaded_products_template = st.file_uploader("12번 제품생산량 템플릿(.xlsx) 업로드", type=["xlsx"], key="products_tpl_file")

    st.divider()
    
    if uploaded_datagrid:
        try:
            raw_mats_parsed, products_parsed = parse_datagrid_excel(uploaded_datagrid)
            st.session_state["module_status"][10] = "normal"
            st.success("✅ DataGrid 엑셀 파싱 및 톤(ton) 환산 완료!")
        except Exception as e:
            st.session_state["module_status"][10] = "error"
            st.error(f"❌ DataGrid 파일 처리 중 오류 발생: {e}")
            raw_mats_parsed, products_parsed = None, None
    else:
        sample_dg_path = r"C:\\Users\\user\\.gemini\\antigravity\\brain\\ad521db9-e8bb-4b72-8409-212c96a01c34\\.user_uploaded\\media_1794890006306_1b57896b.xlsx"
        if os.path.exists(sample_dg_path):
            raw_mats_parsed, products_parsed = parse_datagrid_excel(sample_dg_path)
            st.info("💡 DataGrid 엑셀 파일을 업로드하면 수치가 자동 갱신됩니다. (현재 최근 파일 수치 연동 중)")
        else:
            raw_mats_parsed, products_parsed = None, None

    if raw_mats_parsed and products_parsed:
        st.subheader("3️⃣ 원부원료 및 제품 생산량 데이터 확인 및 수동 수정")
        
        tab1, tab2 = st.tabs(["📊 9. 원부원료 사용량 (7개 공정)", "🏭 12. 제품 생산량 (2개 제품)"])
        
        with tab1:
            st.markdown("##### 📌 원부원료 사용량 (조관수율 투입량 → 톤 환산)")
            df_rm_data = []
            for code, d in raw_mats_parsed.items():
                df_rm_data.append({
                    "공정코드": d["code"],
                    "공정명": d["name"],
                    "원료명": d["material"],
                    "사용량 (톤)": d["amount"],
                    "단위": "톤 (12)"
                })
            df_rm = pd.DataFrame(df_rm_data)
            edited_rm = st.data_editor(
                df_rm,
                column_config={
                    "공정코드": st.column_config.TextColumn(disabled=True),
                    "공정명": st.column_config.TextColumn(disabled=True),
                    "원료명": st.column_config.TextColumn(disabled=True),
                    "사용량 (톤)": st.column_config.NumberColumn(format="%.3f"),
                    "단위": st.column_config.TextColumn(disabled=True)
                },
                disabled=["공정코드", "공정명", "원료명", "단위"],
                use_container_width=True,
                hide_index=True,
                key="ed_rm_tab"
            )
            
        with tab2:
            st.markdown("##### 📌 제품 생산량 (조관수율 양품량 → 톤 환산)")
            df_pr_data = []
            for code, d in products_parsed.items():
                df_pr_data.append({
                    "제품코드": d["code"],
                    "제품명": d["name"].replace("\\n", " "),
                    "제품구분": d["category"],
                    "생산량 (톤)": d["amount"],
                    "단위": "톤 (12)"
                })
            df_pr = pd.DataFrame(df_pr_data)
            edited_pr = st.data_editor(
                df_pr,
                column_config={
                    "제품코드": st.column_config.TextColumn(disabled=True),
                    "제품명": st.column_config.TextColumn(disabled=True),
                    "제품구분": st.column_config.TextColumn(disabled=True),
                    "생산량 (톤)": st.column_config.NumberColumn(format="%.3f"),
                    "단위": st.column_config.TextColumn(disabled=True)
                },
                disabled=["제품코드", "제품명", "제품구분", "단위"],
                use_container_width=True,
                hide_index=True,
                key="ed_pr_tab"
            )

        st.divider()
        st.subheader("4️⃣ 최종 엑셀 파일 추출")
        
        btn_col1, btn_col2 = st.columns([1, 1])
        
        final_rm_dict = {}
        for _, row in edited_rm.iterrows():
            c = row["공정코드"]
            final_rm_dict[c] = {"amount": float(row["사용량 (톤)"])}

        final_pr_dict = {}
        for _, row in edited_pr.iterrows():
            c = row["제품코드"]
            final_pr_dict[c] = {"amount": float(row["생산량 (톤)"])}

        with btn_col1:
            fn9 = f"9.원부원료_사용량({sel_month11}월).xlsx"
            out9_path = os.path.join(BASE_DIR, f"temp_{fn9}")
            tpl9_path = DEFAULT_RAW_MATERIALS_TEMPLATE if use_default11 or not uploaded_raw_template else "temp_raw_tpl.xlsx"
            if uploaded_raw_template and not use_default11:
                with open(tpl9_path, "wb") as f:
                    f.write(uploaded_raw_template.getbuffer())
                    
            generate_raw_materials_excel(target_ym11, final_rm_dict, tpl9_path, out9_path)
            
            with open(out9_path, "rb") as f:
                st.download_button(
                    label=f"📥 '{fn9}' 다운로드",
                    data=f.read(),
                    file_name=fn9,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )

        with btn_col2:
            fn12 = f"12.제품_생산량({sel_month11}월).xlsx"
            out12_path = os.path.join(BASE_DIR, f"temp_{fn12}")
            tpl12_path = DEFAULT_PRODUCTS_TEMPLATE if use_default11 or not uploaded_products_template else "temp_prod_tpl.xlsx"
            if uploaded_products_template and not use_default11:
                with open(tpl12_path, "wb") as f:
                    f.write(uploaded_products_template.getbuffer())
                    
            generate_products_excel(target_ym11, final_pr_dict, tpl12_path, out12_path)
            
            with open(out12_path, "rb") as f:
                st.download_button(
                    label=f"📥 '{fn12}' 다운로드",
                    data=f.read(),
                    file_name=fn12,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
'''

text = text[:m10_old_start] + m10_clean_code + text[m10_old_end:]

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Module 10 cleanly updated.")
