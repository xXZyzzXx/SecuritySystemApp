# -*- coding: utf-8 -*-
import sys
import traceback
import requests

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QEventLoop


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 200)
        self.app_id = 758275
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(410, 20, 64, 21))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(410, 80, 64, 21))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(210, 20, 75, 23))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 140, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 140, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(330, 140, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.lcs_value = 0
        self.lcs_errors = 0
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.upload_statistic)

        self.pushButton_1.clicked.connect(self.start_upload)
        self.pushButton_2.clicked.connect(self.end_upload)
        self.pushButton_3.clicked.connect(self.send_transaction)  # self.generate_error
        self.pushButton_4.clicked.connect(self.generate_error)
        self.pushButton_5.clicked.connect(self.send_alarm)

        self.pushButton_2.setEnabled(False)
        # self.start_upload()

    def generate_error(self):
        raise OSError

    def send_transaction(self):
        transaction = {'transaction': {'amount': 50}}
        url = f"http://localhost:5000/api/transaction/{self.app_id}"
        r = requests.post(url, data=transaction)
        answer = r.json()
        if 'command' in answer:
            print(answer['command'])
        else:
            print(answer)

    def send_status(self):
        status = {'status': 'active'}
        url = f"http://localhost:5000/api/status/{self.app_id}"
        r = requests.post(url, data=status)
        answer = r.json()
        if 'command' in answer:
            print(answer['command'])

    def send_alarm(self):
        alert = {'alert': 'active'}
        url = f"http://localhost:5000/api/alarm/{self.app_id}"
        r = requests.post(url, data=alert)
        answer = r.json()
        if 'command' in answer:
            if answer['command'] == 'reload':
                print(str(answer))
                QtWidgets.QMessageBox.information(
                    self.centralwidget,
                    "Перезагрузка",
                    f"Получена команда: {str(answer)}",
                    QtWidgets.QMessageBox.Ok,
                    QtWidgets.QMessageBox.Ok)
            else:
                print(f'Неизвестная команда: {answer["command"]}')
        else:
            print('Не поступило команды от сервера')

    def upload_statistic(self):
        self.send_status()
        self.lcs_value += 1
        print(f'Upload status count: {self.lcs_value}')
        self.lcdNumber.display(self.lcs_value)

    def start_upload(self):
        # self.dataCollectionThread = DataCaptureThread()
        # self.dataCollectionThread.start()
        self.upload_statistic()
        self.timer.start(10000)
        self.pushButton_1.setEnabled(False)
        self.pushButton_2.setEnabled(True)

    def end_upload(self):
        # self.dataCollectionThread.terminate()
        self.timer.stop()
        self.pushButton_1.setEnabled(True)
        self.pushButton_2.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Клиент SecurityApp"))
        self.label.setText(_translate("MainWindow", "Статус приложения"))
        self.pushButton_3.setText(_translate("MainWindow", "Транзакция"))
        self.label_2.setText(_translate("MainWindow", "Ошибки во время работы"))
        self.pushButton_1.setText(_translate("MainWindow", "Отправлять"))
        self.pushButton_2.setText(_translate("MainWindow", "Прекратить"))
        self.pushButton_4.setText(_translate("MainWindow", "Симуляция ошибки"))
        self.pushButton_5.setText(_translate("MainWindow", "Симуляция взлома"))


def send_error(application, error):
    error = {'error': error}
    url = f"http://localhost:5000/api/error/{application.app_id}"
    r = requests.post(url, data=error)
    answer = r.json()
    if 'command' in answer:
        print(answer['command'])


def excepthook(exc_type, exc_value, exc_tb):
    ui.lcs_errors += 1
    ui.lcdNumber_2.display(ui.lcs_errors)
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
    send_error(ui, error=tb)
    # QtWidgets.QApplication.quit()  # завершить событие


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


''' Необходимо перенести Timer в QThread, чтобы не замерзал GUI
class Thread(QThread):
    _signal = pyqtSignal()

    def __init__(self):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self._signal.emit()


class DataCaptureThread(QThread):
    def collectProcessData(self):
        ui.send_status()

    def __init__(self, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.dataCollectionTimer = QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(self.collectProcessData)

    def run(self):
        self.dataCollectionTimer.start(1000)
        loop = QEventLoop()
        loop.exec_()
'''
