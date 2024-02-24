import os
import requests

from db_api import update_balance, select_by_id, drop, select_by_username


class User(object):
    """ Класс пользователя.
    По Т/З пользователей всего 5, и создавать новых мы не планируем, поэтому при инициализации объекта класса нужно
    передать в него существующий id (1-5). По id будет отправлен запрос в базу данных, который вернет актуальный баланс
    пользователя.

    Код помещенный в комментарии рабочий, он использовался при настройке класса. Так как он не нужен в продакшене, я
    его закомментировал.

    """

    def __init__(self, user_id):
        self.id = user_id
        # self.username = select_by_id(user_id)[1]
        self.balance = self.get_balance(self.id)

    # def __del__(self):
    #     drop(self.id)

    def get_id(self, user_id: int = None, username: str = None) -> int:
        if user_id:
            return select_by_id(self.id)[0]
        # if username:
        #     return select_by_username(self.username)[0]

    @staticmethod
    def get_balance(user_id: int) -> int | float:
        return select_by_id(user_id)[2]

    def update_user_balance(self, balance: int):
        self.balance = balance
        update_balance(balance=balance, id=self.id)

    def drop_user(self):
        drop(self.id)

    def __str__(self):
        return f"({self.id}, {self.balance})"


def fetch_weather(city: str = 'Moscow'):
    """ Функция принимает название города city и возвращает актуальную температуру в этом городе.
    :param city:
    :return:
    """
    api_key = os.getenv('API_KEY')
    url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={api_key}&q={city}"
    response = requests.get(url)
    load_data = response.json()

    if load_data['cod'] == '200':
        current_temp = load_data['list'][0]['main']['temp']
    else:
        return 'City not found'
    return kelvin_to_celsius(current_temp)


def kelvin_to_celsius(kelvin: int) -> float | int:
    """ Функция принимает температуру в кельвинах и возвращает в цельсиях"""
    return round(kelvin - 273.15, 2)
