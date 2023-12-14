from app import db
import datetime

# Association table for many-to-many relationship between Users and Groups
user_group_association = db.Table('user_group_association',
                                  db.Column('user_id', db.Integer,
                                            db.ForeignKey('users.id')),
                                  db.Column('group_id', db.Integer,
                                            db.ForeignKey('groups.id')))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))
    firstName = db.Column(db.String(500))
    secondName = db.Column(db.String(500))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    squat = db.Column(db.Integer)
    bench = db.Column(db.Integer)
    deadlift = db.Column(db.Integer)
    profile_image = db.Column(db.String(20), nullable=False,
                              default='default.png')

    # Correcting the relationship definition
    groups = db.relationship('Groups', secondary=user_group_association,
                             back_populates='users')


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(500), unique=True)
    groupBio = db.Column(db.String(1000))

    # Correcting the relationship definition
    users = db.relationship('Users', secondary=user_group_association,
                            back_populates='groups')
