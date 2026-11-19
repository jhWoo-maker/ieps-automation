import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect indentation around line 360-460, 480-580, etc.
lines = text.splitlines()

fixed_lines = []
in_unindented_if = False
unindent_base = 0

for line in lines:
    if line.strip().startswith("if uploaded_air_pdf:") or \
       line.strip().startswith("if uploaded_pdf:") or \
       line.strip().startswith("if uploaded_fac_sub:") or \
       line.strip().startswith("if uploaded_prev_sub:") or \
       line.strip().startswith("if uploaded_file:"):
        if line.startswith("        if "):
            in_unindented_if = True
            unindent_base = 4
            fixed_lines.append("    " + line.strip())
            continue
    
    if in_unindented_if:
        if line.startswith("# --------------------------------") or line.startswith("elif ") or line.startswith("else:"):
            in_unindented_if = False
            fixed_lines.append(line)
        else:
            if line.startswith("        "):
                fixed_lines.append(line[4:])
            else:
                fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(fixed_lines))

print("Block unindenting applied.")
