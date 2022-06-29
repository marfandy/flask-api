from email.policy import default
from configs import db
from datetime import datetime


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    login = db.Column(db.Boolean, default=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    action = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


db.create_all()
