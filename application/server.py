import os
from config import configs
from dotenv import load_dotenv
import json

from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse

from encrypt import encrypt_message, decrypt_message

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('status')
parser.add_argument('error')
parser.add_argument('transaction')


class Status(Resource):
    def post(self, app_id):
        args = parser.parse_args()
        print(f'Статус приложения {app_id}: {args.status}')
        answer = {}
        return answer


class Errors(Resource):
    def post(self, app_id):
        args = parser.parse_args()
        print(f'Ошибка в приложении {app_id}: {args.error}')
        answer = {}
        return answer


class Transaction(Resource):
    def post(self, app_id):
        args = parser.parse_args()
        answer = {}
        if args.key is not None:
            decrypt = decrypt_message(args.key.encode())
            message = json.loads(decrypt)
            if message and 'transaction' in message:
                print(f'Получена транзакция от приложения {app_id}: {message["transaction"]}')
                command = {'command': 'Транзакция получена сервером'}
                answer = {'key': encrypt_message(command)}
        print(type(answer), answer)
        return answer


class Alarm(Resource):
    def post(self, app_id):
        print(f'Попытка взлома в приложении {app_id}, перезагрузить систему')
        answer = {'command': 'reload'}
        return answer


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
    app.run()  # ssl_context='adhoc'
