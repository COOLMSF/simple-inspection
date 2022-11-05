import sys
import time
import ipaddress

from view import UI_mainwidget
from view import Ui_about

# validate ip
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6 import QtCore 
from PyQt6.QtCore import (QStringListModel, QDir)
from PyQt6 import QtWidgets
from PyQt6 import sip
from PyQt6.QtCore import QThread, QObject, pyqtSignal

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QMessageBox,
    QPushButton,
    QLineEdit,
    QListView,
    QFileDialog,
    QProgressDialog,
)

import re
import os
import time
import socket

from netmiko import BaseConnection, Netmiko
import paramiko
from paramiko import ssh_exception
from paramiko.ssh_exception import AuthenticationException

# 全局ssh句柄
conn = None

class SSHExecCmdWoker(QThread):
    signal_ssh_cmd_exec_over = pyqtSignal()
    
    def __init__(self, mainwindow):
        super(SSHExecCmdWoker, self).__init__()
        self.mainwindow = mainwindow
        
        # 获取全局ssh句柄
        self.conn = conn
        
        self.run = True
        self.cmd = mainwindow.cmd
        self.cmd_array = mainwindow.cmd_array
        
        self.signal_ssh_cmd_exec_over.connect(self.update_ui)
        
    def update_ui(self):
        self.mainwindow.te_cmd_output.setText("链接测试通过✅")
        # ssh连通，打开巡检按钮
        self.mainwindow.btn_inspection.setEnabled(True)
        # self.mainwindow.te_cmd_output.setText(connect_msg)
    
    def run(self):
        cmd_exec_result = self.exec_cmd_array()
        self.signal_ssh_cmd_exec_over.emit(cmd_exec_result)
    
    def exec_cmd_array(self) -> str:
        self.cmd_array = self.te_cmd_input.toPlainText().split('\n')
        cmd_exec_result = ""
        for self.cmd in self.cmd_array:
            cmd_exec_result += self.exec_cmd(self.cmd)
        
        return cmd_exec_result
        
    def exec_cmd(self, cmd) -> str:
        # print_template = ("===================================================================\n时间: %s\n命令执行状态: %s\n命令执行结果: \n%s\n===================================================================\n")
        print_template = ("==============================================================\n时间: %s\n命令执行状态: %s\n当前执行命令： %s\n命令执行结果: \n%s\n")
        
        try:
            cur_time = time.asctime()
            # TOTO, set text color to red
            real_info = self.ssh.send_command(cmd)
            result_str = print_template % (cur_time, '执行成功', cmd, real_info)

        except Exception as e:
            cur_time = time.asctime()
            result_str = print_template % (cur_time, '执行失败', cmd, '')
            
        return result_str

class SSHConnTestWorker(QThread):
    signal_ssh_connected = pyqtSignal()
    signal_ssh_not_connected = pyqtSignal()
    
    def __init__(self, mainwindow):
        super(SSHConnTestWorker, self).__init__()
        self.mainwindow = mainwindow
        self.run = True
        self.ip = mainwindow.ip
        self.port = 22
        self.username = mainwindow.username
        self.passwd = mainwindow.passwd
        
        self.signal_ssh_connected.connect(self.update_ui_connected)
        self.signal_ssh_not_connected.connect(self.update_ui_not_connected)
        
    def update_ui_connected(self):
        self.mainwindow.te_cmd_output.setText("链接测试通过✅")
        # ssh连通，打开巡检按钮
        self.mainwindow.btn_inspection.setEnabled(True)
        # self.mainwindow.te_cmd_output.setText(connect_msg)
        
    def update_ui_not_connected(self):
        self.mainwindow.te_cmd_output.setText("链接测试失败❎")
    
    def run(self):
        is_connected, conn = self.try_connect()
        if is_connected:
            self.signal_ssh_connected.emit()
        else:
            self.signal_ssh_not_connected.emit()
        
    # 返回连接状态(bool)，连接句柄(conn)
    def try_connect(self):
        dev = {
            'device_type': 'linux',
            'username': self.username,
            'password': self.passwd,
            'port': 22,
            'host': self.ip,
        }
        print_template = ("==============================================================\n时间: %s\n命令执行状态: %s\n当前执行命令： %s\n命令执行结果: \n%s\n")
            
        try:
            with Netmiko(**dev) as ssh:
                # 保存ssh连接
                self.conn = ssh
                self.status = True
            
        except Exception as e:
            self.conn = None
            self.status = False
        
        return (self.status, self.conn)
        
class AboutWidget(Ui_about.Ui_Form, QWidget):
    def __init__(self):
        super(AboutWidget, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        self.show()
        
    def btn_ok_clicked(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Ok btn")
        dlg.exec()
    
    def btn_quit_clicked(self):
        self.close()
        
    def init_ui(self):
        self.setWindowTitle("关于")
        flags = self.windowFlags()
        self.setWindowFlags(flags | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        
    def init_slot(self):
        self.btn_ok.clicked.connect(lambda x: self.btn_ok_clicked())
        self.btn_quit.clicked.connect(lambda x: self.btn_quit_clicked())
        
class MainWindow(UI_mainwidget.Ui_Form, QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        self.show()
        
    def showProgregssDialog(self):
       # num = 10000
       num = 5000
       progress = QProgressDialog(self)
       progress.setWindowTitle("请稍等")  
       progress.setLabelText("正在测试连接...")
       # progress.setCancelButtonText("取消")
       progress.setMinimumDuration(1)
       progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
       progress.setRange(0,num) 
       for i in range(num):
           progress.setValue(i) 
           if progress.wasCanceled():
               QMessageBox.warning(self,"提示","操作失败") 
               break
        # 这个else怎么没对齐？
       else:
           progress.setValue(num)
           QMessageBox.information(self,"提示","操作成功")
    
    def btn_inspection_clicked(self):
        self.ssh_exec_cmd_worker = SSHExecCmdWoker()
        self.ssh_exec_cmd_worker.start()
        self.showProgregssDialog()
        
    def btn_import_clicked(self):
        fdlg = QFileDialog()
        fdlg.setFileMode(QFileDialog.FileMode.AnyFile)
        
        if fdlg.exec():
            #接受选中文件的路径，默认为列表
            filenames = fdlg.selectedFiles()
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
            f=open(filenames[0],'r')

            with f:
                #接受读取的内容，并显示到多行文本框中
                data=f.read()
                self.te_cmd_input.setText(data)
        
    def btn_about_clicked(self):
        AboutWidget()
        
    def btn_conn_test_clicked(self):
        self.ip = self.le_ipaddr.displayText()
        self.username = self.le_username.displayText()
        self.passwd = self.le_passwd.text()
        
        # init ssh woker
        self.ssh_conn_test_worker = SSHConnTestWorker(self)
        self.ssh_conn_test_worker.start()
        self.showProgregssDialog()
        
    def init_ui(self):
        self.resize(1000, 700)
        
        # 巡检按钮需要先通过连接性测试才能激活
        self.btn_inspection.setEnabled(False)
        
        # 密码输入
        self.le_passwd.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 设置固定大小
        self.setFixedSize(self.width(), self.height()); 
        
    def init_slot(self):
        self.btn_about.clicked.connect(lambda x: self.btn_about_clicked())
        self.btn_inspection.clicked.connect(lambda x: self.btn_inspection_clicked())
        self.btn_conn_test.clicked.connect(lambda x: self.btn_conn_test_clicked())
        self.btn_import.clicked.connect(lambda x: self.btn_import_clicked())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
    