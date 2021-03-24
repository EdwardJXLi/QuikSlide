from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def setup_db(app):
    with app.app_context():
        db.create_all()
