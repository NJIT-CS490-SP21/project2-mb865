from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    points = db.Column(db.Integer, default=100, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.username
