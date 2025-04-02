@echo off
:: 请求管理员权限
fltmc >nul 2>&1 || (
    echo 请求管理员权限...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

:: 修改注册表（示例：添加启动项）
reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" /v remotecontrol /t REG_SZ /d "\"[C:\Python39\python.exe\]" \"[D:\scripts\script.py\]"" /f
pause