# AI-Driven Personalized Healthcare Pathway Recommendation System

A Flask + Machine Learning mini-project that predicts possible diseases from symptoms, provides a patient-friendly healthcare recommendation pathway, and stores prediction history for each logged-in user.

## Dataset used
Primary dataset reference: Kaggle Community Healthcare MultiSymptoms-Disease Dataset  
https://www.kaggle.com/datasets/arjunnairedu/community-healthcare-multisymptomsdisease-dataset

This project also includes an offline fallback CSV at `data/multi_disease_symptoms.csv`, so the project can run without Kaggle login or internet.

## Main presentation features
- Login and registration system
- Disease prediction form after login
- Symptom search and selection
- Disease prediction using saved ML model
- Recommendation system for patient health improvement
- Prediction history saved for the logged-in user
- Clean presentation UI without developer-level evaluation screens
- SQLite database with SQLAlchemy
- Password hashing with Flask-Login/Werkzeug
- Clean folder structure for project review

## Run commands for VS Code terminal

### Windows PowerShell
```powershell
cd healthcare_pathway_project
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade "pip<26"
pip install --only-binary=:all: Flask Flask-SQLAlchemy Flask-Login Werkzeug pandas numpy scikit-learn joblib matplotlib seaborn flask-limiter flask-wtf email-validator
python scripts\prepare_dataset.py
python scripts\train_model.py
python run.py
```

Open in browser:
```text
http://127.0.0.1:5000
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### Windows CMD
```bat
cd healthcare_pathway_project
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade "pip<26"
pip install --only-binary=:all: Flask Flask-SQLAlchemy Flask-Login Werkzeug pandas numpy scikit-learn joblib matplotlib seaborn flask-limiter flask-wtf email-validator
python scripts\prepare_dataset.py
python scripts\train_model.py
python run.py
```

## Recommended demo flow
1. Open `http://127.0.0.1:5000`
2. Register or login
3. Use the dashboard prediction form
4. Select symptoms and submit
5. Show disease result and recommendation pathway
6. Return to dashboard and show saved history

## Important medical disclaimer
This is an academic mini-project. It is not a real medical diagnosis tool. Always consult a qualified doctor.
