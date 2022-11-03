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
    QProgressDialog
)

import re
import os
import time
import socket

from netmiko import Netmiko
import paramiko
from paramiko import ssh_exception
from paramiko.ssh_exception import AuthenticationException

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
        
        is_connected, msg = self.is_connect()
        
        # ssh连通，打开巡检按钮
        if is_connected:
            self.btn_inspection.setEnabled(True)
            
        self.te_cmd_output.setText(msg)
    
    # 返回连接状态(bool)，连接信息(str)
    def is_connect(self) -> (bool, str):
        sip = self.ip
        sport = 22
        susername = self.username
        spassword = self.passwd
        
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            conn.connect(sip, port=sport, username=susername, password=spassword, timeout=15)
            connect_result = "Connect Server {0} {1} {2} {3} 主机连接成功!\n".format(
                sip, sport, susername, spassword)
            data = '{"code": "1000", "msg": "主机连接成功","result": true}'
            return (True, data)
        except AuthenticationException:
            connect_result = "Connect Server {0} {1} {2} {3} 用户名或密码错误!\n".format(
                sip, sport, susername, spassword)
            data = '{"code": "5000", "msg": "用户名或密码错误","result": false}'
            return (False, data)
        except socket.timeout:
            connect_result = "Connect Server {0} {1} {2} {3} 主机连接异常!\n".format(
                sip, sport, susername, spassword)
            data = '{"code": "6000", "msg": "主机连接异常","result": false}'
            return (False, data)
        except ssh_exception.SSHException:
            connect_result = "Connect Server {0} {1} {2} {3} 端口错误!\n".format(
                sip, sport, susername, spassword)
            data = '{"code": "7000", "msg": "端口错误","result": false}'
            return (False, connect_result)
        
    def exec_cmd(self, cmd) -> str:
        # need to do filter
        result_str = ""
        dev = {
            'device_type': 'linux',
            'username': self.username,
            'password': self.passwd,
            'port': 22,
            'host': self.ip,
        }
        
        # print_template = ("===================================================================\n时间: %s\n命令执行状态: %s\n命令执行结果: \n%s\n===================================================================\n")
        print_template = ("==============================================================\n时间: %s\n命令执行状态: %s\n当前执行命令： %s\n命令执行结果: \n%s\n")
        
        with Netmiko(**dev) as ssh:
            # 通过ssh命令，结果返回
            try:
                cur_time = time.asctime()
                # TOTO, set text color to red
                real_info = ssh.send_command(cmd)
                result_str = print_template % (cur_time, '执行成功', cmd, real_info)

            except Exception as e:
                cur_time = time.asctime()
                result_str = print_template % (cur_time, '执行失败', cmd, '')
        return result_str
    
    def showDialog(self):
       num = 100000
       progress = QProgressDialog(self)
       progress.setWindowTitle("请稍等")  
       progress.setLabelText("正在操作...")
       progress.setCancelButtonText("取消")
       progress.setMinimumDuration(5)
       progress.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
       progress.setRange(0,num) 
       for i in range(num):
           progress.setValue(i) 
           if progress.wasCanceled():
               QMessageBox.warning(self,"提示","操作失败") 
               break
       else:
           progress.setValue(num)
           QMessageBox.information(self,"提示","操作成功")
    
    def btn_inspection_clicked(self):
        pg = QProgressDialog()
        
        self.cmd_array = self.te_cmd_input.toPlainText().split('\n')
        tmp_buf = ""
        for cmd in self.cmd_array:
            tmp_buf += self.exec_cmd(cmd)
            self.te_cmd_output.setText(tmp_buf)
        
    def init_ui(self):
        self.resize(1000, 700)
        
        # 巡检按钮需要先通过连接性测试才能激活
        self.btn_inspection.setEnabled(False)
        
        # self.le_ipaddr.setValidator()
        
        # 密码输入
        self.le_passwd.setEchoMode(QLineEdit.EchoMode.Password)
        
        # 禁止最大化
        # self.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)
        
        # 设置固定大小
        self.setFixedSize(self.width(), self.height()); 
        
    def init_slot(self):
        self.btn_about.clicked.connect(lambda x: self.btn_about_clicked())
        self.btn_inspection.clicked.connect(lambda x: self.btn_inspection_clicked())
        # self.btn_conn_test.clicked.connect(lambda x: self.btn_conn_test_clicked())
        self.btn_conn_test.clicked.connect(lambda x: self.showDialog())
        self.btn_import.clicked.connect(lambda x: self.btn_import_clicked())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())
    