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
from partify import ipc
from partify.config import load_config_from_db
from partify.config import set_config_value
from partify.forms.admin_forms import ConfigurationForm, create_single_user_admin_admin_form
from partify.decorators import with_authentication, with_mpd, with_mpd_lock, with_privileges
from partify.models import User
from partify.player import _get_status
from partify.priv import dump_user_privileges, give_user_privilege, privs, revoke_user_privilege

@app.route("/admin", methods=["GET"])
@with_authentication
@with_privileges(["ADMIN_INTERFACE"], "redirect")
def admin_console():
    user = User.query.get(session['user']['id'])

    form_object = dict( ( (k.lower(),v) for k,v in app.config.iteritems()) )

    configuration_form = ConfigurationForm(request.form, **form_object)

    admin_admin_forms = create_admin_admin_form()
    user_ids_to_names = dict( (u.id, u.name) for u in User.query.all() )

    return render_template("admin.html",
        admin_admin_forms=admin_admin_forms,
        user_ids_to_names=user_ids_to_names,
        configuration_form=configuration_form, 
        user=user, 
        user_privs=dump_user_privileges(user))

@app.route("/admin/config_update", methods=["POST"])
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

@app.route("/admin/admin_admin_update", methods=["POST"])
@with_authentication
@with_privileges(["ADMIN_INTERFACE", "ADMIN_ADMIN"], "redirect")
def admin_admin_update():
    forms = create_admin_admin_form(request.form)

    for user_id, form in forms.iteritems():
        user = User.query.get(user_id)
        user_data = dict( (k[k.find("_")+1:].upper(),v) for k,v in form.data.iteritems())
        for priv, has_priv in user_data.iteritems():
            if has_priv:
                give_user_privilege(user, priv)
            else:
                revoke_user_privilege(user, priv)

    return redirect(url_for('admin_console'))

@app.route("/admin/playback/play")
@with_authentication
@with_mpd
@with_mpd_lock
@with_privileges(["ADMIN_INTERFACE", "ADMIN_PLAYBACK"], "redirect")
def admin_playback_play(mpd):
    ipc.update_desired_player_state("play", "play")
    mpd.play()

    return redirect(url_for('admin_console'))    

@app.route("/admin/playback/pause", methods=["GET"])
@with_authentication
@with_mpd
@with_privileges(["ADMIN_INTERFACE", "ADMIN_PLAYBACK"], "redirect")
def admin_playback_pause(mpd):
    ipc.update_desired_player_state("paused", "pause")
    mpd.pause()
    
    return redirect(url_for('admin_console'))    

@app.route("/admin/playback/skip", methods=["GET"])
@with_authentication
@with_mpd
@with_mpd_lock
@with_privileges(["ADMIN_INTERFACE", "ADMIN_PLAYBACK"], "redirect")
def admin_playback_skip(mpd):
    status = _get_status(mpd)
    rm_id = status['id']

    mpd.deleteid(rm_id)

    return redirect(url_for('admin_console'))

@app.route("/admin/queue/clear", methods=["GET"])
@with_authentication
@with_mpd
@with_mpd_lock
@with_privileges(["ADMIN_INTERFACE", "ADMIN_PLAYBACK"], "redirect")
def admin_queue_clear(mpd):
    mpd.clear()

    return redirect(url_for('admin_console'))    

def create_admin_admin_form(data=None):
    """Returns a list of SingleUserAdminAdminForms - one for each user."""

    users = User.query.all()
    forms = {}
    for user in users:
        form_type = create_single_user_admin_admin_form(user.id)
        form_obj = make_admin_admin_form_object(user)
        if data is None:
            form = form_type(**form_obj)
        else:
            form = form_type(data)
        forms[user.id] = form
    return forms

def make_admin_admin_form_object(user):
    user_form_obj = {}
    user_privs = dump_user_privileges(user)

    for key in privs.iterkeys():
        user_form_obj["%d_%s" % (user.id, key.lower())] = key in user_privs

    return user_form_obj
