from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ======================
# USER TABLE
# ======================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    mobile = db.Column(db.String(15), unique=True)
    address = db.Column(db.String(200))
    role = db.Column(db.String(20))  # user or worker
    verified = db.Column(db.Boolean, default=True)

# ======================
# WORKER TABLE
# ======================

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    mobile = db.Column(db.String(15), unique=True)
    skill = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    service_radius = db.Column(db.Integer)
    price_per_hour = db.Column(db.Float)
    certificate = db.Column(db.String(200))
    id_proof = db.Column(db.String(200))
    company_proof = db.Column(db.String(200))
    verified = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)

# ======================
# BOOKING TABLE
# ======================

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    worker_id = db.Column(db.Integer)
    service_type = db.Column(db.String(100))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ======================
# FEEDBACK TABLE
# ======================

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))

