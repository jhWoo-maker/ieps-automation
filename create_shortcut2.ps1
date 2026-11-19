$DesktopPath = [Environment]::GetFolderPath('Desktop')
$ShortcutPath = [System.IO.Path]::Combine($DesktopPath, "대시보드 직접열기.lnk")

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\user\.gemini\antigravity\scratch\water_quality_automation\run_dashboard_silent.bat"
$Shortcut.WorkingDirectory = "C:\Users\user\.gemini\antigravity\scratch\water_quality_automation"
$Shortcut.WindowStyle = 7
$Shortcut.Description = "세아제강 창원공장 환경/공정 관리 대시보드 직접 열기"
$Shortcut.IconLocation = "imageres.dll, 114"
$Shortcut.Save()

Write-Host "바탕화면에 2번째 바로가기 생성 완료: $ShortcutPath"
