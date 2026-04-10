# Architecture Overview — AI Healthcare Recommendation System

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER'S BROWSER                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              frontend/index.html (SPA)                       │   │
│  │  ┌─────────────────┐   ┌─────────────────────────────────┐  │   │
│  │  │ patient_form.js │   │         dashboard.js            │  │   │
│  │  │  Form Builder   │──▶│  fetch() → API → render result  │  │   │
│  │  └─────────────────┘   └─────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP POST /api/predict (JSON)
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND — Flask REST API                         │
│                     (backend/app.py)                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   routes.py (Blueprint)                      │  │
│  │   /api/predict  →  validate  →  call ML  →  save DB  →       │  │
│  │   return JSON                                                 │  │
│  │   /api/patients →  query DB  →  return list                  │  │
│  │   /api/stats    →  aggregate →  return summary               │  │
│  └───────────────────────────────────────────────────────────────┘  │
│              │                            │                          │
│              ▼                            ▼                          │
│  ┌─────────────────────┐    ┌─────────────────────────────────────┐ │
│  │   ML Layer          │    │   Database Layer                    │ │
│  │   ml_model/         │    │   models.py (SQLAlchemy ORM)        │ │
│  │   predict.py        │    │   ──────────────────────────────    │ │
│  │   ┌───────────────┐ │    │   database/healthcare.db (SQLite)   │ │
│  │   │  model.pkl    │ │    │   Table: patients                   │ │
│  │   │ RandomForest  │ │    │   - id, name, vitals, prediction    │ │
│  │   │  Classifier   │ │    │   - risk_score, risk_level          │ │
│  │   └───────────────┘ │    │   - created_at                      │ │
│  └─────────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Cloud / Docker         │
                    │   cloud/Dockerfile       │
                    │   Gunicorn WSGI server   │
                    │   Port: 5000             │
                    └─────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer

| File              | Responsibility                                             |
|-------------------|------------------------------------------------------------|
| `index.html`      | SPA shell: header, tab nav, page containers, styles        |
| `patient_form.js` | Dynamically renders form from field config, validates input |
| `dashboard.js`    | Calls Flask API, renders result, loads stats & history     |

**Technology**: Vanilla HTML5 + CSS3 + JavaScript (ES6+)  
**Communication**: `fetch()` API with JSON payloads  
**Design**: Dark glassmorphism UI with animated gradient accents

---

### 2. Backend Layer

| File         | Responsibility                                              |
|--------------|-------------------------------------------------------------|
| `app.py`     | Flask app factory, CORS, SQLAlchemy init, blueprint register|
| `routes.py`  | REST API endpoints: `/predict`, `/patients`, `/stats`       |
| `models.py`  | SQLAlchemy `Patient` ORM model, `to_dict()` serialization   |

**Technology**: Python 3.11 + Flask + Flask-SQLAlchemy + Flask-CORS  
**API Style**: RESTful JSON API  
**WSGI**: Gunicorn (production), Flask dev server (development)

---

### 3. Machine Learning Layer

| File             | Responsibility                                           |
|------------------|----------------------------------------------------------|
| `dataset.csv`    | Heart disease training dataset (100 rows, 14 features)  |
| `train_model.py` | Trains Random Forest, evaluates, saves `model.pkl`      |
| `predict.py`     | Loads `model.pkl`, validates input, returns prediction  |

**Algorithm**: Random Forest Classifier (100 trees, max_depth=10)  
**Features**: 13 clinical features (age, sex, cp, trestbps, chol, …)  
**Output**: `prediction` (0/1), `risk_score` (0–1), `risk_level`, `message`

---

### 4. Database Layer

| File            | Responsibility                                  |
|-----------------|-------------------------------------------------|
| `schema.sql`    | Raw SQL DDL for the `patients` table + indexes  |
| `healthcare.db` | SQLite database file (auto-created by Flask)    |

**Technology**: SQLite (file-based, no server needed)  
**ORM**: Flask-SQLAlchemy  
**Tables**: `patients` — stores vitals + prediction per request

---

### 5. Cloud / Deployment

| File              | Responsibility                              |
|-------------------|---------------------------------------------|
| `Dockerfile`      | Containerizes app: trains model + runs API  |
| `deployment.md`   | Step-by-step guides for Docker, AWS, GCP    |

---

## Data Flow — Single Prediction Request

```
[User fills form] 
      │
      ▼
[patient_form.js validates + serializes form]
      │  JSON payload
      ▼
[dashboard.js fetch() → POST /api/predict]
      │
      ▼
[routes.py: parse JSON → call predict()]
      │
      ▼
[predict.py: validate → load model.pkl → model.predict() + predict_proba()]
      │  { prediction, risk_score, risk_level, message, confidence }
      ▼
[routes.py: save Patient record to SQLite → return JSON result]
      │
      ▼
[dashboard.js: renderResult() → animates risk meter, shows badge + message]
      │
      ▼
[User sees: Risk Score, Level Badge, Confidence %, Diagnosis]
```

---

## Security Considerations

- **Input Validation**: All 13 fields validated server-side in `predict.py` with type and range checks
- **CORS**: Configured in Flask to allow cross-origin requests from the frontend
- **No Auth (v1)**: This system is designed for internal/demo use; add JWT auth for production
- **SQL Injection**: Prevented by SQLAlchemy ORM parameterized queries
- **Error Handling**: All endpoints return structured JSON errors; no stack traces exposed to client
