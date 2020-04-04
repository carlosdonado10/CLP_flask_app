from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import ContainerParams, boxesParams, LoginForm
from app.Utils.CLP_Algorithm.volume_maximization import volume_maximization
from app.Utils.utils import params
from json import loads, dumps
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
        return redirect(url_for('boxes', containerX=form.containerX.data,
                                containerY=form.containerY.data, containerZ=form.containerZ.data))

    return render_template('container.html', form=form)


# TODO: Save info to pass to algorithm
@app.route('/boxes/<containerX>/<containerY>/<containerZ>', methods=['GET', 'POST'])
def boxes(containerX, containerY, containerZ):
    form = boxesParams()
    if form.add_box.data:
        form.boxes.append_entry()
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


        return redirect(url_for('results', container_params=container_params, boxes_params=boxes_params))

    return render_template('boxes.html', form=form)


@app.route('/results/<container_params>/<boxes_params>')
def results(container_params, boxes_params):
    all_list, utilization = volume_maximization(problem_params=boxes_params, container_params=container_params)
    flash(utilization)
    return render_template('results.html')


# TODO: Change orientations?
