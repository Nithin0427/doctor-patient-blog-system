# simple script to create DB tables and add sample users
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.create_all()
    # add sample users if not exist
    if not User.query.filter_by(username='doctor').first():
        u = User(username='doctor', password_hash=generate_password_hash('doctorpass'), role='doctor')
        db.session.add(u)
    if not User.query.filter_by(username='patient').first():
        p = User(username='patient', password_hash=generate_password_hash('patientpass'), role='patient')
        db.session.add(p)
    db.session.commit()
    print('Created tables and sample users (doctor/doctorpass, patient/patientpass)')
