from flask import render_template as flask_render_template, request
from flask import flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, config, db
from .forms import LoginForm, RegisterForm, EditProfileForm, PostForm
from .models import User, Post
from datetime import datetime


def render_template(template_name, **content):
    content['title'] = content.get('title', config.title)
    return flask_render_template(template_name, **content)

def paginate(followed_posts, page):
    return followed_posts.paginate(
        page, config.posts_per_page, False)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = paginate(current_user.followed_posts(), page)
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    return render_template(
        'index.html', title=config.title, form=form,
        posts=posts.items, prev_url=prev_url, next_url=next_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = paginate(Post.query.order_by(Post.timestamp.desc()), page)
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    return render_template(
        'index.html', title=config.title,
        posts=posts.items, prev_url=prev_url, next_url=next_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=remember)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = paginate(user.followed_posts(), page)
    prev_url = url_for('user', username=username, page=posts.prev_num) if posts.has_prev else None
    next_url = url_for('user', username=username, page=posts.next_num) if posts.has_next else None
    return render_template(
        'user.html', title=config.title, user=user,
        posts=posts.items, prev_url=prev_url, next_url=next_url)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    elif user == current_user:
        flash('User {} not found.'.format(username))
    else:
        flash('You are following {}!'.format(username))
        current_user.follow(user)
        db.session.commit()
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    elif user == current_user:
        flash('User {} not found.'.format(username))
    else:
        flash('You are following {}!'.format(username))
        current_user.unfollow(user)
        db.session.commit()
    return redirect(url_for('user', username=username))
