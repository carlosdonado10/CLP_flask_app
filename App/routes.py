from flask import render_template
from app.Utils.utils import params
from app import app

@app.route('/')
@app.route('/index')
def index():
    params.update({'user': {'username': 'Larli'}})
    params.update({'posts': [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]})

    return render_template('index.html', params=params)
