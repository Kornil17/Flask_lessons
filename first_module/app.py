from flask import Flask, render_template, url_for, request, flash, get_flashed_messages, session, redirect, abort
from settings import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.get_settings()['app']['key']
menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"}
]
@app.route('/')
def main():
    print(url_for('main'))
    return render_template('index.html', title='Flask Lessons', menu=menu)
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=menu)

@app.route('/login', methods=["POST", "GET"])
def login():
    print(request.method)
    if request.method == "GET" and 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'Dmitriy' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)
@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'{username}'
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404




# Тестовый контекст запроса
# with app.test_request_context():
#     print(url_for('main'))


if __name__ == '__main__':
    app.run(host='localhost', port=7777, debug=True)