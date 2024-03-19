import pprint
from requests import get, post, delete

pprint.pprint(get('http://localhost:5000/api/jobs').json())  # проверка
print(delete('http://localhost:5000/api/jobs/999').json())  # id = 999 нет в базе
print(post('http://localhost:5000/api/jobs/1').json())  # всё нормально
