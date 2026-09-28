# -*- coding: utf-8 -*-
import sys

from PySide.QtGui import * 
from PySide.QtCore import *
from PySide6.QtWidgets import QTextBrowser

class ExplainWebView(QTextBrowser) :
	# 자동완성과 같이 뜨는 툴팁창
	def __init__(self,completer,parent=None):
		super(ExplainWebView,self).__init__(parent)
		self.completer = completer
		self.setOpenLinks(False)
		self.anchorClicked.connect(self.onLinkClicked)

	def onLinkClicked(self,url):
		QDesktopServices.openUrl(url);

	def hideEvent(self,e):
		self.clearFocus()
		return super(ExplainWebView,self).hideEvent(e)
