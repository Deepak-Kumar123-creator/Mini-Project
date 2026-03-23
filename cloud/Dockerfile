FROM python:3.11-slim
LABEL maintainer="AI Healthcare Team"
LABEL description="AI-powered Heart Disease Prediction API (Flask + Random Forest)"
LABEL version="1.0.0"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/database
RUN echo "Training ML model..." \
    && python ml_model/train_model.py \
    && echo "Model training complete!"
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" \
    || exit 1
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "backend.app:create_app()"]
