import os
import subprocess

startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
desktop_dir = os.path.expandvars(r"%USERPROFILE%\Desktop")

vbs_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\run_background.vbs"
open_py_path = r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\open_active_url.py"

ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell

# Startup Shortcut
$StartupShortcut = $WshShell.CreateShortcut("{os.path.join(startup_dir, 'IEPS_Server.lnk')}")
$StartupShortcut.TargetPath = "wscript.exe"
$StartupShortcut.Arguments = '"{vbs_path}"'
$StartupShortcut.WorkingDirectory = "C:\\Users\\user\\.gemini\\antigravity\\scratch\\water_quality_automation"
$StartupShortcut.Save()

# Desktop Server Shortcut
$DesktopShortcut = $WshShell.CreateShortcut("{os.path.join(desktop_dir, 'IEPS_서버_실행.lnk')}")
$DesktopShortcut.TargetPath = "wscript.exe"
$DesktopShortcut.Arguments = '"{vbs_path}"'
$DesktopShortcut.WorkingDirectory = "C:\\Users\\user\\.gemini\\antigravity\\scratch\\water_quality_automation"
$DesktopShortcut.Save()

# Desktop Auto-Open Shortcut
$AutoOpenShortcut = $WshShell.CreateShortcut("{os.path.join(desktop_dir, 'IEPS_웹사이트_접속.lnk')}")
$AutoOpenShortcut.TargetPath = "pythonw.exe"
$AutoOpenShortcut.Arguments = '"{open_py_path}"'
$AutoOpenShortcut.WorkingDirectory = "C:\\Users\\user\\.gemini\\antigravity\\scratch\\water_quality_automation"
$AutoOpenShortcut.Save()
'''

with open(r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\make_shortcuts.ps1", "w", encoding="utf-8-sig") as f:
    f.write(ps_script)

subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", r"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\make_shortcuts.ps1"], check=True)
print("Shortcuts updated successfully!")
