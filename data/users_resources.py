from flask import jsonify, make_response
from flask_restful import abort, Resource
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User
from data.reqparse import parser


def abort_if_news_not_found(user_id):  # вместо @app.errorhandler(404)
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        # Функция abort генерирует HTTP-ошибку с нужным кодом и возвращает ответ в формате JSON
        abort(404, message=f"User {user_id} not found")


# Для каждого ресурса (единица информации в REST называется ресурсом: новости, пользователи и т. д.) создается
# два класса: для одного объекта и для списка объектов: здесь это UserResource и UserListResource соответственно.
def set_password(password):
    return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 'name', 'age', 'email'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    #     get и post - без аргументов.
    #     Доступ к данным, переданным в теле POST-запроса - парсинг аргументов (reqparse)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user=User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.hashed_password = set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
