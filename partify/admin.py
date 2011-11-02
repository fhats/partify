from flask import render_template, session

from partify import app
from partify.decorators import with_authentication, with_privileges
from partify.models import User
from partify.priv import dump_user_privileges

@app.route("/admin", methods=["GET"])
@with_authentication
@with_privileges(["ADMIN_INTERFACE"], "redirect")
def admin_console():
    user = User.query.get(session['user']['id'])

    return render_template("admin.html", user=user, user_privs=dump_user_privileges(user))