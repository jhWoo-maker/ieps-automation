import os

path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\app.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's fix Module 1 block indentation
def fix_module_block(text, header_str, end_anchor):
    pos = text.find(header_str)
    if pos == -1:
        return text
    end_pos = text.find(end_anchor, pos)
    if end_pos == -1:
        end_pos = len(text)
    
    sub_text = text[pos:end_pos]
    lines = sub_text.splitlines()
    fixed_lines = []
    for l in lines:
        if l.startswith("        ") and not l.startswith("            "):
            fixed_lines.append("    " + l[8:])
        elif l.startswith("            "):
            fixed_lines.append("        " + l[12:])
        elif l.startswith("                "):
            fixed_lines.append("            " + l[16:])
        elif l.startswith("                    "):
            fixed_lines.append("                " + l[20:])
        elif l.startswith("                        "):
            fixed_lines.append("                    " + l[24:])
        elif l.startswith("                            "):
            fixed_lines.append("                        " + l[28:])
        elif l.startswith("                                "):
            fixed_lines.append("                            " + l[32:])
        else:
            fixed_lines.append(l)
    return text[:pos] + "\n".join(fixed_lines) + text[end_pos:]

# Restore clean app.py first or write clean blocks directly
