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
