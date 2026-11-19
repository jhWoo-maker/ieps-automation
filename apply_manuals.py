import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Add MODULE_MANUALS and render_work_manual near line 160 (after render_validation_results)
manuals_code = '''
MODULE_MANUALS = {
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
}

def render_work_manual(item_num):
    steps = MODULE_MANUALS.get(item_num, [])
    if not steps:
        return
    items_html = "".join([f"<li>{step}</li>" for step in steps])
    st.markdown(
        f\'\'\'
        <div style="background-color: #F8F9FA; border-left: 4px solid #946CEE; padding: 12px 16px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-weight: bold; font-size: 15px; color: #111; margin-bottom: 6px;">📋 작업 매뉴얼</div>
            <ol style="margin: 0; padding-left: 20px; color: #333; line-height: 1.6; font-size: 14px;">
                {items_html}
            </ol>
        </div>
        \'\'\',
        unsafe_allow_html=True
    )
'''

if "MODULE_MANUALS =" not in text:
    target_anchor = 'def render_validation_results(item_num):'
    text = text.replace(target_anchor, manuals_code + "\n" + target_anchor)

# Now replace old description text in modules 1, 2, 4, 5, 6, 8, 9, 10, 11
# Module 1
t1 = 'st.markdown("대기 측정기록부 **PDF** 성적서를 업로드하면, **배출구별 현장기상/배출가스/측정농도 데이터**를 추출하여 **자가측정기록부 엑셀 파일**을 자동으로 생성 및 최신화합니다.")'
r1 = 'render_work_manual(1)'
text = text.replace(t1, r1)

# Module 2
t2 = 'st.markdown("수질 측정기록부 **PDF** 성적서를 업로드하면, **자가측정기록부 엑셀 파일**을 자동으로 생성 및 최신화합니다.")'
r2 = 'render_work_manual(2)'
text = text.replace(t2, r2)

# Module 4
t4 = 'st.markdown("**`5. 배출구 가동시간` 엑셀 파일** 또는 **설비 가동현황 데이터**를 업로드하면, **282개 전체 배출시설의 가동시간, 가동분, 운영인자 6개, 전력사용량(kWh, 누적 평일 기준)**이 주말/공휴일 및 요일별 규칙에 따라 자동 계산되어 **4-배출시설운영사항**에 작성됩니다.")'
r4 = 'render_work_manual(4)'
text = text.replace(t4, r4)

# Module 5
t5 = 'st.markdown("**`설비별 가동현황 조회_` 엑셀 파일**을 업로드하면, 배출구별(#A1~#A16, #W1, #W2) 가동시간이 자동으로 계산되고 작성됩니다.")'
r5 = 'render_work_manual(5)'
text = text.replace(t5, r5)

# Module 6
t6 = 'st.markdown("**`5. 배출구 가동시간` 엑셀 파일** 또는 **설비 가동현황 데이터**를 업로드하면, **30개 대기 방지시설의 가동시간, 가동분, 전력사용량(kWh, 누적 평일 기준), 운영인자 6개**가 주말/공휴일 및 요일별 규칙에 따라 자동 계산되어 **Sheet1** 및 **6-대기 방지시설 운영현황**에 작성됩니다.")'
r6 = 'render_work_manual(6)'
text = text.replace(t6, r6)

# Module 8
t8_anchor = 'st.title("🔥 8. 연료사용량")'
if "render_work_manual(8)" not in text:
    text = text.replace(t8_anchor, t8_anchor + "\n    render_work_manual(8)")

# Module 9
t9_anchor = 'st.title("🧪 9. 기타화학물질 사용량")'
if "render_work_manual(9)" not in text:
    text = text.replace(t9_anchor, t9_anchor + "\n    render_work_manual(9)")

# Module 10
t10_anchor = 'st.title("📦 10. 원부원료 사용량 및 제품 생산량")'
if "render_work_manual(10)" not in text:
    text = text.replace(t10_anchor, t10_anchor + "\n    render_work_manual(10)")

# Module generic (3, 7, 11 and others)
gen_anchor = 'st.title(f"{module_name}")'
gen_replace = 'st.title(f"{module_name}")\n    render_work_manual(curr_mod_num)'
if "render_work_manual(curr_mod_num)" not in text:
    text = text.replace(gen_anchor, gen_replace)

old_gen_desc = 'st.markdown(f"**{module_name}** 원본 자료(PDF/엑셀/CSV)를 업로드하여 엑셀 데이터를 최신화하는 모듈입니다.")'
text = text.replace(old_gen_desc, '')

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied manuals to app.py successfully!")
