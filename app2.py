import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

# config
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = "fddgkljklj123"

site = Flask(__name__)
site.config.from_object(__name__)

site.config.update(dict(DATABASE=os.path.join(site.root_path, 'flsite.db')))


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
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index2.html', examples=dbase.getMenu())

@site.route("/add_post", methods=["POST", "GET"])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка добавления статьи", category="error")
    return  render_template('add_post.html', examples=dbase.getMenu(), title="Добавление статьи")

@site.route("/posts/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', examples=dbase.getMenu(), title=title, post=post)



@site.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == "__main__":
    site.run(debug=True)
