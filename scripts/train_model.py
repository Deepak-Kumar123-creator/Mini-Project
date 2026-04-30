from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "multi_disease_symptoms.csv"
MODEL_DIR = ROOT / "models"
STATIC_DIR = ROOT / "app" / "static"
MODEL_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "img").mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError("Run: python scripts/prepare_dataset.py")

df = pd.read_csv(DATA_PATH)
X = df.drop(columns=["disease"])
y_text = df["disease"]
le = LabelEncoder()
y = le.fit_transform(y_text)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

rf = RandomForestClassifier(n_estimators=80, max_depth=None, random_state=42, class_weight="balanced")
et = ExtraTreesClassifier(n_estimators=80, random_state=42, class_weight="balanced")
lr = LogisticRegression(max_iter=2000, class_weight="balanced")
model = VotingClassifier(estimators=[("rf", rf), ("et", et), ("lr", lr)], voting="soft")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
metrics = {
    "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
    "precision_macro": round(float(precision_score(y_test, y_pred, average="macro", zero_division=0)), 4),
    "recall_macro": round(float(recall_score(y_test, y_pred, average="macro", zero_division=0)), 4),
    "f1_macro": round(float(f1_score(y_test, y_pred, average="macro", zero_division=0)), 4),
    "cross_val_accuracy_mean": round(float(cross_val_score(model, X, y, cv=3, scoring="accuracy").mean()), 4),
    "disease_count": int(y_text.nunique()),
    "symptom_count": int(X.shape[1]),
    "dataset_rows": int(df.shape[0]),
}

report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True, zero_division=0)
with open(MODEL_DIR / "metrics.json", "w", encoding="utf-8") as f:
    json.dump({"metrics": metrics, "classification_report": report}, f, indent=2)

joblib.dump(model, MODEL_DIR / "disease_model.pkl")
joblib.dump(le, MODEL_DIR / "label_encoder.pkl")
joblib.dump(list(X.columns), MODEL_DIR / "symptoms.pkl")

# Feature importance from ExtraTrees member after fit
et_model = model.named_estimators_["et"]
imp = pd.Series(et_model.feature_importances_, index=X.columns).sort_values(ascending=False).head(15)
plt.figure(figsize=(10, 6))
imp.sort_values().plot(kind="barh")
plt.title("Top Symptoms Used by Model")
plt.tight_layout()
plt.savefig(STATIC_DIR / "img" / "feature_importance.png", dpi=150)
plt.close()

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()
plt.tight_layout()
plt.savefig(STATIC_DIR / "img" / "confusion_matrix.png", dpi=150)
plt.close()

print("Training completed")
print(json.dumps(metrics, indent=2))
