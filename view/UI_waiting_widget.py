# Form implementation generated from reading ui file 'UI/waiting_widget.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(539, 341)
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setGeometry(QtCore.QRect(120, 200, 100, 32))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_cancel = QtWidgets.QPushButton(Form)
        self.btn_cancel.setGeometry(QtCore.QRect(310, 200, 100, 32))
        self.btn_cancel.setObjectName("btn_cancel")
        self.label_msg = QtWidgets.QLabel(Form)
        self.label_msg.setGeometry(QtCore.QRect(200, 90, 161, 41))
        self.label_msg.setObjectName("label_msg")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_ok.setText(_translate("Form", "ok"))
        self.btn_cancel.setText(_translate("Form", "cancel"))
        self.label_msg.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt;\">正在开始巡检</span></p></body></html>"))
