
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    gender = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    birthdate = db.Column(db.String(20))
    strengths = db.Column(db.JSON, default=list)
    weaknesses = db.Column(db.JSON, default=list)
    hobbies = db.Column(db.JSON, default=list)
    specialties = db.Column(db.JSON, default=list)
    part_time_jobs = db.Column(db.JSON, default=list)
    education = db.Column(db.JSON, default=list)
    certificates = db.Column(db.JSON, default=list)
    accounts = db.Column(db.JSON, default=dict)
    skills = db.Column(db.JSON, default=list)
    projects = db.relationship('Project', backref='owner', cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "user_id": self.user_id, "name": self.name, "email": self.email,
            "gender": self.gender, "phone_number": self.phone_number,
            "address": self.address, "birthdate": self.birthdate,
            "strengths": self.strengths, "weaknesses": self.weaknesses,
            "hobbies": self.hobbies, "specialties": self.specialties,
            "part_time_jobs": self.part_time_jobs, "education": self.education,
            "certificates": self.certificates, "accounts": self.accounts,
            "skills": self.skills,
            "projects": [project.to_dict() for project in self.projects]
        }

class Project(db.Model):
    project_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    link = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def to_dict(self):
         return {
            "project_id": self.project_id, "title": self.title,
            "description": self.description, "start_date": self.start_date,
            "end_date": self.end_date, "link": self.link,
            "user_id": self.user_id
        }
