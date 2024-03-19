from requests import get, post, delete

# print(get('http://localhost:5000/api/v2/users').json())
# print(get('http://localhost:5000/api/v2/users/2').json())
# print(get('http://localhost:5000/api/v2/users/52').json())  # нет такой новости
# print(get('http://localhost:5000/api/v2/users/q').json())  # не число

# print(post('http://localhost:5000/api/v2/users').json())  # нет словаря
# print(post('http://localhost:5000/api/v2/users', json={'surname': 'Sonya'}).json())  # не все поля
print(post('http://localhost:5000/api/v2/users', json={'surname': 'MISTER',
                                                       'name': "ZVER`",
                                                       'age': 2,
                                                       'position': 'kurilka',
                                                       'speciality': 'Sralker',
                                                       'address': 'Zona',
                                                       'email': 'shoha@ashan.sky',
                                                       'hashed_password': 'hunt_natura1s'}))
#
# print(delete('http://localhost:5000/api/v2/users/999').json())  # id = 999 нет в базе
print(delete('http://localhost:5000/api/v2/users/3').json())