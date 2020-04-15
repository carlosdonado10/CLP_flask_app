from flask import render_template, flash, redirect, url_for, request, jsonify
from application.forms import ContainerParams, boxesParams, LoginForm, RegistrationForm
from application.Utils.CLP_Algorithm.volume_maximization import volume_maximization
from application.Utils.utils import params
from flask_login import current_user, login_user, logout_user, login_required
from json import loads, dumps
from werkzeug.urls import url_parse
from application.models import User, Dispatch
from application import application, db


@application.route('/')
@application.route('/index')
@login_required
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


@application.route('/container', methods=['POST', 'GET'])
def container():
    dispatches = Dispatch.query.filter_by(user_id=current_user.id)
    if request.method == "POST" and request.form.get('submitnew') is not None:
        flash('new')
        return redirect(url_for('boxes', containerX=request.form.get('containerX'),
                                containerY=request.form.get('containerY'), containerZ=request.form.get('containerZ')))
    elif request.method == "POST" and request.form.get('submitload') is not None:
        containerParams, boxesParams = request.form.get('savedSchemas').split('$$$')
        return redirect(url_for('results', container_params=containerParams, boxes_params=boxesParams))

    return render_template('container.html', dispatches=dispatches)


# TODO: Save info to pass to algorithm
@application.route('/boxes/<containerX>/<containerY>/<containerZ>', methods=['GET', 'POST'])
def boxes(containerX, containerY, containerZ):
    params = {"containerX": containerX,
              "containerY": containerY,
              "containerZ": containerZ}
    if request.method == 'POST':
        containerParams = {"x1": 0,
                            "y1": 0,
                            "z1": 0,
                            "x2": float(containerX),
                            "y2": float(containerY),
                            "z2": float(containerZ)}

        results = request.form.to_dict()
        boxesParams = [{} for i in range(int(results.get('num_items')))]
        flash(boxesParams)
        for key, itm in results.items():
            if key != "num_items":
                key_, idx = key.split("-")
                if key[:9] == "num_items":
                    boxesParams[int(idx)].update({key_: int(itm)})
                else:
                    boxesParams[int(idx)].update({key_: float(itm)})

        containerParams = dumps(containerParams)
        boxesParams = dumps(boxesParams)
        return redirect(url_for('results', container_params=containerParams, boxes_params=boxesParams))

    return render_template('boxes.html', params=params)


@application.route('/results/<container_params>/<boxes_params>', methods=['GET', 'POST'])
def results(container_params, boxes_params):
    if request.method == "POST":
        favorite = Dispatch(name=request.form.get('fav_name'),
                            body=container_params+'$$$'+boxes_params, user_id=current_user.id)
        db.session.add(favorite)
        db.session.commit()

    params = {'container_params': container_params,
              'boxes_params': boxes_params}
    allocated_list, utilization, container, allocated_json = volume_maximization(problem_params=loads(boxes_params),
                                                                 container_params=loads(container_params))

    total_boxes = 400
    # max_iter = max(allocated_list, key=lambda x: x.iteration).iteration
    max_iter=3
    return render_template('results.html', allocated_list=allocated_list, utilization=utilization, container=container,
                           total_boxes=total_boxes, boxes_params=boxes_params, params=params, allocated_list_json=allocated_json,
                           max_iter=max_iter)




# TODO: Change orientations?

#Login Logic

@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In')


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User(username=request.form.get('username'), email=request.form.get('email'))
        user.set_password(request.form.get('password1'))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('registration.html', title='Register')


