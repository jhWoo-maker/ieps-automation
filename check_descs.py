import os
import re

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Check old descriptions
desc_pattern = re.compile(r'st\.markdown\(["\'](\*\*`?[^"\']+|대기 측정기록부|수질 측정기록부|일자별|가스 저장품|MES|전기 사용량)[^"\']*["\']\)')
matches = desc_pattern.findall(text)
print("Found description matches:", len(matches))
for m in matches:
    print(" -", m[:80])
