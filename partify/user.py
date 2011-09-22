from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlalchemy import and_

from database import db_session
from models import User
from partify import app
from forms.user_forms import RegistrationForm
from forms.user_forms import LoginForm

@app.route('/register', methods=['GET'])
def register_form():
    """Presents a form for user registration.

    Form details are handed by the WTForm RegistrationForm."""
    form = RegistrationForm(request.form)
    return render_template("register.html", form=form)

@app.route('/register', methods=['POST'])
def register_post():
    """Processes input from the registration form and registers a new user."""
    # TODO: Store passwords as hashes and not as plaintext (issue #3).
    form = RegistrationForm(request.form)
    if form.validate():
        user = User(form.name.data, form.username.data, form.password.data)
        db_session.add(user)
        db_session.commit()
        session['user'] = dict((k, getattr(result, k)) for k in ('name', 'id', 'username'))
        return redirect(url_for('main'))
    else:
        return render_template("register.html", form=form)

@app.route('/login', methods=['GET'])
def login_form():
    """Presents a login WTForm."""
    form = LoginForm(request.form)
    return render_template("login.html", form=form)

@app.route('/login', methods=['POST'])
def login_post():
    """Reads input from the login form and performs the authentication."""
    form = LoginForm(request.form)
    if form.validate():
        result = User.query.filter(and_(User.username==form.username.data, User.password==form.password.data)).first()
        if result is not None:
            session['user'] = dict((k, getattr(result, k)) for k in ('name', 'id', 'username'))
        return redirect(url_for('main'))
    else:
        return render_template("login.html", form=form)

@app.route('/logout', methods=['GET'])
def logout():
    """Logs out the user."""
    session.pop('user', None)
    return redirect(url_for('main'))