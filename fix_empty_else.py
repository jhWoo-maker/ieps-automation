import os

path = r'C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == 'else:' and i + 1 < len(lines) and lines[i + 1].strip().startswith('# st.title'):
        new_lines.append(line)
        new_lines.append('        pass\n')
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed empty else blocks.")
