from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
db = SQLAlchemy()
class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   doc="Auto-incremented unique patient record ID")
    name = db.Column(db.String(100), nullable=False, default='Anonymous',
                     doc="Patient's name (optional, defaults to Anonymous)")
    age      = db.Column(db.Integer,  nullable=False, doc="Age in years")
    sex      = db.Column(db.Integer,  nullable=False, doc="Sex: 1=male, 0=female")
    cp       = db.Column(db.Integer,  nullable=False, doc="Chest pain type: 0-3")
    trestbps = db.Column(db.Float,    nullable=False, doc="Resting blood pressure (mmHg)")
    chol     = db.Column(db.Float,    nullable=False, doc="Serum cholesterol (mg/dl)")
    fbs      = db.Column(db.Integer,  nullable=False, doc="Fasting blood sugar > 120 mg/dl")
    restecg  = db.Column(db.Integer,  nullable=False, doc="Resting ECG result: 0-2")
    thalach  = db.Column(db.Float,    nullable=False, doc="Maximum heart rate achieved")
    exang    = db.Column(db.Integer,  nullable=False, doc="Exercise induced angina: 1=yes")
    oldpeak  = db.Column(db.Float,    nullable=False, doc="ST depression (exercise vs rest)")
    slope    = db.Column(db.Integer,  nullable=False, doc="Slope of peak exercise ST segment")
    ca       = db.Column(db.Integer,  nullable=False, doc="Major vessels colored by fluoroscopy (0-4)")
    thal     = db.Column(db.Integer,  nullable=False, doc="Thalassemia type (0-3)")
    prediction = db.Column(
        db.Integer, nullable=False,
        doc="ML model output: 1=Heart Disease predicted, 0=No Heart Disease"
    )
    risk_score = db.Column(
        db.Float, nullable=False,
        doc="Probability of heart disease (0.0 to 1.0)"
    )
    risk_level = db.Column(
        db.String(10), nullable=False,
        doc="Risk category: LOW, MODERATE, or HIGH"
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc),
        doc="UTC timestamp when the prediction was made"
    )
    def __repr__(self):
        return (
            f"<Patient id={self.id} name='{self.name}' "
            f"age={self.age} risk_level='{self.risk_level}'>"
        )
    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "age":      self.age,
            "sex":      self.sex,
            "cp":       self.cp,
            "trestbps": self.trestbps,
            "chol":     self.chol,
            "fbs":      self.fbs,
            "restecg":  self.restecg,
            "thalach":  self.thalach,
            "exang":    self.exang,
            "oldpeak":  self.oldpeak,
            "slope":    self.slope,
            "ca":       self.ca,
            "thal":     self.thal,
            "prediction": self.prediction,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "sex_label":        "Male" if self.sex == 1 else "Female",
            "prediction_label": "Heart Disease" if self.prediction == 1 else "No Heart Disease",
        }
