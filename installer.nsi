OutFile "lsc.exe"
Name "lsc"
InstallDir "$PROGRAMFILES\lsc"
RequestExecutionLevel admin

Page components
Page directory
Page instfiles

Section "Program Files"
    SetOutPath "$INSTDIR"
    File "dist\lsc.exe"
    File ".env.example"

    CreateShortCut "$SMPROGRAMS\lsc.lnk" "$INSTDIR\lsc.exe"

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\lsc" "DisplayName" "lsc"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\lsc" "UninstallString" '"$INSTDIR\uninstaller.exe"'
    WriteUninstaller "uninstaller.exe"
SectionEnd

Section /o "Launch at Windows Startup"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Run" "lsc" "$INSTDIR\lsc.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\uninstaller.exe"
  DeleteRegValue HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Run" "lsc"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\lsc"
  Delete "$INSTDIR\lsc.exe"
  Delete "$INSTDIR\.env.example"
  Delete "$INSTDIR\.env"
  Delete "$SMPROGRAMS\lsc.lnk"
  RMDir "$INSTDIR"
SectionEnd