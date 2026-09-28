@echo off
setlocal
cd /d "%~dp0.."
call "Editor\build_atl.cmd" || exit /b 1
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --distpath dist --workpath .venv\pyinstaller-build pini_editor.spec || exit /b 1
copy /Y "Editor\PORTABLE_README.md" "dist\PiniEditor\README.md" >nul || exit /b 1
pushd dist
"..\.venv\Scripts\python.exe" -m zipfile -c PiniEditor-windows-x64.zip PiniEditor || exit /b 1
popd
set QT_QPA_PLATFORM=offscreen
"dist\PiniEditor\PiniEditor.exe" --self-test || exit /b 1
echo Built dist\PiniEditor-windows-x64.zip
