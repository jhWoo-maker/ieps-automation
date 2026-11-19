import os
import subprocess
from PIL import Image, ImageDraw

workspace_dir = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
ico_path = os.path.join(workspace_dir, "eco_green_icon.ico")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
shortcut_name = "세아제강 창원공장 환경관리 자동화시스템.lnk"
shortcut_path = os.path.join(desktop_path, shortcut_name)
target_url = "http://172.17.82.193:8501"

# Create a high-res 512x512 eco-friendly green icon
size = 512
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw rounded rectangle green background
bg_color = (46, 125, 50, 255) # #2E7D32
corner_radius = 110
draw.rounded_rectangle([(16, 16), (size - 16, size - 16)], radius=corner_radius, fill=bg_color)

# Draw crisp white leaf / eco sprout symbol
leaf_color = (255, 255, 255, 255)
stem_color = (255, 255, 255, 230)

# Main leaf polygon / curves
leaf_points = [
    (140, 360),
    (180, 240),
    (280, 140),
    (380, 120),
    (370, 220),
    (320, 310),
    (220, 370),
    (140, 360)
]
draw.polygon(leaf_points, fill=leaf_color)

# Leaf vein
draw.line([(140, 360), (320, 180)], fill=(46, 125, 50, 220), width=16)

# Second smaller leaf / sprout
leaf2_points = [
    (150, 350),
    (110, 270),
    (140, 200),
    (200, 220),
    (180, 300),
    (150, 350)
]
draw.polygon(leaf2_points, fill=(240, 248, 240, 240))

# Save multi-resolution ICO file
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save(ico_path, format='ICO', sizes=icon_sizes)
print(f"Created custom high-res green eco icon at: {ico_path}")

# Update Desktop shortcut
ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "explorer.exe"
$Shortcut.Arguments = "{target_url}"
$Shortcut.IconLocation = "{ico_path}, 0"
$Shortcut.Description = "세아제강 창원공장 환경관리 자동화시스템"
$Shortcut.Save()
"""

cmd = ["powershell", "-Command", ps_script]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("PowerShell output:", result.stdout)

if os.path.exists(shortcut_path):
    print(f"✅ Desktop shortcut updated with custom green eco icon successfully at: {shortcut_path}")
else:
    print("❌ Failed to update desktop shortcut.")
