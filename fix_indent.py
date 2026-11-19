import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Unindent lines if they were inside with col2: but are now at top level after st.divider()
    if line.startswith("        if uploaded_air_pdf:") or \
       line.startswith("        if uploaded_pdf:") or \
       line.startswith("        if uploaded_fac_sub:") or \
       line.startswith("        if uploaded_prev_sub:") or \
       line.startswith("        if uploaded_file:"):
        # Fix indentation from 8 spaces to 4 spaces
        new_lines.append("    " + line.lstrip())
    else:
        new_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Indentation adjusted.")
