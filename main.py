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
from PyQt6 import sip
from PyQt6.QtCore import QThread, QObject, pyqtSignal, QMutex, QTimer

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
    QAbstractItemView,
    QHeaderView
)

import re
import os
import time
import socket

from netmiko import BaseConnection, Netmiko
import paramiko
from paramiko import ssh_exception
from paramiko.ssh_exception import AuthenticationException

class Host():
    ip = None
    passwd = None
    username = None
    host_type = None
    
    conn = None
    status = None
    cmd_result = str()
    cmd_array = list()
    
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
    
    def set_cmd_array(self, cmd_array: list):
        self.cmd_array = cmd_array

    def get_cmd_array(self) -> list:
        return self.cmd_array
    
    def get_cmd_result(self) -> str:
        return self.cmd_result
    
class SSHCmdExecWoker(QThread):
    signal_ssh_cmd_exec_over = pyqtSignal(str)
    
    def __init__(self, host):
        super(SSHCmdExecWoker, self).__init__()
        self.run = True
        
        self.host = host
        
    def run(self):
        self.host.cmd_result = self.exec_cmd_array()
        print("host cmd result in thread:" + self.host.cmd_result)
    
    def exec_cmd_array(self) -> str:
        cmd_exec_result = ""
        for cmd in self.host.cmd_array:
            cmd_exec_result += self.exec_cmd(cmd)
        return cmd_exec_result
        
    def exec_cmd(self, cmd) -> str:
        # print_template = ("===================================================================\n时间: %s\n命令执行状态: %s\n命令执行结果: \n%s\n===================================================================\n")
        print_template = ("==============================================================\n时间: %s\n主机: %s\n命令执行状态: %s\n当前执行命令: %s\n命令执行结果: \n%s\n")
        result_str = ""
        
        cur_time = time.asctime()
        try:
            # TODO, set text color to red
            real_info = self.host.conn.send_command(cmd)
            result_str = print_template % (cur_time, self.host.ip, '执行成功', cmd, real_info)
        except Exception as e:
            cur_time = time.asctime()
            result_str = print_template % (cur_time, self.host.ip, '执行失败', cmd, '')
        return result_str

class SSHConnTestWorker(QThread):
    signal_ssh_connected = pyqtSignal(dict)
    
    def __init__(self, host):
        super(SSHConnTestWorker, self).__init__()
        self.host = host
        self.run = True
        
    def run(self):
        is_connected, host = self.try_connect()
        
        # ? 是否有必要加锁
        qmutex = QMutex()
        qmutex.lock() 
        if is_connected:
            self.host.status = True
        else:
            self.host.status = False
        qmutex.unlock()
        
    # 返回连接状态(bool)，连接句柄(conn)
    def try_connect(self):
        dev = {
            'device_type': 'linux',
            'username': self.host.username,
            'password': self.host.passwd,
            'port': 22,
            'host': self.host.ip,
        }
        print_template = ("==============================================================\n时间: %s\n命令执行状态: %s\n当前执行命令： %s\n命令执行结果: \n%s\n")
            
        try:
            ssh = Netmiko(**dev)
            # 保存ssh连接
            self.host.conn = ssh
            self.host.status = True
            
        except Exception as e:
            self.host.conn = None
            self.host.status = False
        
        return (self.host.status, self.host)
        
