from app.db import db

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(60))
    link = db.Column(db.String(255))

    def __repr__(self):
        return '<Project %r, name: %r, owner: %r>' % (self.id, self.name, self.owner)
