from datetime import datetime
from backend import db

# Ignore column member errors
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    roles = db.Column(db.String(64))
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    #logs = db.relationship('Log', backref='uploader', lazy='dynamic')

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls,username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)
    
    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(140))
    driver = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr(self):
        return '<Log {}>'.format(self.file_name)