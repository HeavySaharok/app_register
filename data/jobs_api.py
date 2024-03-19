import flask
# Согласно архитектуре REST, обмен данными между клиентом и сервером осуществляется в формате JSON (реже — XML).
# Поэтому формат ответа сервера flask изменён с помощью метода jsonify, который преобразует наши данные в JSON.
from flask import request, jsonify

from data import db_session
from data.jobs import Jobs

# Механизм разделения приложения Flask на независимые модули
# Как правило, blueprint — логически выделяемый набор обработчиков адресов.
# Blueprint работает аналогично объекту приложения Flask, но в действительности он не является приложением.
blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify(
        {'jobs': [item.to_dict(only=('job', 'team_leader', 'work_size')) for item in jobs]})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    # Согласно REST, далее нужно реализовать получение информации об одной новости. Фактически, мы уже получили из списка
    # всю информацию о каждой новости. При проектировании приложений по архитектуре REST обычно поступают таким образом:
    # когда возвращается список объектов, он содержит только краткую информацию (например, только id и заголовок)...
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    # ...а полную информацию (текст и автора) можно посмотреть с помощью запроса, который мы обработаем далее.
    # Можно явно указать, какие именно поля оставить в получившемся словаре.
    return jsonify({'jobs': jobs.to_dict(only=('job', 'team_leader', 'work_size', 'collaborators', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    # Проверив, что запрос содержит все требуемые поля, мы заносим новую запись в базу данных.
    # request.json содержит тело запроса, с ним можно работать, как со словарем.
    db_sess = db_session.create_session()

    jobs = Jobs()
    jobs.job = request.json['job']
    jobs.team_leader = request.json['team_leader']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.is_finished = request.json['is_finished']
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_Jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

# @blueprint.route('/api/jobs/<int:jobs_id>', methods=['POST'])
# def edit_jobs(jobs_id):
#     if not request.json:
#         return jsonify({'error': 'Empty request'})
#     elif not any(key in request.json for key in
#                  ['job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     jobs = db_sess.query(Jobs).get(jobs_id)
#     if not jobs:
#         return jsonify({'error': 'Not found'})
#
#     jobs.job = request.json['job']
#     jobs.team_leader = request.json['team_leader']
#     jobs.work_size = request.json['work_size']
#     jobs.collaborators = request.json['collaborators']
#     jobs.is_finished = request.json['is_finished']
#     db_sess.commit()
#     return jsonify({'success': 'OK'})