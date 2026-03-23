import pickle
import os
import pandas as pd
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
_model = None

def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at: {MODEL_PATH}\n"
                f"Please run train_model.py first to generate model.pkl"
            )
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
        print(f"[INFO] Model loaded from: {MODEL_PATH}")
    return _model

def validate_input(data: dict) -> dict:
    required_features = [
        'age', 'sex', 'cp', 'trestbps', 'chol',
        'fbs', 'restecg', 'thalach', 'exang',
        'oldpeak', 'slope', 'ca', 'thal'
    ]
    missing = [f for f in required_features if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    validations = {
        'age':      (int,   1,   120,  "Age must be between 1 and 120"),
        'sex':      (int,   0,   1,    "Sex must be 0 (female) or 1 (male)"),
        'cp':       (int,   0,   3,    "Chest pain type must be 0-3"),
        'trestbps': (float, 80,  220,  "Resting blood pressure must be 80-220 mmHg"),
        'chol':     (float, 100, 600,  "Cholesterol must be 100-600 mg/dl"),
        'fbs':      (int,   0,   1,    "Fasting blood sugar must be 0 or 1"),
        'restecg':  (int,   0,   2,    "Resting ECG must be 0, 1, or 2"),
        'thalach':  (float, 60,  220,  "Max heart rate must be 60-220"),
        'exang':    (int,   0,   1,    "Exercise induced angina must be 0 or 1"),
        'oldpeak':  (float, 0,   10,   "ST depression must be 0-10"),
        'slope':    (int,   0,   2,    "Slope must be 0, 1, or 2"),
        'ca':       (int,   0,   4,    "Number of major vessels must be 0-4"),
        'thal':     (int,   0,   3,    "Thal must be 0-3"),
    }
    
    cleaned = {}
    for field, (dtype, min_val, max_val, msg) in validations.items():
        try:
            value = dtype(data[field])
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for '{field}': expected {dtype.__name__}")
        if not (min_val <= value <= max_val):
            raise ValueError(f"Invalid value for '{field}': {msg}")
        cleaned[field] = value
    
    return cleaned

def predict(patient_data: dict) -> dict:
    
    model = load_model()
    cleaned_data = validate_input(patient_data)
    feature_order = [
        'age', 'sex', 'cp', 'trestbps', 'chol',
        'fbs', 'restecg', 'thalach', 'exang',
        'oldpeak', 'slope', 'ca', 'thal'
    ]
    input_df = pd.DataFrame([[cleaned_data[f] for f in feature_order]], columns=feature_order)
    prediction = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0]
    risk_score: float = float(probabilities[1])
    if risk_score < 0.3:
        risk_level = "LOW"
        message = "Low risk of heart disease. Maintain a healthy lifestyle!"
    elif risk_score < 0.6:
        risk_level = "MODERATE"
        message = "Moderate risk of heart disease. Consult a doctor for further evaluation."
    else:
        risk_level = "HIGH"
        message = "High risk of heart disease. Immediate medical consultation recommended!"
    confidence: float = float(max(probabilities)) * 100.0
    
    return {
        "prediction": prediction,
        "risk_score": float(f"{risk_score:.4f}"),
        "risk_level": risk_level,
        "message": message,
        "confidence": float(f"{confidence:.2f}"),
        "status": "success"
    }
if __name__ == "__main__":
    sample_patient = {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1
    }
    
    print("=" * 50)
    print("  Heart Disease Prediction Test")
    print("=" * 50)
    print(f"\nPatient Data: {sample_patient}")
    
    result = predict(sample_patient)
    
    print("\n--- Prediction Result ---")
    for key, value in result.items():
        print(f"  {key:<15}: {value}")
    print("=" * 50)
