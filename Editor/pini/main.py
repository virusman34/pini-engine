# -*- coding: utf-8 -*-
import sys
from config import *

if config.__RELEASE__ == False : 
	sys.path.append("../Noriter")
else:
	# sys.stderr   = Error_Logger
	# sys.stdout   = Error_Logger
	pass

from PySide.QtGui import *
from PySide.QtCore import *
from Noriter.views.NoriterMainWindow import *
from Noriter.utils.Settings import Settings

import os
from pathlib import Path
import json
import urllib.request, urllib.error, urllib.parse

if getattr(sys, "frozen", False):
	os.chdir(Path(sys._MEIPASS) / "Editor" / "pini")

Error_Logger = open("ERROR_LOG.txt","w+")

from view.LoaderView import LoaderWindow

launcher = None
def run():
	app = QtGui.QApplication(sys.argv)
	app.setQuitOnLastWindowClosed(False)

	def quit_when_no_windows():
		if not any(window.isVisible() for window in app.topLevelWidgets()):
			app.quit()

	app.lastWindowClosed.connect(lambda: QTimer.singleShot(0, quit_when_no_windows))

	v = LoaderWindow()
	_exit_ = app.exec()
	##################
	Error_Logger.close()
	##################
	sys.exit(_exit_)

if __name__ == "__main__":
	run()

