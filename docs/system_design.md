# System Design — AI Healthcare Recommendation System

## 1. Problem Statement

Cardiovascular disease is the leading cause of death globally. Early detection of heart disease risk is critical for preventive healthcare. This system uses machine learning to analyze patient clinical data and predict heart disease risk in real-time, providing healthcare workers with an instant risk assessment tool.

---

## 2. System Goals

| Goal              | Description                                               |
|-------------------|-----------------------------------------------------------|
| **Accuracy**      | Train ML model with ≥ 80% accuracy on heart disease data  |
| **Speed**         | API response time < 500ms per prediction                  |
| **Usability**     | Simple form UI requiring no technical expertise           |
| **Persistence**   | Store every prediction in a database for audit/review     |
| **Portability**   | Run locally or deploy to any cloud via Docker             |

---

## 3. Technology Choices & Rationale

### Frontend
- **Vanilla HTML/CSS/JS** — No build step needed; lightweight, deployable from any static host
- **Font Awesome** — Icon library for medical UI elements
- **Google Fonts** — Professional Inter typeface

### Backend
- **Flask (Python)** — Lightweight, easy to integrate with scikit-learn ML models natively
- **Flask-CORS** — Handles cross-origin requests between frontend and API
- **Flask-SQLAlchemy** — ORM for clean, Pythonic database access

### Machine Learning
- **Random Forest Classifier** — Chosen for:
  - High accuracy on tabular medical data
  - Built-in feature importance scores
  - Robust to outliers and missing data
  - Probability estimates via `predict_proba()`
- **scikit-learn** — Industry-standard ML library

### Database
- **SQLite** — Chosen for simplicity (file-based, zero config); easy to swap with PostgreSQL in production

### Deployment
- **Docker** — Environment consistency across local, staging, and production
- **Gunicorn** — Production-grade WSGI server (replaces Flask's dev server)

---

## 4. ML Model Design

### Dataset
- **Source**: UCI Heart Disease / Cleveland Dataset (adapted)
- **Rows**: 100 training samples
- **Target**: `target` (0 = no disease, 1 = disease)

### Feature Engineering
No additional feature engineering applied — all 13 raw clinical features used directly:

| Feature    | Type   | Description                              |
|------------|--------|------------------------------------------|
| `age`      | int    | Patient age in years                     |
| `sex`      | binary | 1 = male, 0 = female                     |
| `cp`       | 0-3    | Chest pain type                          |
| `trestbps` | float  | Resting blood pressure (mmHg)            |
| `chol`     | float  | Serum cholesterol (mg/dl)                |
| `fbs`      | binary | Fasting blood sugar > 120 mg/dl          |
| `restecg`  | 0-2    | Resting ECG results                      |
| `thalach`  | float  | Maximum heart rate achieved              |
| `exang`    | binary | Exercise-induced angina                  |
| `oldpeak`  | float  | ST depression (exercise vs rest)         |
| `slope`    | 0-2    | Slope of peak exercise ST segment        |
| `ca`       | 0-4    | Major vessels colored by fluoroscopy     |
| `thal`     | 0-3    | Thalassemia type                         |

### Training Pipeline

```
dataset.csv  →  pd.read_csv()  →  80/20 train/test split
  →  RandomForestClassifier(n_estimators=100, max_depth=10)
  →  model.fit(X_train, y_train)
  →  accuracy_score, classification_report
  →  pickle.dump(model, model.pkl)
```

### Prediction Pipeline

```
POST /api/predict JSON
  →  validate_input()      — type + range checks
  →  np.array([[...]])     — convert to numpy in feature order
  →  model.predict()       — binary prediction (0 or 1)
  →  model.predict_proba() — probability array [p(0), p(1)]
  →  risk_score = p(1)     — probability of heart disease
  →  risk_level logic:
       risk_score < 0.30  → LOW
       risk_score < 0.60  → MODERATE
       risk_score ≥ 0.60  → HIGH
  →  return JSON result
```

---

## 5. API Design

### Endpoint: `POST /api/predict`

**Request:**
```json
{
  "age": 63, "sex": 1, "cp": 3,
  "trestbps": 145, "chol": 233, "fbs": 1,
  "restecg": 0, "thalach": 150, "exang": 0,
  "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1,
  "patient_name": "John Doe"
}
```

**Response:**
```json
{
  "prediction": 1,
  "risk_score": 0.87,
  "risk_level": "HIGH",
  "message": "High risk of heart disease. Immediate medical consultation recommended!",
  "confidence": 87.0,
  "patient_id": 42,
  "status": "success"
}
```

### HTTP Status Codes

| Code | Meaning                                     |
|------|---------------------------------------------|
| 200  | Prediction successful                        |
| 400  | Bad request (not JSON, empty body)           |
| 422  | Validation error (invalid field values)      |
| 500  | Internal server error (model not trained)    |

---

## 6. Database Design

```
┌──────────────────────────────────────┐
│           patients                   │
├──────────────┬───────────────────────┤
│ id           │ INTEGER PK AUTOINCR.  │
│ name         │ TEXT                  │
│ age          │ INTEGER               │
│ sex          │ INTEGER               │
│ cp           │ INTEGER               │
│ trestbps     │ REAL                  │
│ chol         │ REAL                  │
│ fbs          │ INTEGER               │
│ restecg      │ INTEGER               │
│ thalach      │ REAL                  │
│ exang        │ INTEGER               │
│ oldpeak      │ REAL                  │
│ slope        │ INTEGER               │
│ ca           │ INTEGER               │
│ thal         │ INTEGER               │
│ prediction   │ INTEGER               │
│ risk_score   │ REAL                  │
│ risk_level   │ TEXT                  │
│ created_at   │ TEXT (ISO datetime)   │
└──────────────┴───────────────────────┘
Indexes: risk_level, created_at DESC, prediction
```

---

## 7. Error Handling Strategy

| Layer      | Strategy                                                    |
|------------|-------------------------------------------------------------|
| Frontend   | Show inline error message; scroll to field; disable submit  |
| API        | Structured JSON error responses; appropriate HTTP codes     |
| ML Layer   | Input validation before calling model; `FileNotFoundError` if model missing |
| Database   | DB write failure does NOT break prediction response (soft warning) |

---

## 8. Scalability Considerations

| Concern           | Current (v1)       | Production (v2+)                         |
|-------------------|--------------------|------------------------------------------|
| Database          | SQLite             | PostgreSQL / MySQL                       |
| WSGI Server       | Gunicorn (2 workers)| Gunicorn + nginx reverse proxy          |
| ML Model          | Single model.pkl   | Model versioning / A-B testing           |
| Auth              | None               | JWT Bearer tokens                        |
| Frontend          | Static files       | CDN (CloudFront, Vercel)                 |
| Horizontal Scale  | Single container   | Kubernetes / ECS cluster                 |
