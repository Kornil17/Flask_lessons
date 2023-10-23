import sqlite3
import os
from flask import Flask, render_template, request, g

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
    return render_template('index.html', menu=[])

@site.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()

if __name__ == "__main__":
    site.run(debug=True)
