from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration successful!", "success")
        models.User.create_user(
            username=form.username.data,
            password=form.password.data
        )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
            if not user.verify_password(form.password.data):
                return False
        except models.DoesNotExist:
            flash("Your username or password doesn't match!", "error")
        else:
            login_user(user)
            flash("You've been logged in!", "success")
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('index'))

@app.route('/taco', methods=('GET', 'POST'))
@login_required
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(
            user=g.user._get_current_object(),
            protein=form.protein.data.lower(),
            shell=form.shell.data.lower(),
            cheese=form.cheese.data,
            extras=form.extras.data.lower())
        flash("Taco added!", "success")
        return redirect(url_for('index'))
    return render_template('taco.html', form=form)

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='admin',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
