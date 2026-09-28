import os
import shutil
import sys
import tempfile
from pathlib import Path

from main import LoaderWindow, run


def self_test():
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication
    from command.ScriptCommands import ScriptGraphicsProtocol
    from view.Launcher import LauncherView

    with tempfile.TemporaryDirectory(prefix="pini-self-test-") as workspace:
        project = Path(workspace) / "Animation"
        sample = Path.cwd().parent / "sample_proj" / "sample" / "사용자애니메이션예제"
        shutil.copytree(sample, project)
        os.environ["PINI_WORKSPACE"] = workspace
        os.environ["PINI_SKIP_RECOVERY"] = "1"

        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)
        loader = LoaderWindow()

        def check_launcher():
            launchers = [window for window in app.topLevelWidgets() if isinstance(window, LauncherView) and window.isVisible()]
            if len(launchers) != 1 or not launchers[0].samplelist.data or "Animation" not in launchers[0].list.data:
                print("PINI_SELF_TEST_FAILED: launcher", flush=True)
                app.exit(1)
                return
            launcher = launchers[0]
            launcher.selectProject(launcher.list.data.index("Animation"))

        def check_project():
            ready = ScriptGraphicsProtocol().XVM is not None and any((project / "build" / "scene").glob("*.lua"))
            print("PINI_SELF_TEST_OK" if ready else "PINI_SELF_TEST_FAILED: project", flush=True)
            app.exit(0 if ready else 1)

        QTimer.singleShot(3500, check_launcher)
        QTimer.singleShot(6500, check_project)
        return app.exec()

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    run()
