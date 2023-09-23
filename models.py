from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://Zertalian:password@localhost:5432/testDb'
app.config['SECRET_KEY'] = 'secret-key'
db = SQLAlchemy(app)


class University(db.Model):
    __tablename__ = 'university'
    university_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    short_name = db.Column(db.String(10))
    date_of_creation = db.Column(db.DateTime(), server_default=db.func.now())


class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.Integer, db.ForeignKey("university.university_id"))
    FCs = db.Column(db.String(50))
    date_of_birth = db.Column(db.DateTime(), default=datetime.utcnow)
    year_of_admission = db.Column(db.DateTime(), default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
