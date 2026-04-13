from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
import sys
import os
_ml_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml_model')
if _ml_dir not in sys.path:
    sys.path.insert(0, _ml_dir)
from predict import predict 
from models import db, Patient
api_blueprint = Blueprint('api', __name__)
@api_blueprint.route('/predict', methods=['POST'])
def predict_heart_disease():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON. Set Content-Type: application/json"
        }), 400
    data = request.get_json()
    
    if not data:
        return jsonify({
            "status": "error",
            "message": "Empty request body received."
        }), 400
    patient_name = data.get('patient_name', 'Anonymous')
    try:
        result = predict(data)
    except FileNotFoundError as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "hint": "Please train the model first by running: python ml_model/train_model.py"
        }), 500
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid input data: {str(e)}"
        }), 422
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500
    try:
        patient_data = {
            'name': patient_name,
            'age': int(data.get('age', 0)),
            'sex': int(data.get('sex', 0)),
            'cp': int(data.get('cp', 0)),
            'trestbps': float(data.get('trestbps', 0)),
            'chol': float(data.get('chol', 0)),
            'fbs': int(data.get('fbs', 0)),
            'restecg': int(data.get('restecg', 0)),
            'thalach': float(data.get('thalach', 0)),
            'exang': int(data.get('exang', 0)),
            'oldpeak': float(data.get('oldpeak', 0)),
            'slope': int(data.get('slope', 0)),
            'ca': int(data.get('ca', 0)),
            'thal': int(data.get('thal', 0)),
            'prediction': result['prediction'],
            'risk_score': result['risk_score'],
            'risk_level': result['risk_level'],
            'created_at': datetime.now(timezone.utc)
        }
        
        patient = Patient(**patient_data)
        db.session.add(patient)
        db.session.commit()
        result['patient_id'] = patient.id
    except TypeError as e:
        result['patient_id'] = None
        result['db_warning'] = f"Model parameter mismatch: {str(e)}"
    except Exception as e:
        result['patient_id'] = None
        result['db_warning'] = f"Could not save to database: {str(e)}"
    return jsonify(result), 200
@api_blueprint.route('/patients', methods=['GET'])
def get_all_patients():
    """
    Returns a list of all patient prediction records stored in the database.
    Supports optional query parameters:
        ?limit=N    - Limit number of results (default: 50)
        ?offset=N   - Offset for pagination (default: 0)
    """
    limit  = request.args.get('limit',  50,  type=int)
    offset = request.args.get('offset', 0,   type=int)
    try:
        patients = Patient.query.order_by(Patient.created_at.desc()).limit(limit).offset(offset).all()
        total    = Patient.query.count()
        
        return jsonify({
            "status": "success",
            "total": total,
            "returned": len(patients),
            "offset": offset,
            "patients": [p.to_dict() for p in patients]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@api_blueprint.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = db.get_or_404(Patient, patient_id)
        return jsonify({
            "status": "success",
            "patient": patient.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Patient {patient_id} not found."}), 404
@api_blueprint.route('/stats', methods=['GET'])
def get_stats():
    try:
        total        = Patient.query.count()
        high_risk    = Patient.query.filter_by(risk_level='HIGH').count()
        moderate     = Patient.query.filter_by(risk_level='MODERATE').count()
        low_risk     = Patient.query.filter_by(risk_level='LOW').count()
        heart_disease = Patient.query.filter_by(prediction=1).count()
        
        avg_risk = db.session.query(
            db.func.avg(Patient.risk_score)
        ).scalar() or 0.0
        
        return jsonify({
            "status": "success",
            "stats": {
                "total_patients":      total,
                "high_risk_count":     high_risk,
                "moderate_risk_count": moderate,
                "low_risk_count":      low_risk,
                "heart_disease_cases": heart_disease,
                "healthy_cases":       total - heart_disease,
                "avg_risk_score":      round(float(avg_risk), 4),  # type: ignore
                "high_risk_pct":       round(float((high_risk / total * 100) if total else 0.0), 1),  # type: ignore
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@api_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "AI Healthcare Recommendation System"
    }), 200
