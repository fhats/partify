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

from flask import redirect, render_template, request, session, url_for

from partify import app
from partify.config import load_config_from_db
from partify.config import set_config_value
from partify.forms.admin_forms import ConfigurationForm
from partify.decorators import with_authentication, with_privileges
from partify.models import User
from partify.priv import dump_user_privileges

@app.route("/admin", methods=["GET"])
@with_authentication
@with_privileges(["ADMIN_INTERFACE"], "redirect")
def admin_console():
    user = User.query.get(session['user']['id'])

    form_object = dict( ( (k.lower(),v) for k,v in app.config.iteritems()) )

    configuration_form = ConfigurationForm(request.form, **form_object)

    return render_template("admin.html", 
        configuration_form=configuration_form, 
        user=user, 
        user_privs=dump_user_privileges(user))

@app.route("/admin", methods=["POST"])
@with_authentication
@with_privileges(["ADMIN_INTERFACE", "ADMIN_CONFIG"], "redirect")
def configuration_update():
    configuration_form = ConfigurationForm(request.form)
    
    if configuration_form.validate():
        for key,val in configuration_form.data.iteritems():
            key = key.upper()
            set_config_value(key, val)
        load_config_from_db()
        return redirect(url_for('admin_console'))
    else:
        return render_template("admin.html", 
            configuration_form=configuration_form, 
            user=User.query.get(session['user']['id']), 
            user_privs=dump_user_privileges(User.query.get(session['user']['id'])))
