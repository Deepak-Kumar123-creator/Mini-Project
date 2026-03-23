# AI Healthcare Recommendation System

> **An end-to-end AI-powered heart disease risk prediction system** using Random Forest ML, Flask REST API, and a modern dark-themed web frontend.

---

## 🏗️ Project Structure

```
AI Drive HealthCare/
│
├── frontend/
│   ├── index.html          ← Main SPA (single-page app)
│   ├── dashboard.js        ← API calls, result rendering, stats
│   └── patient_form.js     ← Dynamic form builder
│
├── backend/
│   ├── app.py              ← Flask app factory + entry point
│   ├── routes.py           ← REST API endpoints
│   └── models.py           ← SQLAlchemy ORM model
│
├── ml_model/
│   ├── dataset.csv         ← Heart disease training dataset
│   ├── train_model.py      ← Trains & saves model.pkl
│   └── predict.py          ← Prediction function
│
├── database/
│   └── schema.sql          ← SQLite schema definition
│
├── cloud/
│   ├── Dockerfile          ← Docker container definition
│   └── deployment.md       ← Cloud deployment guide
│
├── docs/
│   ├── architecture.md     ← System architecture diagram
│   └── system_design.md    ← Design decisions & ML pipeline
│
├── README.md               ← This file
└── requirements.txt        ← Python dependencies
```

---

## ⚡ Quick Start (5 Steps)

### Step 1 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Train the ML Model

```bash
python ml_model/train_model.py
```

This will:
- Load `ml_model/dataset.csv`
- Train a Random Forest Classifier
- Print accuracy & classification report
- Save `ml_model/model.pkl`

### Step 3 — Start the Flask Backend

```bash
python backend/app.py
```

Server starts at: `http://127.0.0.1:5000`

### Step 4 — Open the Frontend

Open **`frontend/index.html`** in your browser (double-click or use Live Server in VS Code).

### Step 5 — Make a Prediction

1. Fill in the patient form
2. Click **"Analyze Heart Disease Risk"**
3. View the risk score, level badge, and diagnosis

---

## 🤖 Machine Learning

| Property          | Value                              |
|-------------------|------------------------------------|
| Algorithm         | Random Forest Classifier           |
| Number of Trees   | 100 estimators                     |
| Max Depth         | 10 levels                          |
| Train/Test Split  | 80% / 20%                          |
| Features          | 13 clinical features               |
| Target            | Binary (0 = healthy, 1 = disease)  |
| Model File        | `ml_model/model.pkl`               |

### Input Features

| Feature    | Description                              | Range      |
|------------|------------------------------------------|------------|
| `age`      | Patient age                              | 1–120      |
| `sex`      | Gender (1=male, 0=female)                | 0–1        |
| `cp`       | Chest pain type                          | 0–3        |
| `trestbps` | Resting blood pressure (mmHg)            | 80–220     |
| `chol`     | Serum cholesterol (mg/dl)                | 100–600    |
| `fbs`      | Fasting blood sugar > 120 mg/dl          | 0–1        |
| `restecg`  | Resting ECG results                      | 0–2        |
| `thalach`  | Maximum heart rate achieved              | 60–220     |
| `exang`    | Exercise-induced angina                  | 0–1        |
| `oldpeak`  | ST depression                            | 0–10       |
| `slope`    | ST segment slope                         | 0–2        |
| `ca`       | Major vessels (fluoroscopy)              | 0–4        |
| `thal`     | Thalassemia type                         | 0–3        |

---

## 🔌 API Endpoints

| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| GET    | `/`                   | Health check + endpoint directory  |
| POST   | `/api/predict`        | Run heart disease prediction       |
| GET    | `/api/patients`       | List all patient records           |
| GET    | `/api/patients/<id>`  | Get a specific patient record      |
| GET    | `/api/stats`          | Aggregate statistics               |
| GET    | `/api/health`         | API health check                   |

### Example: Predict (cURL)

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55, "sex": 1, "cp": 2,
    "trestbps": 132, "chol": 210, "fbs": 0,
    "restecg": 1, "thalach": 165, "exang": 0,
    "oldpeak": 1.2, "slope": 1, "ca": 0, "thal": 2,
    "patient_name": "Jane Smith"
  }'
```

### Example Response

```json
{
  "prediction": 1,
  "risk_score": 0.63,
  "risk_level": "HIGH",
  "message": "High risk of heart disease. Immediate medical consultation recommended!",
  "confidence": 63.0,
  "patient_id": 5,
  "status": "success"
}
```

---

## 🐳 Docker Deployment

```bash
# Build image (trains model automatically)
docker build -f cloud/Dockerfile -t ai-healthcare:latest .

# Run container
docker run -d -p 5000:5000 --name ai-healthcare ai-healthcare:latest

# Access API
curl http://localhost:5000/
```

See [`cloud/deployment.md`](cloud/deployment.md) for AWS EC2, Google Cloud Run, and Docker Compose guides.

---

## 📋 Frontend Features

| Feature             | Description                                       |
|---------------------|---------------------------------------------------|
| Patient Form        | All 13 inputs with validation hints               |
| Risk Meter          | Animated gradient bar showing risk percentage     |
| Risk Badge          | Color-coded LOW / MODERATE / HIGH badge           |
| Prediction Result   | Diagnosis, risk score, confidence, patient ID     |
| Dashboard Tab       | Aggregate stats (total patients, avg risk, etc.)  |
| History Tab         | Full patient history table from the database      |

---

## 🛠️ Technologies Used

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Frontend    | HTML5, CSS3, Vanilla JavaScript     |
| Backend     | Python 3.11, Flask, Flask-CORS      |
| ML          | scikit-learn (Random Forest)        |
| Database    | SQLite + Flask-SQLAlchemy           |
| Deployment  | Docker, Gunicorn                    |

---

## ⚠️ Medical Disclaimer

This system is for **educational and demonstration purposes only**. It does **not** constitute medical advice. Always consult a licensed healthcare professional for medical decisions.

---

## 📄 License

MIT License — Free to use, modify, and distribute.
