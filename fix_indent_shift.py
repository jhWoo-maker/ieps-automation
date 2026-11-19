import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
fixed_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith("if uploaded_") or (line.strip().startswith("if ") and ("uploaded_" in line or "uploaded_file" in line)):
        if line.startswith("    if "):
            fixed_lines.append(line)
            i += 1
            # Next lines until else: or end of module block should be shifted left by 4 spaces
            while i < len(lines):
                cur = lines[i]
                if cur.startswith("# ------------") or cur.startswith("elif ") or (cur.startswith("    if ") and "in menu:" in cur):
                    break
                if cur.startswith("        "): # 8 or more spaces
                    fixed_lines.append(cur[4:])
                elif cur.startswith("    else:"):
                    fixed_lines.append("    else:")
                else:
                    fixed_lines.append(cur)
                i += 1
            continue
    fixed_lines.append(line)
    i += 1

with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(fixed_lines))

print("Indentation shift complete.")
