from flask import render_template, flash, redirect, url_for, request, jsonify
from datetime import datetime
from application.Utils.CLP_Algorithm.volume_maximization import volume_maximization
from application.Utils.utils import params
from flask_login import current_user, login_user, logout_user, login_required
from json import loads, dumps
from werkzeug.urls import url_parse
from application.models import User, Dispatch, Post
from application import application, db
from urllib.parse import quote
from config import base_url


@application.route('/')
@application.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    dispatches = Dispatch.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST' and request.form.get('post') is not None:
        dispatch = Dispatch.query.filter_by(name=request.form.get('savedSchemas')).first()
        flash(request.form.get('savedSchemas'))
        if dispatch is not None:
            dispatch_id = dispatch.id
        else:
            dispatch_id = None

        post = Post(body=request.form.get('post'), user_id=current_user.id,
                    username=current_user.username, dispatch_id=dispatch_id)

        db.session.add(post)
        db.session.commit()

    params.update({'user': current_user})
    posts = current_user.followed_posts().all()
    print(posts)
    post_params = []
    for user, post, dispatch in posts:
        if dispatch is not None:
            post_params.append({"user_id": user.id,
                                "user_name": user.username,
                                "post_body": post.body,
                                "post_timestamp": post.timestamp,
                                "dispatch_name": dispatch.name,
                                "dispatch_body": base_url + '/results/' +
                                                    quote(dispatch.body.replace('$$$', '').replace('[', '/['))})
            print(post_params[-1]['dispatch_body'])
        else:
            post_params.append({"user_id": user.id,
                                "user_name": user.username,
                                "post_body": post.body,
                                "post_timestamp": post.timestamp})


    params.update({'posts': dumps(post_params, default=str)})
    # print(dispatches)
    return render_template('index.html', params=params, dispatches=dispatches)


@application.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@application.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    params = [{'author': user, 'body': post.body} for post in posts]

    if request.method == 'POST':
        if request.form.get('follow') is not None:
            current_user.follow(user)
            db.session.commit()
            flash(f'User: {user.username} followed successfully')
        elif request.form.get('unfollow') is not None:
            current_user.unfollow(user)
            db.session.commit()
            flash(f'User: {user.username} unfollowed successfully')

    return render_template('user.html', user=user, params=params)


@application.route('/follow/<username>')
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'user: {username} does not exist')
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}!')
    return redirect(url_for('user', username=username))


@application.route('/unfolow/<username>')
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User: {username} does not exist!')
        return redirect(url_for('index'))
    if username == current_user.username:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    else:
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are no longer following {username}')
        return redirect(url_for('user', username=username))


@application.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == "POST":
        if User.query.filter_by(username=request.form.get('username')).first() is not None:
            flash(f"Username: {request.form.get('username')} is already taken!")
        elif request.form.get('username') == current_user.username:
            flash("Your username did not change!")
        elif len(request.form.get('username')) == 0:
            flash("Empty username not allowed")
        else:
            current_user.username = request.form.get('username')
            current_user.about_me = request.form.get('about_me')
            db.session.commit()
            flash("Changes executed successfully!")
        # TODO: Mejorar lógica para poder cambiar solo un atributo
    return render_template('edit_profile.html', title='Edit Prodile')


@application.route('/container', methods=['POST', 'GET'])
@login_required
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
@login_required
def boxes(containerX, containerY, containerZ):
    params = {"containerX": containerX,
              "containerY": containerY,
              "containerZ": containerZ}
    if request.method == 'POST' and request.form.get('submit') is not None:
        containerParams = {"x1": 0,
                           "y1": 0,
                           "z1": 0,
                           "x2": float(containerX),
                           "y2": float(containerY),
                           "z2": float(containerZ)}

        results = request.form.to_dict()
        boxesParams = [{} for i in range(int(results.get('num_items')))]
        for key, itm in results.items():
            if key != "num_items" and key != 'submit':
                key_, idx = key.split("-")
                if key[:9] == "num_items":
                    boxesParams[int(idx)].update({key_: int(itm)})
                else:
                    boxesParams[int(idx)].update({key_: float(itm)})

        containerParams = dumps(containerParams)
        boxesParams = dumps(boxesParams)
        return redirect(url_for('results', container_params=containerParams, boxes_params=boxesParams))

    elif request.method == 'POST' and request.form.get('updateContainer') is not None:
        return redirect(url_for('boxes', containerX=request.form.get('contXupdate'),
                                containerY=request.form.get('contYupdate'), containerZ=request.form.get('contZupdate')))

    return render_template('boxes.html', params=params)


# TODO: Change orientations?
@application.route('/results/<container_params>/<boxes_params>', methods=['GET', 'POST'])
@login_required
def results(container_params, boxes_params):
    if request.method == "POST":
        favorite = Dispatch(name=request.form.get('fav-name'), description=request.form.get('fav-description'),
                            body=container_params + '$$$' + boxes_params, user_id=current_user.id)
        db.session.add(favorite)
        db.session.commit()

    params = {'container_params': container_params,
              'boxes_params': boxes_params}
    allocated_list, utilization, container, allocated_json = volume_maximization(problem_params=loads(boxes_params),
                                                                                 container_params=loads(
                                                                                     container_params))

    total_boxes = 400
    # max_iter = max(allocated_list, key=lambda x: x.iteration).iteration
    max_iter = 3
    return render_template('results.html', allocated_list=allocated_list, utilization=utilization, container=container,
                           total_boxes=total_boxes, boxes_params=boxes_params, params=params,
                           allocated_list_json=allocated_json,
                           max_iter=max_iter)


# Login Logic
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
@login_required
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


@application.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST' and request.form.get('search-value'):

        users = User.query.filter(User.username.like('%adm%'))

        return render_template('search.html', users=users.all(), search_value=request.form.get('search-value'))
    return redirect(url_for('index'))
