import os

from utils import fetch_weather, User

from flask_caching import Cache
from flask import Flask, render_template

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

app = Flask("task_python_developer")
app.secret_key = os.getenv('SECRET_KEY')
cache.init_app(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='Страница не найдена'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', message='Измени айди юзера (1-5) или город'), 500


@app.route('/')
@app.route('/<userId>/<city>')
def dev(userId: int, city: str):
    """ Функция представления данных из базы по GET запросу
    На вход подаются userId и city через GET запрос. Далее инициализируется пользователь через класс, где получает
    данные о себе из базы данных. Проверяется значение температуры города их кэша, и если его нет, то записывается
    новое значение. Далее происходит проверка на положительный баланс, и если он таков, то делаем запрос к базе данных
    на обновление баланса пользователя. В обратном случае выводим предупреждение. Таким образом баланс не станет
    отрицательным.
    
    """
    user = User(userId)
    current_balance = user.balance

    current_temp = cache.get(city)
    if not current_temp:
        data = fetch_weather(city)
        cache.set(city, data, 600)
        current_temp = data

    view_balance = round(current_balance + current_temp, 2)

    if view_balance >= 0:
        user.update_user_balance(balance=view_balance)
        data = {'userId': userId, 'balance': view_balance, 'current_temp': current_temp}
    else:
        data = 'Ваш баланс не может быть отрицательным, измените город!'
    return render_template('home.html', data=data)

# if __name__ == '__main__':
#     db_init()
#     app.run(debug=True, host='0.0.0.0')
