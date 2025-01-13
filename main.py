import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *


class BrowserTab(QWebEngineView):
    def __init__(self):
        super(BrowserTab, self).__init__()
        self.setUrl(QUrl("http://google.com"))  # replace with your website


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.browser_tabs)
        self.showMaximized()

        # Add initial tab
        self.add_new_tab(QUrl("http://google.com"), "Home")

        # Navigation Bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().back())
        nav_bar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().forward())
        nav_bar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.browser_tabs.currentWidget().reload())
        nav_bar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)
        #add new tab button here
        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_bar.addAction(new_tab_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)
        self.browser_tabs.currentChanged.connect(self.update_url)

        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        nav_bar.addAction(new_tab_btn)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or not isinstance(qurl, QUrl):
            qurl = QUrl("http://google.com")
        browser = BrowserTab()
        browser.setUrl(qurl)
        i = self.browser_tabs.addTab(browser, label)
        self.browser_tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

    def close_tab(self, i):
        if self.browser_tabs.count() < 2:
            return
        self.browser_tabs.removeTab(i)

    def navigate_home(self):
        self.browser_tabs.currentWidget().setUrl(QUrl("http://google.com"))  # replace with your website

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser_tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, i):
        qurl = self.browser_tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())

    def update_url_bar(self, qurl, browser=None):
        if browser != self.browser_tabs.currentWidget():
            return
        self.url_bar.setText(qurl.toString())


app = QApplication(sys.argv)
QApplication.setApplicationName("My Browser")
window = MainWindow()
app.exec_()