class HostInfoInput(Ui_host_info_input.Ui_Form, QWidget):
    host_ip = None
    host_passwd = None
    host_username = None
    
    # 发送添加主机信号
    signal_host_info_input_widget_add_host = pyqtSignal(str)
    
    # host_info_input widget的信号，接收子窗口传过来的IP，账号，密码
    signal_host_info_input_widget_data = pyqtSignal(dict)
    
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
        
        # 发送host_info
        self.signal_host_info_input_widget_data.emit(host_info)
        
        # 清空上一次输入的数据
        self.le_host_ip.setText('')
        self.le_host_username.setText('')
        self.le_host_passwd.setText('')
        
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
    ssh_conn_test_workers = list()
    ssh_cmd_exec_workers = list()
    cmd_results = str()
        
    
    signal_mainwindow_del_host = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.init_slot()
        
    def showProgregssDialog(self):
       # num = 10000
       num = 8000
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
        # 开启计时器，2秒后超时
        self.qtimer_ssh_conn_test_timeout = QTimer(self)
        self.qtimer_ssh_conn_test_timeout.start(2000)
        self.qtimer_ssh_conn_test_timeout.timeout.connect(self.update_ui_host)
        
        # 测试所有主机
        for i, host in enumerate(self.hosts):
            # init ssh woker
            self.ssh_conn_test_workers.append(SSHConnTestWorker(host))
            self.ssh_conn_test_workers[i].start()
        
        self.showProgregssDialog()
        self.btn_inspection.setEnabled(True)
        
    def btn_inspection_clicked(self):
        # self.qtimer_ssh_exec_timeout = QTimer()
        # self.qtimer_ssh_exec_timeout.start(1000)
        # self.qtimer_ssh_exec_timeout.timeout.connect(self.update_ui_cmd_result)
        
        cmd_array = list()
        te_cmd_input_data = self.te_cmd_input.toPlainText()
        
        for cmd in te_cmd_input_data.split('\n'):
            cmd_array.append(cmd)
            
        alive_hosts = [ alive_host for alive_host in self.hosts if alive_host.conn ]
        
                
        # 执行指令
        for i, host in enumerate(alive_hosts):
            self.hosts[i].cmd_array = cmd_array
            # init ssh woker
            self.ssh_cmd_exec_workers.append(SSHCmdExecWoker(host))
            self.ssh_cmd_exec_workers[i].start()
        
        time.sleep(0.5)
            
        # 输出
        for i, host in enumerate(alive_hosts):
            print("host cmd_result:" + host.cmd_result)
            self.cmd_results += host.cmd_result
        self.te_cmd_output.setText(self.cmd_results)
        # 清除上一次的记录
        self.cmd_results = ''
        
    def btn_about_clicked(self):
        AboutWidget().show()
        
    # top left side UI logic
    def btn_add_host_clicked(self):
        # 获取信号
        self.host_info_input.show()
    
    def btn_del_host_clicked(self):
        selected_items = self.tw_host_info.selectedItems()
        if not selected_items:
            return
        else:
            for i, host in enumerate(selected_items):
                selected_items = self.tw_host_info.selectedItems()[i].text()
                self.del_host(selected_items)
        self.signal_mainwindow_del_host.emit("done")
    
    def btn_undo_host_clicked(self):
        pass
    
    def btn_batch_host_import_clicked(self):
        fdlg = QFileDialog()
        fdlg.setFileMode(QFileDialog.FileMode.AnyFile)
        
        if fdlg.exec():
            #接受选中文件的路径，默认为列表
            filenames = fdlg.selectedFiles()
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
            f=open(filenames[0],'r')

            with f:
                #接受读取的内容，并显示到多行文本框中
                lines = f.readlines()
                for line in lines:
                    # min len of ip is 1.1.1.1
                    # no ip found
                    if len(line) < 7:
                        continue
                    
                    # clean the line
                    host_info = ''
                    for i, c in enumerate(line):
                        if c == '\n':
                            pass
                        # any other blank character, replace it with space
                        if c == '\t':
                            host_info += ' '
                        if c == '\n':
                            continue
                        else:
                            host_info += c
                        
                    ip = host_info.split(' ')[0]
                    username = host_info.split(' ')[1]
                    passwd = host_info.split(' ')[2]
                    
                    self.hosts.append(Host(ip=ip, username=username, passwd=passwd))
                    self.update_ui_host()
    
    def add_host(self, host_info):
        self.hosts.append(Host(ip=host_info['ip'], username=host_info['username'], passwd=host_info['passwd']))
        
        # 操作完成，发送信号
        self.host_info_input.signal_host_info_input_widget_add_host.emit("")

    def del_host(self, ip):
        for host in self.hosts:
            # 按照ip删除主机
            if host.ip == ip:
                self.hosts.remove(host)
        
    def get_all_hosts(self):
        for host in self.hosts:
            print("Host:%s\nUsername:%s\nPasswd:%s" % host.ip, host.username, host.passwd)
        
    def update_ui_cmd_result(self):
        print("result:" + self.cmd_results)
        self.te_cmd_output.setText(self.cmd_results)
    
    # UI更新部分
    # TODO text alignment
    def update_ui_host(self):
        # clear tablewidget
        for i in range(self.tw_host_info.rowCount()):
            self.tw_host_info.setItem(i, 0, QTableWidgetItem(''))
            self.tw_host_info.setItem(i, 1, QTableWidgetItem(''))
            self.tw_host_info.setItem(i, 2, QTableWidgetItem(''))
            self.tw_host_info.setItem(i, 3, QTableWidgetItem(''))
        
        # set tablewidget
        for i, host in enumerate(self.hosts):
            # ? why tablewidgetitem not show after set alignment
            # self.tw_host_info.setItem(i, 0, QTableWidgetItem(host.ip).
            #                           setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter))
            # self.tw_host_info.setItem(i, 1, QTableWidgetItem(host.username).
            #                           setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter))
            # self.tw_host_info.setItem(i, 2, QTableWidgetItem(host.passwd).
            #                           setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter))
            # if host.status == True:
            #     self.tw_host_info.setItem(i, 3, QTableWidgetItem("✔️").
            #                           setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter))
            # else:
            #     self.tw_host_info.setItem(i, 3, QTableWidgetItem("❌").
            #                           setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter))
            
            self.tw_host_info.setItem(i, 0, QTableWidgetItem(host.ip))
            self.tw_host_info.setItem(i, 1, QTableWidgetItem(host.username))
            self.tw_host_info.setItem(i, 2, QTableWidgetItem(host.passwd))
            if host.status == True:
                self.tw_host_info.setItem(i, 3, QTableWidgetItem("✔️"))
            else:
                self.tw_host_info.setItem(i, 3, QTableWidgetItem("❌"))
        
    def init_ui(self):
        # self.resize(1000, 1000)
        
        # 巡检按钮需要先通过连接性测试才能激活
        self.btn_inspection.setEnabled(False)
        # 设置固定窗口大小
        self.setFixedSize(self.width(), self.height())
        
        # table widget设置
        self.tw_host_info.setRowCount(10)
        self.tw_host_info.setColumnCount(4)
        
        # 禁止编辑
        self.tw_host_info.setEditTriggers(QAbstractItemView.EditTrigger.SelectedClicked)
        
        self.tw_host_info.setHorizontalHeaderLabels(['主机', '用户名', '密码', '状态'])
        # 扩展Header长度
        self.tw_host_info.horizontalHeader().setStretchLastSection(True)
        
        # 子窗口
        self.host_info_input = HostInfoInput()
        
        # tabwidget
        self.tab.setObjectName("IPS巡检")
        self.tab_2.setObjectName("堡垒机授权服务器")
        
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
        self.btn_conn_test.clicked.connect(lambda x: self.btn_conn_test_clicked())
        self.btn_inspection.clicked.connect(lambda x: self.btn_inspection_clicked())
        
        # 子窗口信号连接
        self.host_info_input.signal_host_info_input_widget_data.connect(lambda host_info: self.add_host(host_info))
        self.host_info_input.signal_host_info_input_widget_add_host.connect(lambda x: self.update_ui_host())
        self.signal_mainwindow_del_host.connect(lambda x: self.update_ui_host())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
    