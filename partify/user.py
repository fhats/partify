"""Copyright 2011 Fred Hatfull

This file is part of Partify.

Partify is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Partify is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Partify.  If not, see <http://www.gnu.org/licenses/>."""

from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from models import User
from partify import app
from partify.decorators import with_authentication
from partify.priv import dump_user_privileges
from partify.priv import give_user_privilege
from partify.priv import privs
from forms.user_forms import RegistrationForm
from forms.user_forms import LoginForm
from forms.user_forms import SettingsForm

@app.route("/account_settings", methods=['GET'])
@with_authentication
def account_settings_page():
    user = User.query.get(session['user']['id'])
    form = SettingsForm(name=user.name)

    return render_template("account_settings.html", user=user, form=form, user_privs=dump_user_privileges(user))

@app.route("/account_settings", methods=['POST'])
@with_authentication
def account_settings_update():
    user = User.query.get(session['user']['id'])
    form = SettingsForm(request.form)

    if form.validate():
        user.name = form.name.data
        if form.current_password.data != "" and form.new_password.data != "":
            if check_password_hash(user.password, form.current_password.data):
                user.password = generate_password_hash(form.new_password.data)
    
    db.session.commit()

    return redirect(url_for('account_settings_page'))

@app.route('/register', methods=['GET'])
def register_form():
    """Presents a form for user registration.

    Form details are handed by the WTForm RegistrationForm."""
    form = RegistrationForm(request.form)
    return render_template("register.html", form=form)

@app.route('/register', methods=['POST'])
def register_post():
    """Processes input from the registration form and registers a new user."""
    form = RegistrationForm(request.form)
    if form.validate():
        user = User(form.name.data, form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user'] = dict((k, getattr(user, k)) for k in ('name', 'id', 'username'))
        if User.query.count() == 1:
            # If there's only one user in the database at this point (i.e. this is the first user in the DB), then give that user administrative rights.
            for priv in privs:
                give_user_privilege(user, priv)
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
        result = User.query.filter((User.username==form.username.data)).first()
        if result is not None and check_password_hash(result.password, form.password.data):
            session['user'] = dict((k, getattr(result, k)) for k in ('name', 'id', 'username'))
        return redirect(url_for('main'))
    else:
        return render_template("login.html", form=form)

@app.route('/logout', methods=['GET'])
def logout():
    """Logs out the user."""
    session.pop('user', None)
    return redirect(url_for('main'))