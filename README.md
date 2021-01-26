Добавлены базовые функции обмена клиента с сервером

Добавлено получение команды перезагрузки

Добавлено считывание данных с .env конфига или терминала

## Requirements

* Python3
* Flask
* pyusb
* cryptography
* requests

## Dependencies

    pip install -r requirements.txt


## TODO List:


* Безопасность данных при передаче

* Отправка буфера с помощью pyusb вместе с транзакцией

* Добавить тесты

* Написать документацию

* Добавить Timer  QThread/QtConcurrent::run(), чтобы процессы не замораживались