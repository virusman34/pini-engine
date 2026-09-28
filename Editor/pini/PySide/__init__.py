"""Legacy PySide imports backed by PySide6 during the editor migration."""

import sys

from PySide6 import QtCore, QtGui, QtNetwork, QtWidgets


def set_codec(stream, name):
    if name.upper() != "UTF-8":
        raise ValueError(f"Unsupported legacy QTextStream encoding: {name}")
    stream.setEncoding(QtCore.QStringConverter.Encoding.Utf8)


QtCore.QTextStream.setCodec = set_codec
QtCore.QObject.trUtf8 = QtCore.QObject.tr
QtGui.QFontMetrics.width = QtGui.QFontMetrics.horizontalAdvance
QtWidgets.QPlainTextEdit.setTabStopWidth = QtWidgets.QPlainTextEdit.setTabStopDistance
QtWidgets.QGraphicsView.matrix = QtWidgets.QGraphicsView.transform

# Qt 4 kept widgets in QtGui. Existing editor modules import them from there.
for name in dir(QtWidgets):
    if name.startswith("Q") and not hasattr(QtGui, name):
        setattr(QtGui, name, getattr(QtWidgets, name))

sys.modules[__name__ + ".QtCore"] = QtCore
sys.modules[__name__ + ".QtGui"] = QtGui
sys.modules[__name__ + ".QtNetwork"] = QtNetwork
