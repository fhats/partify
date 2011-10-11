from flaskext.sqlalchemy import SQLAlchemy

from partify import app

db = SQLAlchemy(app)

def init_db():
    import partify.models
    db.create_all()
    
def reinit_db():
    global db

    db = SQLAlchemy(app)
    db.create_all()

if __name__ == "__main__":
    init_db()