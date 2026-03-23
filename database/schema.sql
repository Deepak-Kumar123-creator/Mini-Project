-- =============================================================================
-- schema.sql - SQLite Database Schema
-- =============================================================================
-- This file defines the database schema for the AI Healthcare Recommendation
-- System. Run this script to manually initialize the database structure.
-- NOTE: Flask-SQLAlchemy (models.py) also creates these tables automatically.
-- =============================================================================

-- Enable foreign key constraint support in SQLite
PRAGMA foreign_keys = ON;

-- =============================================================================
-- TABLE: patients
-- =============================================================================
-- Stores patient vitals submitted via the frontend, along with the ML
-- model's prediction for that patient's record.
-- =============================================================================
CREATE TABLE IF NOT EXISTS patients (
    -- ---- Primary Key --------------------------------------------------------
    id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-increment unique ID

    -- ---- Patient Identification ---------------------------------------------
    name        TEXT    NOT NULL DEFAULT 'Anonymous', -- Patient name (optional)

    -- ---- Clinical Input Features (13 features used by the ML model) ---------
    age         INTEGER NOT NULL,   -- Age in years
    sex         INTEGER NOT NULL,   -- 1 = Male, 0 = Female
    cp          INTEGER NOT NULL,   -- Chest pain type (0-3)
    trestbps    REAL    NOT NULL,   -- Resting blood pressure (mmHg)
    chol        REAL    NOT NULL,   -- Serum cholesterol (mg/dl)
    fbs         INTEGER NOT NULL,   -- Fasting blood sugar > 120 mg/dl (1=true)
    restecg     INTEGER NOT NULL,   -- Resting ECG results (0-2)
    thalach     REAL    NOT NULL,   -- Maximum heart rate achieved
    exang       INTEGER NOT NULL,   -- Exercise-induced angina (1=yes, 0=no)
    oldpeak     REAL    NOT NULL,   -- ST depression (exercise relative to rest)
    slope       INTEGER NOT NULL,   -- Slope of peak exercise ST segment (0-2)
    ca          INTEGER NOT NULL,   -- Major vessels colored by fluoroscopy (0-4)
    thal        INTEGER NOT NULL,   -- Thalassemia type (0-3)

    -- ---- ML Prediction Output -----------------------------------------------
    prediction  INTEGER NOT NULL,   -- 0 = No Heart Disease, 1 = Heart Disease
    risk_score  REAL    NOT NULL,   -- Probability of heart disease (0.0–1.0)
    risk_level  TEXT    NOT NULL,   -- 'LOW' | 'MODERATE' | 'HIGH'

    -- ---- Metadata -----------------------------------------------------------
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'utc'))
                                    -- UTC timestamp of prediction
);

-- =============================================================================
-- INDEXES for performance
-- =============================================================================
-- Index on risk_level for fast filtering by risk category
CREATE INDEX IF NOT EXISTS idx_patients_risk_level
    ON patients (risk_level);

-- Index on created_at for time-based sorting
CREATE INDEX IF NOT EXISTS idx_patients_created_at
    ON patients (created_at DESC);

-- Index on prediction for fast count of positive/negative cases
CREATE INDEX IF NOT EXISTS idx_patients_prediction
    ON patients (prediction);

-- =============================================================================
-- Sample verification queries (run manually to test)
-- =============================================================================
-- SELECT COUNT(*) AS total FROM patients;
-- SELECT risk_level, COUNT(*) AS count FROM patients GROUP BY risk_level;
-- SELECT * FROM patients ORDER BY created_at DESC LIMIT 10;
-- SELECT AVG(risk_score) AS avg_risk FROM patients;
