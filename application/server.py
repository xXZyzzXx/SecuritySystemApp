from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
parser = reqparse.RequestParser()
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
        print(f'Получена транзакция от приложения {app_id}: {args.transaction}')
        answer = 'Транзакция получена сервером'
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

if __name__ == '__main__':
    app.run(debug=True)

