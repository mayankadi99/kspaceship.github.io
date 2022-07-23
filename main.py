from operator import iconcat
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import matplotlib.pyplot as plt
from tkinter import *
import sys
import os

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.setCentralWidget(self.tabs)
		self.status = QStatusBar()
		self.setStatusBar(self.status)
		navtb = QToolBar("Navigation")
		self.addToolBar(navtb)

		back_btn = QAction(QIcon('back.png'), 'Go back',self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(lambda:self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		forward_btn = QAction(QIcon('forward.png'),'Go forward', self)
		forward_btn.setStatusTip("Forward to next page")
		forward_btn.triggered.connect(lambda:self.tabs.currentWidget().forward())
		navtb.addAction(forward_btn)

		reload_btn = QAction(QIcon('reload.png'),'Reload this page', self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(lambda:self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		home_btn = QAction(QIcon('home.png'),'Go back to home', self)
		home_btn.setStatusTip("Go home")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		navtb.addSeparator()
		
		self.urlBar = QLineEdit()
		self.urlBar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlBar)

		stop_btn = QAction(QIcon('cancel.png'), 'Stop loading current page', self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(lambda:self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		ks_btn = QAction(QIcon('about.png'), 'Go to Khanda Corp. Main Website', self)
		ks_btn.setStatusTip("Go to Khanda Corp. Main Website")
		ks_btn.triggered.connect(self.navigate_koala)
		navtb.addAction(ks_btn)

		self.add_new_tab(QUrl('file:///C:/Users/mayan/Desktop/Koala%20Software/Koala_SpaceShip_(Python_ED)/google.html'), 'homepage')
		self.show()
		self.setWindowTitle('Khanda SpaceShip New Tab')
		self.setWindowIcon(QIcon('image/icon.ico'))

	def add_new_tab(self, qurl=None, label = "Khanda SpaceShip"):
		if qurl is None:
			qurl = QUrl('file:///C:/Users/mayan/Desktop/Koala%20Software/Koala_SpaceShip_(Python_ED)/google.html')

		browser = QWebEngineView()
		browser.setUrl(qurl)

		i= self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser = browser : self.update_urlbar(qurl, browser))

		browser.loadFinished.connect(lambda _, i= i, browser = browser : self.tabs.setTabText(i, browser.page().title()))

	def tab_open_doubleclick(self, i):

		if i == -1:
			self.add_new_tab()

	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title(self.tabs.currentWidget())

	def close_current_tab(self, i):
		if self.tabs.count() <2:
			return

		self.tabs.removeTab(i)

	def update_title(self, browser):
		if browser != self.tabs.currentWidget():
			return

		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s - Khanda SpaceShip" % title)

	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl("file:///C:/Users/mayan/Desktop/Koala%20Software/Koala_SpaceShip_(Python_ED)/google.html"))

	def navigate_koala(self):
		self.tabs.currentWidget().setUrl(QUrl("file:///C:/Users/mayan/Desktop/Koala%20Software/Main%20Website/index.html"))

	def navigate_to_url(self):
		q = QUrl(self.urlBar.text())
		if q.scheme()== "":
			q.setScheme("https")

		self.tabs.currentWidget().setUrl(q)

	def update_urlbar(self, q, browser = None):
		if browser != self.tabs.currentWidget():
			return
		
		self.urlBar.setText(q.toString())
		self.urlBar.setCursorPosition(0)

	input("Press [Enter] to continue.")

app = QApplication(sys.argv)
app.setApplicationName("Khanda SpaceShip")
app.setOrganizationName("Khanda Corparation")
app.setOrganizationDomain("khanda.ca")
window  = MainWindow()
app.exec_() 
