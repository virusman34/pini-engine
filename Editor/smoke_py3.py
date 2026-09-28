"""Launch the migrated editor and open a disposable project offscreen."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox


ROOT = Path(__file__).resolve().parent.parent
EDITOR = ROOT / "Editor" / "pini"
temporary_workspace = tempfile.TemporaryDirectory(prefix="pini-smoke-", dir=ROOT / ".venv")
WORKSPACE = Path(temporary_workspace.name)
PROJECT = WORKSPACE / "Animation"

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["PINI_WORKSPACE"] = str(WORKSPACE)
os.environ["PINI_SKIP_RECOVERY"] = "1"
os.chdir(EDITOR)
sys.path = [path for path in sys.path if Path(path).resolve() != ROOT / "Editor"]
sys.path.insert(0, str(EDITOR))

import main

errors = []
original_excepthook = sys.excepthook
sys.excepthook = lambda kind, value, traceback: errors.append(value)
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
loader = main.LoaderWindow()


def check_editor():
    from compiler import LNXToolChain
    from view.Launcher import LauncherView, exampleCopyer

    launchers = [w for w in app.topLevelWidgets() if isinstance(w, LauncherView) and w.isVisible()]
    assert len(launchers) == 1, "Project launcher did not open"
    launcher = launchers[0]
    sample_name = "사용자애니메이션예제"
    launcher.samplelist.selectIndex(launcher.samplelist.data.index(sample_name))
    with patch.object(QMessageBox, "information", return_value=QMessageBox.Ok):
        copier = exampleCopyer(launcher.sampleDir, sample_name, launcher)
        copier.name = "Animation"
        copier.useExample()
    launcher.loadingWorkspace(str(WORKSPACE))
    assert "Animation" in launcher.list.data, "Disposable project was not listed"
    project_index = launcher.list.data.index("Animation")
    launcher.list.selectIndex(project_index)
    launcher.selectProject(project_index)
    toolchain = LNXToolChain()
    ok, result = toolchain.gen_obj((PROJECT / "scene" / "메인.lnx").read_text(encoding="utf-8"), isActivePreProcess=False)
    assert ok, f"Sample LNX did not compile (line {result})"
    assert toolchain.gen_lua(result), "Sample LNX did not generate Lua"


QTimer.singleShot(3500, check_editor)


def check_preview():
    from command.ScriptCommands import ScriptGraphicsProtocol
    from controller.SceneListController import SceneListController

    assert ScriptGraphicsProtocol().XVM is not None, "Lua preview did not initialize"
    assert any((PROJECT / "build" / "scene").glob("*.lua")), "Sample scene was not compiled"
    SceneListController.getInstance().Open(str(PROJECT / "scene" / "메인.lnx"))


def check_save():
    from view.SceneScriptWindow import SceneScriptWindowManager

    scene = PROJECT / "scene" / "메인.lnx"
    window = SceneScriptWindowManager.getInstance().getActive()
    assert window is not None, "Scene editor did not open"
    original = scene.read_text(encoding="utf-8")
    window.editor.setPlainText(original + "\n")
    window.saveScene()
    assert scene.read_text(encoding="utf-8") == original + "\n", "Scene edit was not saved"


QTimer.singleShot(6000, check_preview)
QTimer.singleShot(9000, check_save)
QTimer.singleShot(12000, app.quit)
app.exec()
sys.excepthook = original_excepthook
temporary_workspace.cleanup()
if errors:
    raise errors[0]
print("Editor launch, example copy, project open, scene edit, and save passed")
