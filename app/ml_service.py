from pathlib import Path
import json
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"

# Disease-specific recommendation knowledge base for patient-friendly pathways.
# This is educational guidance and should not replace professional diagnosis.
RECOMMENDATION_RULES = {
    "Heart Disease": {
        "care_level": "Priority consultation with a cardiologist",
        "summary": "Chest pain, breathlessness, sweating or left arm discomfort should be taken seriously and reviewed by a doctor.",
        "actions": [
            "Book a cardiology consultation and get ECG, blood pressure, lipid profile and sugar test checked.",
            "Avoid heavy exercise until a doctor confirms that it is safe.",
            "Reduce oily food, smoking, alcohol and high-salt diet; prefer fruits, vegetables and light meals.",
            "Go to emergency care immediately if chest pain is severe, spreading to arm/jaw, or associated with breathlessness."
        ],
        "lifestyle": "Daily walking after medical clearance, low-salt food, stress control and regular follow-up are important."
    },
    "Diabetes": {
        "care_level": "Routine medical review with regular monitoring",
        "summary": "High thirst, frequent urination, fatigue and weight changes may indicate blood sugar imbalance.",
        "actions": [
            "Check fasting blood sugar and HbA1c with medical advice.",
            "Avoid sugary drinks, excessive sweets and irregular meals.",
            "Follow a balanced diet with controlled carbohydrates and regular physical activity.",
            "Monitor feet, eyes and wounds because diabetes can delay healing."
        ],
        "lifestyle": "Maintain meal timing, exercise regularly and track sugar levels as advised by the doctor."
    },
    "Hypertension": {
        "care_level": "Doctor consultation and blood pressure monitoring",
        "summary": "Headache, dizziness or chest discomfort with high blood pressure needs proper monitoring.",
        "actions": [
            "Measure blood pressure on multiple days and record readings.",
            "Reduce salt, processed food and excess caffeine.",
            "Do regular walking, manage sleep and avoid stress triggers.",
            "Consult a doctor if BP remains high or symptoms worsen."
        ],
        "lifestyle": "Low-salt diet, weight control, exercise and regular BP tracking help improve control."
    },
    "COVID-19": {
        "care_level": "Isolation and symptom monitoring",
        "summary": "Fever, cough, fatigue, sore throat or breathing difficulty may require infection precautions.",
        "actions": [
            "Use mask and avoid close contact until infection risk is clear.",
            "Monitor temperature and oxygen saturation if available.",
            "Drink fluids, rest properly and consult a doctor for testing and medicines.",
            "Seek urgent help if breathing difficulty, chest pain or low oxygen occurs."
        ],
        "lifestyle": "Rest, hydration and avoiding spread to others are the first priorities."
    },
    "Dengue": {
        "care_level": "Doctor review with platelet monitoring",
        "summary": "High fever, body pain, rash or bleeding signs can be related to dengue and need monitoring.",
        "actions": [
            "Get CBC/platelet count checked as advised by doctor.",
            "Drink plenty of fluids and take proper rest.",
            "Avoid painkillers like ibuprofen/aspirin unless doctor allows.",
            "Seek urgent care for bleeding, severe abdominal pain, vomiting or weakness."
        ],
        "lifestyle": "Hydration and timely blood tests are very important during dengue-like illness."
    },
    "Malaria": {
        "care_level": "Medical test and anti-malarial treatment by doctor",
        "summary": "Fever with chills and sweating may need malaria testing, especially in mosquito-prone areas.",
        "actions": [
            "Get malaria rapid test or blood smear test done.",
            "Take anti-malarial medicine only under medical supervision.",
            "Use mosquito nets, repellents and avoid stagnant water nearby.",
            "Seek urgent care if fever is very high, confusion or severe weakness occurs."
        ],
        "lifestyle": "Prevent mosquito bites and complete the prescribed treatment course."
    },
    "Tuberculosis": {
        "care_level": "Specialist consultation and diagnostic confirmation",
        "summary": "Long-term cough, fever, night sweats or weight loss should be checked for TB.",
        "actions": [
            "Consult a doctor for sputum test, chest X-ray or other TB tests.",
            "Use mask and avoid close exposure if cough is persistent.",
            "Do not stop TB medicines without medical advice if treatment starts.",
            "Improve nutrition and follow up regularly."
        ],
        "lifestyle": "Early testing, treatment adherence and nutrition support are important."
    },
    "Asthma": {
        "care_level": "Respiratory review if breathing symptoms are frequent",
        "summary": "Wheezing, cough and shortness of breath may require inhaler-based management.",
        "actions": [
            "Avoid dust, smoke, pollution and known allergy triggers.",
            "Consult a doctor for inhaler or lung function evaluation.",
            "Keep rescue medication only as prescribed.",
            "Seek urgent care if speaking or breathing becomes difficult."
        ],
        "lifestyle": "Trigger control, clean environment and correct inhaler technique help reduce attacks."
    },
    "Migraine": {
        "care_level": "Routine consultation if headaches are recurrent or severe",
        "summary": "Severe headache with nausea, light sensitivity or repeated episodes may suggest migraine.",
        "actions": [
            "Rest in a quiet and dark room during headache episodes.",
            "Track triggers such as sleep loss, stress, dehydration or certain foods.",
            "Drink water and maintain regular sleep schedule.",
            "Consult a doctor if headaches are new, sudden, very severe or associated with weakness."
        ],
        "lifestyle": "Regular sleep, hydration, reduced screen strain and stress control are helpful."
    },
    "Common Cold": {
        "care_level": "Home care with monitoring",
        "summary": "Mild cough, runny nose, sneezing and throat irritation are usually managed with rest and fluids.",
        "actions": [
            "Drink warm fluids and take adequate rest.",
            "Use steam inhalation or saline gargle if comfortable.",
            "Avoid close contact if infection symptoms are present.",
            "Consult a doctor if fever is high, symptoms persist or breathing difficulty occurs."
        ],
        "lifestyle": "Hydration, rest and hygiene usually help recovery."
    }
}

