import sys

with open("app.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Fix top imports
old_top_import = """import fuel_consumption_processor
import facility_status_processor
import air_prevention_processor
import chemicals_processor

importlib.reload(fuel_consumption_processor)
importlib.reload(facility_status_processor)
importlib.reload(air_prevention_processor)
importlib.reload(chemicals_processor)

from fuel_consumption_processor import generate_fuel_consumption_excel
from facility_status_processor import process_facility_status
from air_prevention_processor import process_air_prevention"""

new_top_import = """import fuel_consumption_processor
import facility_status_processor
import air_prevention_processor
import chemicals_processor
import raw_materials_products_processor

importlib.reload(fuel_consumption_processor)
importlib.reload(facility_status_processor)
importlib.reload(air_prevention_processor)
importlib.reload(chemicals_processor)
importlib.reload(raw_materials_products_processor)

from fuel_consumption_processor import generate_fuel_consumption_excel
from facility_status_processor import process_facility_status
from air_prevention_processor import process_air_prevention
from chemicals_processor import process_chemicals_excel
from raw_materials_products_processor import parse_datagrid_excel, generate_raw_materials_excel, generate_products_excel"""

code = code.replace(old_top_import, new_top_import)

# 2. Fix sidebar radio options
old_sidebar_radio = """menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "1. 대기-자가측정기록부 (자동화 구동 중)",
        "2. 수질-자가측정기록부 (자동화 구동 중)",
        "3. 기타-자가측정기록부",
        "4. 배출시설 운영현황 (자동화 구동 중)",
        "5. 배출구 가동시간 (자동화 구동 중)",
        "6. 대기 방지시설 운영현황 (자동화 구동 중)",
        "7. 폐수처리시설(수질방지시설)",
        "8. 연료사용량 (자동화 구동 중)",
        "10. 기타화학물질 사용량 (자동화 구동 중)",
        "11. 원부원료 사용량 및 제품 생산량 (자동화 구동 중)",
        "12. 에너지 사용량"
    ],
    index=0
)"""

new_sidebar_radio = """menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "1. 대기-자가측정기록부 (자동화 구동 중)",
        "2. 수질-자가측정기록부 (자동화 구동 중)",
        "3. 기타-자가측정기록부",
        "4. 배출시설 운영현황 (자동화 구동 중)",
        "5. 배출구 가동시간 (자동화 구동 중)",
        "6. 대기 방지시설 운영현황 (자동화 구동 중)",
        "7. 폐수처리시설(수질방지시설)",
        "8. 연료사용량 (자동화 구동 중)",
        "10. 기타화학물질 사용량 (자동화 구동 중)",
        "11. 원부원료 사용량 및 제품 생산량 (자동화 구동 중)",
        "12. 에너지 사용량"
    ],
    index=0
)"""

# Also check if old menu options with 9 were still present
old_sidebar_radio_with_9 = """menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "1. 대기-자가측정기록부 (자동화 구동 중)",
        "2. 수질-자가측정기록부 (자동화 구동 중)",
        "3. 기타-자가측정기록부",
        "4. 배출시설 운영현황 (자동화 구동 중)",
        "5. 배출구 가동시간 (자동화 구동 중)",
        "6. 대기 방지시설 운영현황 (자동화 구동 중)",
        "7. 폐수처리시설(수질방지시설)",
        "8. 연료사용량 (자동화 구동 중)",
        "9. 원부원료 사용량",
        "10. 기타화학물질 사용량 (자동화 구동 중)",
        "11. 에너지 사용량",
        "12. 제품 생산량"
    ],
    index=0
)"""

code = code.replace(old_sidebar_radio_with_9, new_sidebar_radio)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Applied fixes to app.py successfully!")
