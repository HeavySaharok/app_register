from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Заголовок работы', validators=[DataRequired()])
    team_leader = TextAreaField("ID Тим лидера")
    work_size = IntegerField("Размер работы")
    collaborators = TextAreaField("Коллабораторы")
    is_finished = BooleanField("Работа завершена?")
    submit = SubmitField('Применить')
