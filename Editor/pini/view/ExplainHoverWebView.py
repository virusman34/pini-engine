# -*- coding: utf-8 -*-
import sys

from PySide.QtGui import * 
from PySide.QtCore import *
from PySide6.QtWidgets import QTextBrowser

class ExplainHoverWebView(QTextBrowser) :
	# 마우스를 글자에 두었을때 뜨는 툴팁창
	def __init__(self,parent=None):
		super(ExplainHoverWebView,self).__init__(parent)
		self.setOpenLinks(False)
		self.anchorClicked.connect(self.onLinkClicked)

	def onLinkClicked(self,url):
		QDesktopServices.openUrl(url);

	def leaveEvent(self,e):
		self.resize(0,0)
		return super(ExplainHoverWebView,self).leaveEvent(e)

	def hideEvent(self,e):
		self.clearFocus()
		return super(ExplainHoverWebView,self).hideEvent(e)
