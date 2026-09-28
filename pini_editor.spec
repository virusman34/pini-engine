# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
import sys
from PyInstaller.utils.hooks import collect_submodules

root = Path(SPECPATH).resolve()
editor = root / "Editor"
sys.path.insert(0, str(editor / "Noriter"))

analysis = Analysis(
    [str(root / "pini_entry.py")],
    pathex=[str(editor / "pini"), str(editor / "Noriter")],
    binaries=[(str(root / ".venv" / "ATL.dll"), ".")],
    datas=[
        (str(editor / "pini" / "resource"), "Editor/pini/resource"),
        (str(editor / "sample_proj" / "sample"), "Editor/sample_proj/sample"),
        (str(root / "Engine" / "VisNovel" / "src"), "Engine/VisNovel/src"),
    ],
    hiddenimports=collect_submodules("Noriter"),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
# Do not bundle unrelated ICU DLLs found on PATH; Qt uses Windows' ICU DLL.
analysis.binaries = [entry for entry in analysis.binaries if entry[0].lower() not in {"icuuc.dll", "icudt78.dll"}]
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="PiniEditor",
    console=False,
    icon=str(editor / "pini" / "icon.ico"),
)
bundle = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    name="PiniEditor",
)
