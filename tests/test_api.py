from app import create_app, DB
from app.models import Prediction


def test_logged_in_prediction_is_saved():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    client.post('/register', data={
        'name': 'Test User',
        'email': 'test_user@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    res = client.post('/predict', data={
        'patient_name': 'Test Patient',
        'age': '25',
        'gender': 'Male',
        'symptoms': ['chest_pain', 'breathlessness', 'sweating']
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Recommended Healthcare Pathway' in res.data

    with app.app_context():
        record = Prediction.query.filter_by(patient_name='Test Patient').first()
        assert record is not None
        assert record.user_id is not None
