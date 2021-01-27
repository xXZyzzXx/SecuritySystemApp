# -*- coding: utf-8 -*-
import os
import sys
import json
import traceback
import requests
from dotenv import load_dotenv

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

from encrypt import encrypt_message, decrypt_message


def post_data(url, data):
    """
    Шифрует сообщение, отправляет на указанный в url сервер и дешифрует ответ

    :param url: url-адрес
    :param data: данные для отправки post запроса
    :return: возвращает словарь с ответом от сервера
    """
    encrypted = encrypt_message(data)
    r = requests.post(url, data={"key": encrypted})
    answer = r.json()
    if isinstance(answer, dict) and 'key' in answer:
        decrypt = decrypt_message(answer['key'].encode())
        return json.loads(decrypt)


class MainWindowUI(object):

    def send_transaction(self):
        """
        Отправляет транзакцию на сервер, выводит полученный ответ
        """
        url = f"http://localhost:5000/api/transaction/{self.app_id}"
        transaction = {'transaction': {'user': 2}}
        answer = post_data(url, transaction)
        if isinstance(answer, dict) and 'command' in answer:
            print(f"Получена команда: {answer['command']}")
        else:
            print('Не поступило команды от сервера')

    def send_status(self):
        """
        Отправляет статус приложения на сервер каждое n-ное время
        """
        status = {'status': 'active'}
        url = f"http://localhost:5000/api/status/{self.app_id}"
        post_data(url, status)

    def send_alarm(self):
        """
        Отправляется на сервер в случае попытки взлома приложения,
        при получении команды 'reload' выводит полученную команду
        """
        alert = {'alert': 'caution'}
        url = f"http://localhost:5000/api/alarm/{self.app_id}"
        answer = post_data(url, alert)
        if isinstance(answer, dict) and 'command' in answer:
            if answer['command'] == 'reload':
                self.show_reload_messagebox(answer)
            else:
                print(f'Неизвестная команда: {answer["command"]}')
        else:
            print('Не поступило команды от сервера')

    def generate_error(self):
        """
        Вызывает исключение OSError для симуляции ошибки в приложении
        """
        raise OSError

    def upload_statistic(self):
        """
        Запускает функцию отправки статуса на сервер и обновляет счётчик запросов
        """
        self.send_status()
        self.lcs_value += 1
        print(f'Upload status count: {self.lcs_value}')
        self.lcdNumber.display(self.lcs_value)

    def start_upload(self):
        """
        Запускает таймер отправки статистики
        """
        self.upload_statistic()
        self.timer.start(10000)
        self.send_data_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def end_upload(self):
        """
        Приостанавливает таймер отправки статистики
        """
        self.timer.stop()
        self.send_data_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def show_reload_messagebox(self, answer):
        """
        Вызывает окно с уведомлением о перезагрузке
        """
        QtWidgets.QMessageBox.information(
            self.centralwidget,
            "Перезагрузка",
            f"Получена команда: {str(answer)}",
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 200)
        self.app_id = 758275
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(10, 20, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.status_label.setFont(font)
        self.status_label.setObjectName("label")
        self.errors_label = QtWidgets.QLabel(self.centralwidget)
        self.errors_label.setGeometry(QtCore.QRect(10, 80, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.errors_label.setFont(font)
        self.errors_label.setObjectName("label_2")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(410, 20, 64, 21))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(410, 80, 64, 21))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.send_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_data_button.setGeometry(QtCore.QRect(210, 20, 75, 23))
        self.send_data_button.setObjectName("pushButton_1")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(300, 20, 75, 23))
        self.stop_button.setObjectName("pushButton_2")
        self.transaction_button = QtWidgets.QPushButton(self.centralwidget)
        self.transaction_button.setGeometry(QtCore.QRect(20, 140, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.transaction_button.setFont(font)
        self.transaction_button.setObjectName("pushButton_3")
        self.error_button = QtWidgets.QPushButton(self.centralwidget)
        self.error_button.setGeometry(QtCore.QRect(150, 140, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.error_button.setFont(font)
        self.error_button.setObjectName("pushButton_4")
        self.alarm_button = QtWidgets.QPushButton(self.centralwidget)
        self.alarm_button.setGeometry(QtCore.QRect(330, 140, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.alarm_button.setFont(font)
        self.alarm_button.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.lcs_value = 0
        self.lcs_errors = 0
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.upload_statistic)

        self.send_data_button.clicked.connect(self.start_upload)
        self.stop_button.clicked.connect(self.end_upload)
        self.transaction_button.clicked.connect(self.send_transaction)
        self.error_button.clicked.connect(self.generate_error)
        self.alarm_button.clicked.connect(self.send_alarm)

        self.stop_button.setEnabled(False)
        # self.start_upload()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Клиент SecurityApp"))
        self.status_label.setText(_translate("MainWindow", "Статус приложения"))
        self.errors_label.setText(_translate("MainWindow", "Ошибки во время работы"))
        self.send_data_button.setText(_translate("MainWindow", "Отправлять"))
        self.stop_button.setText(_translate("MainWindow", "Прекратить"))
        self.transaction_button.setText(_translate("MainWindow", "Транзакция"))
        self.error_button.setText(_translate("MainWindow", "Симуляция ошибки"))
        self.alarm_button.setText(_translate("MainWindow", "Симуляция взлома"))


def send_error(application, tb):
    """
    Отправляет сообщение об ошибке в приложении

    :param application: Ui_MainWindow class
    :param str tb: Сообщение об ошибке (traceback)
    """
    error = {'error': tb}
    url = f"http://localhost:5000/api/error/{application.app_id}"
    answer = post_data(url, error)
    if isinstance(answer, dict) and 'command' in answer:
        print(answer['command'])


def excepthook(exc_type, exc_value, exc_tb):
    """
    Прослушивает приложение на наличие ошибок

    :param exc_type: OSError type
    :param exc_value: OSError value
    :param exc_tb: Traceback from error handler
    """
    ui.lcs_errors += 1
    ui.lcdNumber_2.display(ui.lcs_errors)
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)
    send_error(ui, tb=tb)
    # QtWidgets.QApplication.quit()  # завершить событие


if os.path.exists('.env'):
    load_dotenv('.env')

crypt_key = os.environ.get('CRYPT_KEY')

if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
