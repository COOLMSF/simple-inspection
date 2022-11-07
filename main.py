import sys
import time
import ipaddress

from view import UI_mainwidget
from view import Ui_about
from view import Ui_host_info_input

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

class Host():
    ip = None
    passwd = None
    username = None
    conn = None
    host_type = None
    
    def __init__(self, ip, username, passwd):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        
    def get_ip(self):
        return self.ip
    
    def get_username(self):
        return self.username
    
    def get_passwd(self):
        return self.passwd

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
    
class HostInfoInput(Ui_host_info_input.Ui_Form, QWidget):
    host_ip = None
    host_passwd = None
    host_username = None
    
    def __init__(self):
        super(HostInfoInput, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        
    def init_ui(self):
        # 隐藏密码
        self.le_host_passwd.setEchoMode(QLineEdit.EchoMode.Password)
        
    def init_slot(self):
        self.btn_ok.clicked.connect(lambda x: self.btn_ok_clicked())
        self.btn_cancel.clicked.connect(lambda x: self.btn_calcel_clicked())
        
    def btn_ok_clicked(self):
        self.host_ip = self.le_host_ip.text()
        self.host_username = self.le_host_username.text()
        self.host_passwd = self.le_host_passwd.text()
        
        host_info = dict()
        host_info['ip'] = self.host_ip
        host_info['passwd'] = self.host_passwd
        host_info['username'] = self.host_username
        
        self.mainwindow = MainWindow()
        # 发送host_info
        self.mainwindow.signal_host_info_input_widget.emit(host_info)
        self.close()
    
    def btn_calcel_clicked(self):
        self.close()
        
class AboutWidget(Ui_about.Ui_Form, QWidget):
    def __init__(self):
        super(AboutWidget, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        
    def btn_ok_clicked(self):
        dlg = QDialog(self)
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
    # 主机列表
    hosts = []
    
    # host_info_input widget的信号，接收子窗口传过来的IP，账号，密码
    signal_host_info_input_widget = pyqtSignal(dict)
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        
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
    
    # top right side UI logic
    def btn_batch_cmd_import_clicked(self):
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
        
    # buttom side UI logic
    def btn_conn_test_clicked(self):
        for host in self.hosts:
            # init ssh woker
            self.ssh_conn_test_worker = SSHConnTestWorker(self)
            self.ssh_conn_test_worker.start()
        
        self.showProgregssDialog()
        
    def btn_inspection_clicked(self):
        self.ssh_exec_cmd_worker = SSHExecCmdWoker()
        self.ssh_exec_cmd_worker.start()
        self.showProgregssDialog()
        
    def btn_about_clicked(self):
        AboutWidget().show()
        
    # top left side UI logic
    def btn_add_host_clicked(self):
        HostInfoInput().show()
    
    def btn_del_host_clicked(self):
        selected_items = self.tw_host_info.selectedItems()
        if not selected_items:
            return
        else:
            for i, host in enumerate(selected_items):
                selected_items = self.tw_host_info.selectedItems()[i].text()
                self.del_host(selected_items)
    
    def btn_undo_host_clicked(self):
        pass
    
    def btn_batch_host_import_clicked(self):
        pass
    
    def add_host(self, host_info):
        self.hosts.append(Host(ip=host_info['ip'], username=host_info['username'], passwd=host_info['passwd']))
        # 更新UI
        self.update_ui_host()

        
    def del_host(self, ip):
        for host in self.hosts:
            # 按照ip删除主机
            if host.ip == ip:
                self.hosts.remove(host)
        self.update_ui_host()
        
    def get_all_hosts(self):
        for host in self.hosts:
            print("Host:%s\nUsername:%s\nPasswd:%s" % host.ip, host.username, host.passwd)
        
    # UI更新部分
    def update_ui_host(self):
        for i, host in enumerate(self.hosts):
            print(i, str(host.ip), host.username, host.passwd)
            print(self.tw_host_info)
            self.tw_host_info.setItem(i, 0, QTableWidgetItem(host.ip))
            self.tw_host_info.setItem(i, 1, QTableWidgetItem(str(host.username)))
            self.tw_host_info.setItem(i, 2, QTableWidgetItem(str(host.passwd)))
        
    def init_ui(self):
        self.resize(1000, 700)
        
        # 巡检按钮需要先通过连接性测试才能激活
        self.btn_inspection.setEnabled(False)
        # 设置固定窗口大小
        self.setFixedSize(self.width(), self.height())
        
        # 设置行数
        self.tw_host_info.setRowCount(3)
        self.tw_host_info.setColumnCount(4)
    
    # 槽部分
    def init_slot(self):
        # top left side
        self.btn_add_host.clicked.connect(lambda x: self.btn_add_host_clicked())
        self.btn_del_host.clicked.connect(lambda x: self.btn_del_host_clicked())
        self.btn_undo_host.clicked.connect(lambda x: self.btn_undo_host_clicked())
        self.btn_batch_host_import.clicked.connect(lambda x: self.btn_batch_host_import_clicked())
        
        # top right side
        self.btn_batch_cmd_import.clicked.connect(lambda x: self.btn_batch_cmd_import_clicked())
        
        # buttom side
        self.btn_about.clicked.connect(lambda x: self.btn_about_clicked())
        self.btn_inspection.clicked.connect(lambda x: self.btn_inspection_clicked())
        self.btn_conn_test.clicked.connect(lambda x: self.btn_conn_test_clicked())
        
        # signal
        self.signal_host_info_input_widget.connect(lambda x:self.add_host(x))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
    