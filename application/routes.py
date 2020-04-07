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


@application.route('/container', methods=['GET', 'POST'])
def container():
    form = ContainerParams()
    if form.validate_on_submit():
        flash(request.data.decode('utf-8'))
        return redirect(url_for('boxes', containerX=form.containerX.data,
                                containerY=form.containerY.data, containerZ=form.containerZ.data))

    return render_template('container.html', form=form)


# TODO: Save info to pass to algorithm
@application.route('/boxes/<containerX>/<containerY>/<containerZ>', methods=['GET', 'POST'])
def boxes(containerX, containerY, containerZ):
    form = boxesParams()
    if form.add_box.data:
        form.boxes.append_entry()
        return render_template('boxes.html', form=form)

    if form.favorites.data:
        container_params = {"x1": 0,
                            "y1": 0,
                            "z1": 0,
                            "x2": float(containerX),
                            "y2": float(containerY),
                            "z2": float(containerZ)}

        results = form.boxes.data
        boxes_params = []
        for bx in results:
            box_params = dict({"num_items": bx.get("num_boxes"),
                               "x": bx.get("boxX"),
                               "y": bx.get("boxY"),
                               "z": bx.get("boxZ")})
            boxes_params.append(box_params)

        d = Dispatch(
            name=form.fav_name.data,
            body=url_for('results', container_params=dumps(container_params), boxes_params=dumps(boxes_params)),
            user_id=current_user.id

        )
        db.session.add(d)
        db.session.commit()
        return render_template('boxes.html', form=form)

    if form.validate_on_submit():
        container_params = {"x1": 0,
                            "y1": 0,
                            "z1": 0,
                            "x2": float(containerX),
                            "y2": float(containerY),
                            "z2": float(containerZ)}

        results = form.boxes.data
        boxes_params = []
        for bx in results:
            box_params = dict({"num_items": bx.get("num_boxes"),
                              "x": bx.get("boxX"),
                              "y": bx.get("boxY"),
                              "z": bx.get("boxZ")})

            boxes_params.append(box_params)


        return redirect(url_for('results', container_params=dumps(container_params), boxes_params=dumps(boxes_params)))

    return render_template('boxes.html', form=form)


@application.route('/results/<container_params>/<boxes_params>')
def results(container_params, boxes_params):

    allocated_list, utilization, container = volume_maximization(problem_params=loads(boxes_params),
                                                                 container_params=loads(container_params))


    total_boxes = 400

    return render_template('results.html', allocated_list=allocated_list, utilization=utilization, container=container,
                           total_boxes=total_boxes)




# TODO: Change orientations?

#Login Logic

@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


