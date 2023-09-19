from sqlalchemy.sql import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://Zertalian:password@localhost:5432/testDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class University(db.Model):
    university_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    short_name = db.Column(db.String(10))
    date_of_creation = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.full_name}_{self.short_name}_{self.date_of_creation}"


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.Integer, db.ForeignKey("university.university_id"))
    FCs = db.Column(db.String(50))
    date_of_birth = db.Column()
    year_of_admission = db.Column()

    def __str__(self):
        return f"{self.FCs}_{self.date_of_birth}_{self.year_of_admission}_{self.university.id}"
