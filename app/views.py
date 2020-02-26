from flask import render_template, flash, redirect, url_for
from app import app
from app import config
from .forms import LoginForm


@app.route('/')
def index():
    return render_template('index.html', title=config.title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        flash(
            'Login requested Username: {}, Password: {}'.format(username, password))
        print(flash)
        return redirect(url_for('index'))

    return render_template('login.html', title=config.title, form=form)
