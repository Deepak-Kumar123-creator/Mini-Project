
from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

def create_app():
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '02a334ce3302ddac351df5fd53e3012c279a4e67c02be834e6e8c7753d5e0178'
    db_path = os.path.join(backend_dir, '..', 'database', 'healthcare.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(db_path)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    from models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[INFO] Database tables created/verified.")
    from routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    @app.route('/')
    def health_check():
        return jsonify({
            "status": "running",
            "message": "AI Healthcare Recommendation API is live!",
            "version": "1.0.0",
            "endpoints": {
                "predict":        "POST /api/predict",
                "patients":       "GET  /api/patients",
                "patient_detail": "GET  /api/patients/<id>",
                "stats":          "GET  /api/stats",
                "health":         "GET  /api/health"
            }
        })
    
    return app
if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "=" * 60)
    print("  AI Healthcare Recommendation System - Backend API")
    print("=" * 60)
    print("  Server running at: http://127.0.0.1:5000")
    print("  API Base URL:      http://127.0.0.1:5000/api")
    print("  Prediction URL:    http://127.0.0.1:5000/api/predict")
    print("=" * 60 + "\n")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
