# Cloud Deployment Guide

## AI Healthcare Recommendation System — Docker & Cloud Deployment

---

## Prerequisites

| Tool       | Version  | Purpose                        |
|------------|----------|--------------------------------|
| Docker     | ≥ 20.x   | Containerize the application   |
| Python     | ≥ 3.9    | Local development              |
| Git        | Any      | Version control                |

---

## Option 1 — Run Locally with Docker

### Step 1: Build the Docker Image

Open a terminal in the **project root directory** and run:

```bash
# Build the image (this also trains the ML model inside Docker)
docker build -f cloud/Dockerfile -t ai-healthcare:latest .
```

> ⏱️ First build takes 3–5 minutes. Subsequent builds use layer cache.

### Step 2: Run the Container

```bash
# Run the container, mapping port 5000 on your machine to port 5000 in the container
docker run -d \
  --name ai-healthcare \
  -p 5000:5000 \
  -v $(pwd)/database:/app/database \
  ai-healthcare:latest
```

**Windows PowerShell:**
```powershell
docker run -d `
  --name ai-healthcare `
  -p 5000:5000 `
  -v ${PWD}/database:/app/database `
  ai-healthcare:latest
```

### Step 3: Verify It's Running

```bash
# Check container status
docker ps

# View logs
docker logs ai-healthcare

# Test API endpoint
curl http://localhost:5000/
```

You should see: `{"message": "AI Healthcare Recommendation API is live!", ...}`

### Step 4: Test the Prediction API

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3,
    "trestbps": 145, "chol": 233, "fbs": 1,
    "restecg": 0, "thalach": 150, "exang": 0,
    "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1,
    "patient_name": "Test Patient"
  }'
```

### Step 5: Stop the Container

```bash
docker stop ai-healthcare
docker rm ai-healthcare
```

---

## Option 2 — Deploy to AWS EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose: **Ubuntu 22.04 LTS** (t2.micro for free tier)
3. Security Group: Open ports **22** (SSH) and **5000** (API)
4. Download your `.pem` key pair

### Step 2: SSH into EC2

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>
```

### Step 3: Install Docker on EC2

```bash
sudo apt-get update -y
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker ubuntu
# Re-login to apply group changes
exit && ssh -i your-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>
```

### Step 4: Transfer Project Files

From your local machine:
```bash
scp -i your-key.pem -r "AI Drive HealthCare" ubuntu@<EC2_IP>:~/ai-healthcare
```

### Step 5: Build & Run on EC2

```bash
cd ~/ai-healthcare
docker build -f cloud/Dockerfile -t ai-healthcare:latest .
docker run -d --name ai-healthcare -p 5000:5000 ai-healthcare:latest
```

### Step 6: Access the API

Open in browser: `http://<YOUR_EC2_PUBLIC_IP>:5000/`

---

## Option 3 — Deploy to Google Cloud Run (Serverless)

### Step 1: Install Google Cloud SDK

Download from: https://cloud.google.com/sdk/docs/install

### Step 2: Authenticate and Configure

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com containerregistry.googleapis.com
```

### Step 3: Build and Push to Google Container Registry

```bash
# Tag the image for GCR
docker build -f cloud/Dockerfile -t gcr.io/YOUR_PROJECT_ID/ai-healthcare:latest .

# Push to GCR
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/ai-healthcare:latest
```

### Step 4: Deploy to Cloud Run

```bash
gcloud run deploy ai-healthcare \
  --image gcr.io/YOUR_PROJECT_ID/ai-healthcare:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 1Gi \
  --cpu 1
```

### Step 5: Get the Service URL

Cloud Run provides a permanent HTTPS URL, e.g.:
`https://ai-healthcare-xxxx-uc.a.run.app`

Update `API_BASE` in `frontend/dashboard.js` to this URL.

---

## Option 4 — Docker Compose (Full Stack)

Create `docker-compose.yml` in the project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: cloud/Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./database:/app/database
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

- Frontend: `http://localhost:8080`
- Backend API: `http://localhost:5000`

---

## Environment Variables

| Variable       | Default              | Description              |
|----------------|----------------------|--------------------------|
| `FLASK_ENV`    | `production`         | Flask environment mode   |
| `FLASK_APP`    | `backend/app.py`     | Flask entry point        |
| `PORT`         | `5000`               | Server port              |

---

## Troubleshooting

| Problem                         | Solution                                           |
|---------------------------------|----------------------------------------------------|
| `model.pkl not found`           | Run `python ml_model/train_model.py` first         |
| `Connection refused on :5000`   | Ensure Flask/Docker is running; check firewall     |
| CORS errors in browser          | Backend CORS is pre-configured for all origins     |
| `Module not found` error        | Run `pip install -r requirements.txt`              |
| Slow Docker build               | Use `--cache-from` flag on subsequent builds       |
