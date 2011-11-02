from partify.database import db
from partify.models import User

privs = {
    "ADMIN_CONFIG": 0x01,
    "ADMIN_PLAYBACK": 0x02,
    "ADMIN_ADMIN": 0x04,
    "ADMIN_INTERFACE": 0x08
}

def give_user_privilege(user, priv):
    """Given a user (either a User type or an ID) set the given privilege (identified by string) in the user's privilege list."""
    if not isinstance(user, User):
        user = User.query.get(user)
    # Set the appropriate bit in the user's privileges bitfield
    user.privs |= privs[priv]
    db.session.commit()

def revoke_user_privilege(user, priv):
    """Given a user (either a User type or an ID) remove the given privilege (identified by string) in the user's privilege list."""
    if not isinstance(user, User):
        user = User.query.get(user)
    user.privs &= (~privs[priv])
    db.session.commit()

def user_has_privilege(user, priv):
    if not isinstance(user, User):
        user = User.query.get(user)
    return user.privs & privs[priv] > 0

def dump_user_privileges(user):
    if not isinstance(user, User):
        user = User.query.get(user)
    return [p for p, v in privs.iteritems() if user.privs & v > 0]