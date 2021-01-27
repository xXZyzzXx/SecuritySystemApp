import os
from config import configs
from dotenv import load_dotenv
import json

from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_talisman import Talisman

from encrypt import encrypt_message, decrypt_message

app = Flask(__name__)
Talisman(app)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('status')
parser.add_argument('error')
parser.add_argument('transaction')


def decrypt_client_message(args):
    """
    Дешифрует сообщения в запросе с помощью ключа.

    :param args: аргументы запроса
    :return type=dict: дешифрованное сообщение
    """
    if args.key is not None:
        decrypt = decrypt_message(args.key.encode())
        message = json.loads(decrypt)
        return message


class Status(Resource):
    """Получает статус приложения"""
    def post(self, app_id):
        args = parser.parse_args()
        message = decrypt_client_message(args)
        if isinstance(message, dict) and 'status' in message:
            print(f'Статус приложения {app_id}: {message["status"]}')
            return 200


class Errors(Resource):
    """Получает ошибки из приложения"""
    def post(self, app_id):
        args = parser.parse_args()
        message = decrypt_client_message(args)
        if isinstance(message, dict) and 'error' in message:
            print(f'Ошибка в приложении {app_id}: {message["error"]}')


class Transaction(Resource):
    """Получает транзакцию из приложения, возвращает сообщение об успешной отправке"""
    def post(self, app_id):
        args = parser.parse_args()
        message = decrypt_client_message(args)
        if isinstance(message, dict) and 'transaction' in message:
            print(f'Получена транзакция от приложения {app_id}: {message["transaction"]}')
            command = {'command': 'Транзакция получена сервером'}  # 'Транзакция получена сервером'
            answer = {'key': encrypt_message(command)}
            return answer
        return None


class Alarm(Resource):
    """Получает сообщение об попытке взлома в приложении, возвращает команду перезагрузки"""
    def post(self, app_id):
        args = parser.parse_args()
        message = decrypt_client_message(args)
        if isinstance(message, dict) and 'alarm' in message:
            print(f'Получено предупреждение от приложения {app_id}: {message["alarm"]}')
            command = {'command': 'reload'}
            answer = {'key': encrypt_message(command)}
            return answer
        return None


api.add_resource(Status, '/api/status/<int:app_id>')
api.add_resource(Errors, '/api/error/<int:app_id>')
api.add_resource(Transaction, '/api/transaction/<int:app_id>')
api.add_resource(Alarm, '/api/alarm/<int:app_id>')
app.register_blueprint(api_bp)

if os.path.exists('.env'):
    load_dotenv('.env')

evn = os.environ.get('FLASK_ENV', 'default')

app.config.from_object(configs[evn])  # Получить значение FLASK_ENV и настроить конфигурацию

if __name__ == '__main__':
    app.run(port=8080)  # ssl_context='adhoc'
