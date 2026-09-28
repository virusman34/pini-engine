@echo off
setlocal

for /f "delims=" %%V in ('"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath') do set "VS_DIR=%%V"
if not defined VS_DIR (
    echo Visual Studio C++ build tools are required.
    exit /b 1
)

call "%VS_DIR%\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
if not exist "%~dp0..\.venv" mkdir "%~dp0..\.venv"

cl /nologo /LD /EHsc /DGPP_FOR_PYTHON /I "%~dp0..\Engine\VisNovel\frameworks\cocos2d-x\external" /I "%~dp0..\Engine\VisNovel\frameworks\runtime-src\Classes" "%~dp0..\Engine\VisNovel\frameworks\runtime-src\Classes\ATL.cpp" /Fo"%~dp0..\.venv\ATL.obj" /link /OUT:"%~dp0..\.venv\ATL.dll" /IMPLIB:"%~dp0..\.venv\ATL.lib" /EXPORT:registAnimation /EXPORT:getFrame /EXPORT:deleteFrame /EXPORT:getMaxFrame /EXPORT:getNumberVal /EXPORT:getNumberSetVal /EXPORT:getNumberSet /EXPORT:isValue /EXPORT:getStringVal /EXPORT:getMarkedFrames /EXPORT:numNode /EXPORT:isExists /EXPORT:registStringValue /EXPORT:registNumberValue /EXPORT:deleteNodeValue /EXPORT:clearFrame
