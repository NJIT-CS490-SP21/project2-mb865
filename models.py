"""
This file creates the model for the database to use.
"""
from app import DB


class Player(DB.Model):
    """
    Model for Player in database.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    points = DB.Column(DB.Integer, default=100, nullable=False)

    def __repr__(self):
        return '<Player %r>' % self.username
