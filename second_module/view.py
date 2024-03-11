from flask import render_template, url_for, request

from app import app
from config import Configuration

app.config['SECRET_KEY'] = Configuration.SecretKey

@app.route('/')
def index():
    print(request.endpoint)
    return render_template('base.html', methods_name='posts.index')

