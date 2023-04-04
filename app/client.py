import requests

# Регистариция пользователя:

# response = requests.post('http://127.0.0.1:5000/register/', json={'email': 'Ali@yndex.ru',
#                                                                  'password': 'Ali!@1234'})

# Вход:
#
# response = requests.post('http://127.0.0.1:5000/login/', json={'email': 'Ali@yndex.ru',
#                                                               'password': 'Ali!@1234'})
## Получение пользователя и всех его обьявлений по id:

# response = requests.get('http://127.0.0.1:5000/users/1/')

## Частичное изменение данных пользователя:

# response = requests.patch('http://127.0.0.1:5000/users/1/', json={'email_address': 'ali@gmai.com'},
#                           headers={'token': '4853d67a-cf79-4b79-87c6-22c51d961042'})
## Удаление пользователя:

# response = requests.delete('http://127.0.0.1:5000/users/1/', headers={'token': '4853d67a-cf79-4b79-87c6-22c51d961042'})

## Создание обьявления:

# response = requests.post('http://127.0.0.1:5000/ads/', json={'title': 'Разработчик Python',
#                                                             'description': 'Крутое резюме for Python', 'owner_id': 1},
#                          headers={'token': '4853d67a-cf79-4b79-87c6-22c51d961042'})
## Получение обьявления по id:

# response = requests.get('http://127.0.0.1:5000/ads/1/')

## Частичное изменение обьявления:

# response = requests.patch('http://127.0.0.1:5000/ads/1/', json={'description': 'Крутейшее резюме'},
#                           headers={'token': '4853d67a-cf79-4b79-87c6-22c51d961042'})
## Удаление обьявления:

# response = requests.delete('http://127.0.0.1:5000/ads/3/', headers={'token': '4853d67a-cf79-4b79-87c6-22c51d961042'})

print(response.status_code)
print(response.json())