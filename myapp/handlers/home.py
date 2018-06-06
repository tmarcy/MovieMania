from myapp import app
from flask import render_template


@app.route('/')
def homepage():
    handlers = [('search movie', '/search'),
                ('statistics', '/api/v1.0/statistics'),
                ('search list', '/api/v1.0/list')
                ]
    return render_template('home.html', handlers=handlers)