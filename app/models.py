from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import DB

class User(UserMixin, DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), nullable=False)
    email = DB.Column(DB.String(120), unique=True, nullable=False, index=True)
    password_hash = DB.Column(DB.String(255), nullable=False)
    created_at = DB.Column(DB.DateTime, default=datetime.utcnow)
    predictions = DB.relationship("Prediction", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Prediction(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    patient_name = DB.Column(DB.String(100), nullable=False)
    age = DB.Column(DB.Integer, nullable=False)
    gender = DB.Column(DB.String(20), nullable=False)
    symptoms = DB.Column(DB.Text, nullable=False)
    predicted_disease = DB.Column(DB.String(100), nullable=False)
    confidence = DB.Column(DB.Float, nullable=False)
    pathway = DB.Column(DB.Text, nullable=False)
    created_at = DB.Column(DB.DateTime, default=datetime.utcnow)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"), nullable=True)
