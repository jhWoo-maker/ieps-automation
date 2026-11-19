import os
import subprocess
from PIL import Image

# 1. Paths
workspace_dir = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
png_path = os.path.join(workspace_dir, "seah_logo.png")
ico_path = os.path.join(workspace_dir, "seah_logo.ico")

# Get Desktop directory
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 2. Convert PNG to ICO with multiple sizes
if os.path.exists(png_path):
    img = Image.open(png_path)
    # Convert RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    print(f"Created ICO icon file at: {ico_path}")
else:
    print(f"Error: {png_path} not found.")

shortcut_name = "세아제강 창원공장 환경관리 자동화시스템.lnk"
shortcut_path = os.path.join(desktop_path, shortcut_name)
target_url = "http://172.17.82.193:8501"

# 3. Use PowerShell WScript.Shell to create shortcut
ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "explorer.exe"
$Shortcut.Arguments = "{target_url}"
$Shortcut.IconLocation = "{ico_path}, 0"
$Shortcut.Description = "세아제강 창원공장 환경관리 자동화시스템"
$Shortcut.Save()
print "Shortcut created."
"""

cmd = ["powershell", "-Command", ps_script]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("PowerShell output:", result.stdout)
if result.stderr:
    print("PowerShell error:", result.stderr)

if os.path.exists(shortcut_path):
    print(f"✅ Desktop shortcut successfully created at: {shortcut_path}")
else:
    print("❌ Failed to create desktop shortcut.")
