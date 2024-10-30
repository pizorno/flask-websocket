from email.policy import default

from repository.database import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False, nullable=False)
    bank_payment_id = db.Column(db.Integer, nullable=True)
    qrcode = db.Column(db.String(100), nullable=True)
    expiration_date= db.Column(db.DateTime)