DEFAULT_RECOMMENDATION = {
    "care_level": "General doctor consultation recommended",
    "summary": "The predicted condition should be confirmed by a qualified medical professional before making health decisions.",
    "actions": [
        "Consult a doctor for physical examination and required tests.",
        "Drink enough water, take rest and monitor symptoms for any worsening.",
        "Avoid self-medication and follow professional medical advice.",
        "Seek urgent care if symptoms become severe, sudden or difficult to manage."
    ],
    "lifestyle": "Healthy diet, sleep, hygiene and regular follow-up support better recovery."
}


def load_assets():
    model = joblib.load(MODEL_DIR / "disease_model.pkl")
    encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
    symptoms = joblib.load(MODEL_DIR / "symptoms.pkl")
    metrics = {}
    mp = MODEL_DIR / "metrics.json"
    if mp.exists():
        with mp.open("r", encoding="utf-8") as f:
            metrics = json.load(f)
    return model, encoder, symptoms, metrics


def build_recommendation(disease, selected_symptoms=None, age=None):
    rec = dict(RECOMMENDATION_RULES.get(disease, DEFAULT_RECOMMENDATION))
    rec["actions"] = list(rec.get("actions", []))
    selected = {str(s).lower() for s in (selected_symptoms or [])}

    urgent_flags = {"chest_pain", "breathlessness", "shortness_of_breath", "bleeding", "severe_abdominal_pain"}
    if selected.intersection(urgent_flags):
        rec["actions"].append("Because warning symptoms are present, do not delay medical evaluation.")

    try:
        if age is not None and int(age) >= 60:
            rec["actions"].append("Since the patient is older, early doctor consultation is safer even for moderate symptoms.")
    except (TypeError, ValueError):
        pass

    return rec


def predict(selected_symptoms, age=None):
    model, encoder, symptoms, _ = load_assets()
    selected = set(selected_symptoms)
    row = {s: 1 if s in selected else 0 for s in symptoms}
    X = pd.DataFrame([row])
    proba = model.predict_proba(X)[0]
    top_indices = proba.argsort()[::-1][:3]
    top = []
    for idx in top_indices:
        disease = encoder.inverse_transform([idx])[0]
        recommendation = build_recommendation(disease, selected_symptoms, age)
        top.append({
            "disease": disease,
            "confidence": round(float(proba[idx]) * 100, 2),
            "pathway": recommendation["summary"],
            "recommendation": recommendation,
        })
    return top[0], top
