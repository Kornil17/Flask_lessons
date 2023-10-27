import datetime
import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, make_response, session, redirect, url_for
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin

# config
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "fddb73b6a9a16cad6ab975862ec77ee2b40a070d"
site = Flask(__name__)
site.config.from_object(__name__)
login_manager = LoginManager(site)

site.config.update(dict(DATABASE=os.path.join(site.root_path, 'flsite.db')))
# session.permanent_session_lifetime = datetime.timedelta(seconds=10)
dbase = None

@site.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

def connect_db():
    conn = sqlite3.connect(site.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with site.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
def get_db():
    if not hasattr(g, 'link.db'):
        g.link_db = connect_db()
    return g.link_db

@site.route("/")
def index():
    for i in dbase.getMenu():
        print(i)
    return render_template('index2.html', examples=dbase.getMenu(), posts=dbase.getPostAnonce())

@site.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return  render_template('add_post.html', examples=dbase.getMenu(), title="Добавление статьи")

@site.route("/posts/<int:id>")
@login_required
def showPost(id):
    title, post = dbase.getPost(id)
    print(dbase.getPost(id))
    if not title:
        abort(404)
    return render_template('post.html', examples=dbase.getMenu(), title=title, post=post)

@site.route("/cookies")   # cookies
def cookies():
    log = ''
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')
    res = make_response(f"<h1>Форма авторизации</h1><p>logged: {log}")
    res.set_cookie("logged", "yes", 30*24*3600)
    return res
@site.route("/logout")
def logout_cookies():
    res = make_response("<p>Вы больше не авторизованы</p>")
    res.set_cookie("logged", "", 0)
    return res

@site.route("/login")
def login():
    return render_template('login2.html', examples=dbase.getMenu(), title='Login')
@site.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Success register", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template('register.html', examples=dbase.getMenu(), title='Register')

@site.route("/sessions") # sessions
def sessions():
    print(session)
    session.permanent = True
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    session.modified = True
    return f"<h1>Session Page</h1><p>Число посещений: {session['visits']}"

@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, dbase)
@site.route("/login2", methods=["POST", "GET"])
def login2():
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('index'))
        flash("Bad passsword or email", "error")
    return render_template("login.html", examples=dbase.getMenu(), title="Autorization")

@site.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == "__main__":
    site.run(debug=True)
