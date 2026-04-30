"""Creates a multi-disease symptom dataset fallback.
Primary dataset idea/source: Kaggle Community Healthcare MultiSymptoms–Disease Dataset.
This script creates an offline CSV so the project works without Kaggle login.
"""
from pathlib import Path
import random
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "multi_disease_symptoms.csv"
random.seed(42)

DISEASE_PROFILES = {
    "Common Cold": ["runny_nose", "sneezing", "sore_throat", "mild_fever", "cough"],
    "Influenza": ["high_fever", "body_ache", "fatigue", "cough", "headache"],
    "COVID-19": ["fever", "dry_cough", "loss_of_smell", "breathlessness", "fatigue"],
    "Dengue": ["high_fever", "joint_pain", "rash", "headache", "low_platelets"],
    "Malaria": ["fever", "chills", "sweating", "headache", "nausea"],
    "Typhoid": ["prolonged_fever", "abdominal_pain", "weakness", "loss_of_appetite", "diarrhea"],
    "Pneumonia": ["fever", "productive_cough", "chest_pain", "breathlessness", "fatigue"],
    "Asthma": ["wheezing", "breathlessness", "chest_tightness", "cough", "night_symptoms"],
    "Diabetes": ["excessive_thirst", "frequent_urination", "fatigue", "blurred_vision", "weight_loss"],
    "Hypertension": ["headache", "dizziness", "chest_discomfort", "blurred_vision", "fatigue"],
    "Heart Disease": ["chest_pain", "breathlessness", "sweating", "left_arm_pain", "fatigue"],
    "Migraine": ["severe_headache", "nausea", "light_sensitivity", "sound_sensitivity", "visual_aura"],
    "Gastroenteritis": ["vomiting", "diarrhea", "abdominal_cramps", "fever", "dehydration"],
    "GERD": ["heartburn", "acid_regurgitation", "chest_burning", "sore_throat", "bloating"],
    "Tuberculosis": ["chronic_cough", "weight_loss", "night_sweats", "fever", "blood_in_sputum"],
    "Anemia": ["fatigue", "pale_skin", "dizziness", "shortness_of_breath", "fast_heartbeat"],
    "Jaundice": ["yellow_eyes", "dark_urine", "abdominal_pain", "nausea", "itching"],
    "Urinary Tract Infection": ["burning_urination", "frequent_urination", "lower_abdominal_pain", "fever", "cloudy_urine"],
    "Kidney Stone": ["flank_pain", "blood_in_urine", "nausea", "vomiting", "painful_urination"],
    "Allergy": ["sneezing", "itching", "rash", "watery_eyes", "runny_nose"],
}
all_symptoms = sorted({s for v in DISEASE_PROFILES.values() for s in v})
rows = []
for disease, core in DISEASE_PROFILES.items():
    for _ in range(260):
        row = {s: 0 for s in all_symptoms}
        # Keep strong signal but realistic missing/noisy symptoms
        chosen = random.sample(core, random.randint(3, len(core)))
        for s in chosen:
            row[s] = 1
        noise_pool = [s for s in all_symptoms if s not in core]
        for s in random.sample(noise_pool, random.randint(0, 2)):
            row[s] = 1
        row["disease"] = disease
        rows.append(row)

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
DATA.parent.mkdir(exist_ok=True)
df.to_csv(DATA, index=False)
print(f"Dataset saved: {DATA} | rows={len(df)} | symptoms={len(all_symptoms)} | diseases={len(DISEASE_PROFILES)}")
