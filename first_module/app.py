from flask import Flask, render_template, url_for, request, flash, get_flashed_messages, session, redirect, abort, make_response
from flask_login import LoginManager
from settings import Config
from database import WorkDb
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from user_login import UserLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.get_settings()['app']['key']
app.permanent_session_lifetime = timedelta(days=10)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().get_user(user_id)


@app.route('/')
def main():
    print(url_for('main'))
    return render_template('index.html', title='Flask Lessons', menu=WorkDb.get_menu(), posts=WorkDb.get_all_posts())
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form)
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=WorkDb.get_menu())

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET" and 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'Dmitriy' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=WorkDb.get_menu())

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['username']) >= 4 and len(request.form['email']) >= 4 \
            and len(request.form['password']) >= 4 and (request.form['password'] == request.form['repeat_password']):
            hash = generate_password_hash(request.form['password'])
            res = WorkDb.addUser(request.form['username'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for("login"))
            else:
                flash('Ошибка при добавлении пользователя в БД', category='error')
        else:
            flash('Неверно заполнены поля', category='error')

    return render_template('register.html', title='Регистрация', menu=WorkDb.get_menu())

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'{username}'

@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) >= 4:
            res = WorkDb.add_post(request.form['name'], request.form['message'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=WorkDb.get_menu(), title="Добавление статьи")

@app.route('/post/<int:id_post>')
def showPost(id_post):
    data = WorkDb.get_post(id_post)
    if not data:
        abort(404)
    title, post = data.title, data.text
    return render_template('post.html', menu=WorkDb.get_menu(), title=title, post=post)

@app.route('/test')
def test():
    res = make_response(render_template('index.html'))
    res.headers['Content-Type'] = 'text/html'
    return res, 200

@app.route('/set_cookie')
def set_cookie():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')
    res = make_response(f'Cookie авторизации:  {log}')
    res.set_cookie('logged', 'yes')
    return res

@app.route('/del_cookie')
def del_cookie():
    res = make_response('Вы больше не авторизованы')
    res.set_cookie('logged', '', 0)
    return res

@app.route('/session_cookie')
def session_cookie():
    session.permanent = False
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f"<h1>Main Page</h1><p>Число просмотров: {session['visits']}"

@app.route('/del_session_cookie')
def del_session_cookie():
    if 'visits' in session:
        del session['visits']
    return f"Seesion cookie очищены"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=WorkDb.get_menu()), 404




# Тестовый контекст запроса
# with app.test_request_context():
#     print(url_for('main'))


if __name__ == '__main__':
    app.run(host='localhost', port=7777, debug=True)