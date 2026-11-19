$DesktopPath = [Environment]::GetFolderPath('Desktop')
$ShortcutPath = [System.IO.Path]::Combine($DesktopPath, "환경 및 공정 관리 대시보드.lnk")

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = '"C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\run_dashboard_silent.vbs"'
$Shortcut.WorkingDirectory = "C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
$Shortcut.Description = "세아제강 창원공장 환경/공정 관리 대시보드"
$Shortcut.IconLocation = "shell32.dll, 14"
$Shortcut.Save()

Write-Host "바탕화면에 바로가기 업데이트 완료: $ShortcutPath"
