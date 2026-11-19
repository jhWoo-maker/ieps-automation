import re

file_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

cleaned_lines = []
i = 0
n = len(lines)

while i < n:
    line = lines[i]
    if line.strip() == "else:":
        # check if next lines until next non-blank line are unindented or comment/if
        indent = len(line) - len(line.lstrip())
        next_has_body = False
        j = i + 1
        while j < n:
            next_line = lines[j]
            if next_line.strip() == "":
                j += 1
                continue
            next_indent = len(next_line) - len(next_line.lstrip())
            if next_indent > indent and not next_line.strip().startswith("#"):
                next_has_body = True
            break
        
        if not next_has_body:
            # Skip empty else block
            i = j
            continue
    cleaned_lines.append(line)
    i += 1

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

print("Empty else blocks cleaned up.")
