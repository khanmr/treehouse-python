from flask import Flask, render_template, flash, g, redirect, url_for, request
#, abort

from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user)

from peewee import DoesNotExist

import models
import forms

DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'abcedfghijklmnopqrstuvwxyz0123456789'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


# index
@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)


# login
@app.route('/login', methods=('Get', 'Post'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password,
                                   form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match", "error")

    return render_template('login.html', form=form)

# logout


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('index'))

# register


@app.route('/register', methods=('Get', 'Post'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            models.User.create_user(
                email=form.email.data,
                password=form.password.data,
                admin=True)
            print("User {} created".format(form.email.data))
        except ValueError:
            flash("User {} already exists".format(form.email.data))
        else:
            flash("User {} created".format(form.email.data))
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

# taco


@app.route('/taco', methods=('Get', 'Post'))
@login_required
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        # try:
        models.Taco.create(
            user=g.user._get_current_object(),
            protein=form.protein.data.lower(),
            shell=form.shell.data.lower(),
            cheese=form.cheese.data,
            extras=form.extras.data.lower())
        return redirect(url_for('index'))
        # except:
        #    flash("Taco create failed", "error")
    elif request.method == 'POST':
        flash("Taco form NOT valid", "warning")
    return render_template('taco.html', form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        # with models.DATABASE.transaction():
        models.User.create_user(
            email='chris.freeman.pdx@gmail.com',
            password='password',
            admin=True)
        print("admin 'chrisfreeman' created")
    except ValueError:
        admin = models.User.get(models.User.email ==
                                'chris.freeman.pdx@gmail.com')
        print("admin 'chrisfreeman' exist")
    app.run(debug=DEBUG, host=HOST, port=PORT)
