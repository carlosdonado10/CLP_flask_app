from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import ContainerParams, boxesParams, LoginForm
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

# TODO: Finish login logic
@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested')
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In', form=form)


@app.route('/container', methods=['GET', 'POST'])
def loading():
    form = ContainerParams()
    if form.validate_on_submit():
        flash(request.data.decode('utf-8'))
        return redirect(url_for('boxes', containerX=form.containerX.data,\
                                containerY=form.containerY.data, containerZ=form.containerZ.data))

    return render_template('container.html', form=form)


# TODO: Save info to pass to algorithm
@app.route('/boxes/<containerX>/<containerY>/<containerZ>', methods=['GET', 'POST'])
def boxes(containerX, containerY, containerZ):
    form = boxesParams()
    if form.validate_on_submit():
        container_params={}
        container_params['x1'] = 0
        container_params['y1'] = 0
        container_params['z1'] = 0
        container_params['x2'] = containerX
        container_params['y2'] = containerY
        container_params['z2'] = containerZ
        flash(':)')
        flash(request.data.decode('utf-8'))

    return render_template('boxes.html', form=form)

# TODO: Change orientations?
