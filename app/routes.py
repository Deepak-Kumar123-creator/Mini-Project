from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import DB, LIMITER
from app.models import User, Prediction
from app.ml_service import load_assets, predict

main = Blueprint("main", __name__)

@main.after_app_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


def get_symptom_labels():
    _, _, symptoms, _ = load_assets()
    return [(s, s.replace("_", " ").title()) for s in symptoms]


@main.route("/")
def index():
    return render_template("index.html", symptoms=get_symptom_labels())


@main.route("/predict", methods=["POST"])
@login_required
@LIMITER.limit("20 per minute")
def predict_route():
    name = request.form.get("patient_name", "").strip()
    age_raw = request.form.get("age", "").strip()
    gender = request.form.get("gender", "").strip()
    selected = request.form.getlist("symptoms")
    if not name or not age_raw or not gender or len(selected) < 2:
        flash("Enter patient name, age, gender, and at least 2 symptoms.", "danger")
        return redirect(url_for("main.dashboard"))
    try:
        age = int(age_raw)
        if age < 1 or age > 120:
            raise ValueError
    except ValueError:
        flash("Age must be between 1 and 120.", "danger")
        return redirect(url_for("main.dashboard"))

    best, top = predict(selected, age=age)
    record = Prediction(
        patient_name=name,
        age=age,
        gender=gender,
        symptoms=", ".join(selected),
        predicted_disease=best["disease"],
        confidence=best["confidence"],
        pathway=best["pathway"],
        user_id=current_user.id,
    )
    DB.session.add(record)
    DB.session.commit()
    return render_template("result.html", best=best, top=top, record=record)


@main.route("/api/predict", methods=["POST"])
@login_required
@LIMITER.limit("30 per minute")
def api_predict():
    data = request.get_json(silent=True) or {}
    selected = data.get("symptoms", [])
    age = data.get("age")
    if not isinstance(selected, list) or len(selected) < 2:
        return jsonify({"error": "Provide symptoms as a list with at least 2 selected symptoms."}), 400
    best, top = predict(selected, age=age)
    return jsonify({"best_prediction": best, "top_predictions": top})


@main.route("/dashboard")
@login_required
def dashboard():
    records = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).limit(20).all()
    return render_template("dashboard.html", records=records, symptoms=get_symptom_labels())


@main.route("/metrics")
def metrics():
    # Model metrics are intentionally hidden from the presentation UI.
    # They remain available only as backend files for development/report work.
    if current_user.is_authenticated:
        flash("Metrics are hidden in presentation mode. Use the prediction dashboard.", "warning")
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("main.index"))


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 6:
            flash("Name, valid email and 6+ character password required.", "danger")
            return redirect(url_for("main.register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return redirect(url_for("main.login"))
        user = User(name=name, email=email)
        user.set_password(password)
        DB.session.add(user)
        DB.session.commit()
        login_user(user)
        return redirect(url_for("main.dashboard"))
    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Invalid login.", "danger")
    return render_template("login.html")


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
