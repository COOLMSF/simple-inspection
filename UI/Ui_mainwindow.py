# Form implementation generated from reading ui file 'UI/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(833, 709)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(110, 80, 595, 481))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridFrame = QtWidgets.QFrame(self.widget)
        self.gridFrame.setMinimumSize(QtCore.QSize(228, 194))
        self.gridFrame.setMaximumSize(QtCore.QSize(228, 194))
        self.gridFrame.setStyleSheet("border: 1px solid  rgb(214, 214, 214) \n"
"")
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.gridFrame)
        self.label_5.setMinimumSize(QtCore.QSize(87, 26))
        self.label_5.setMaximumSize(QtCore.QSize(87, 26))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        self.le_ipaddr = QtWidgets.QLineEdit(self.gridFrame)
        self.le_ipaddr.setMinimumSize(QtCore.QSize(127, 22))
        self.le_ipaddr.setMaximumSize(QtCore.QSize(127, 22))
        self.le_ipaddr.setObjectName("le_ipaddr")
        self.horizontalLayout_4.addWidget(self.le_ipaddr)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.gridFrame)
        self.label_6.setMinimumSize(QtCore.QSize(87, 26))
        self.label_6.setMaximumSize(QtCore.QSize(87, 26))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.le_username = QtWidgets.QLineEdit(self.gridFrame)
        self.le_username.setMinimumSize(QtCore.QSize(127, 22))
        self.le_username.setMaximumSize(QtCore.QSize(127, 22))
        self.le_username.setObjectName("le_username")
        self.horizontalLayout_5.addWidget(self.le_username)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.gridFrame)
        self.label_8.setMinimumSize(QtCore.QSize(87, 26))
        self.label_8.setMaximumSize(QtCore.QSize(87, 26))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.le_passwd = QtWidgets.QLineEdit(self.gridFrame)
        self.le_passwd.setMinimumSize(QtCore.QSize(127, 22))
        self.le_passwd.setMaximumSize(QtCore.QSize(127, 22))
        self.le_passwd.setObjectName("le_passwd")
        self.horizontalLayout_6.addWidget(self.le_passwd)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.gridFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setMinimumSize(QtCore.QSize(83, 149))
        self.label_7.setMaximumSize(QtCore.QSize(83, 149))
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.btn_import = QtWidgets.QPushButton(self.widget)
        self.btn_import.setMinimumSize(QtCore.QSize(83, 32))
        self.btn_import.setMaximumSize(QtCore.QSize(83, 32))
        self.btn_import.setObjectName("btn_import")
        self.verticalLayout.addWidget(self.btn_import)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.te_cmd_input = QtWidgets.QTextEdit(self.widget)
        self.te_cmd_input.setMinimumSize(QtCore.QSize(256, 192))
        self.te_cmd_input.setMaximumSize(QtCore.QSize(256, 192))
        self.te_cmd_input.setStyleSheet("")
        self.te_cmd_input.setObjectName("te_cmd_input")
        self.horizontalLayout.addWidget(self.te_cmd_input)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(98, 29))
        self.label.setMaximumSize(QtCore.QSize(98, 29))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.te_cmd_output = QtWidgets.QTextEdit(self.widget)
        self.te_cmd_output.setStyleSheet("")
        self.te_cmd_output.setObjectName("te_cmd_output")
        self.verticalLayout_2.addWidget(self.te_cmd_output)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_conn_test = QtWidgets.QPushButton(self.widget)
        self.btn_conn_test.setMinimumSize(QtCore.QSize(137, 32))
        self.btn_conn_test.setMaximumSize(QtCore.QSize(137, 32))
        self.btn_conn_test.setObjectName("btn_conn_test")
        self.horizontalLayout_2.addWidget(self.btn_conn_test)
        self.btn_export = QtWidgets.QPushButton(self.widget)
        self.btn_export.setMinimumSize(QtCore.QSize(136, 32))
        self.btn_export.setMaximumSize(QtCore.QSize(136, 32))
        self.btn_export.setObjectName("btn_export")
        self.horizontalLayout_2.addWidget(self.btn_export)
        self.btn_inspection = QtWidgets.QPushButton(self.widget)
        self.btn_inspection.setMinimumSize(QtCore.QSize(137, 32))
        self.btn_inspection.setMaximumSize(QtCore.QSize(137, 32))
        self.btn_inspection.setObjectName("btn_inspection")
        self.horizontalLayout_2.addWidget(self.btn_inspection)
        self.btn_about = QtWidgets.QPushButton(self.widget)
        self.btn_about.setMinimumSize(QtCore.QSize(137, 32))
        self.btn_about.setMaximumSize(QtCore.QSize(137, 32))
        self.btn_about.setObjectName("btn_about")
        self.horizontalLayout_2.addWidget(self.btn_about)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 833, 22))
        self.menubar.setObjectName("menubar")
        self.menuDevice = QtWidgets.QMenu(self.menubar)
        self.menuDevice.setObjectName("menuDevice")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOption = QtWidgets.QMenu(self.menubar)
        self.menuOption.setObjectName("menuOption")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionFAQ = QtGui.QAction(MainWindow)
        self.actionFAQ.setObjectName("actionFAQ")
        self.menuDevice.addAction(self.action)
        self.menuDevice.addAction(self.action_2)
        self.menuDevice.addAction(self.action_3)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionFAQ)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOption.menuAction())
        self.menubar.addAction(self.menuDevice.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">设备IP</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">用户名</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">密码</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">命令</span></p></body></html>"))
        self.btn_import.setText(_translate("MainWindow", "批量导入"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">当前运行结果</span></p></body></html>"))
        self.btn_conn_test.setText(_translate("MainWindow", "连接性测试"))
        self.btn_export.setText(_translate("MainWindow", "导出报告"))
        self.btn_inspection.setText(_translate("MainWindow", "巡检"))
        self.btn_about.setText(_translate("MainWindow", "关于"))
        self.menuDevice.setTitle(_translate("MainWindow", "Device"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOption.setTitle(_translate("MainWindow", "Option"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.action.setText(_translate("MainWindow", "堡垒机"))
        self.action_2.setText(_translate("MainWindow", "数据库审计"))
        self.action_3.setText(_translate("MainWindow", " 日志审计"))
        self.actionOpen.setText(_translate("MainWindow", "Open(Ctrl+O)"))
        self.actionSave.setText(_translate("MainWindow", "Save(Ctrl+S)"))
        self.actionSaveAs.setText(_translate("MainWindow", "SaveAs(Ctrl+Shift+S)"))
        self.actionQuit.setText(_translate("MainWindow", "Quit(Ctrl+Q)"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionFAQ.setText(_translate("MainWindow", "FAQ"))
