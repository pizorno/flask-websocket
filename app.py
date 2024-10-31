from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SECRET_KEY'] = 'SECRET_KEY'
db.init_app(app)

@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()
    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400
    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qrcode = data_payment_pix['qrcode_path']
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "The payment has been created", "payment":
        new_payment.to_dict()})

@app.route('/payments/pix/qrcode/<filename>', methods=['GET'])
def get_image(filename):
    return send_file(f"static/img/{filename}.png", mimetype='img/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify(({"message": "The payment has been confirmed"}))

@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)
    return render_template('payment.html',
                           payment_id=payment.id,
                           value=payment.value,
                           host="http://127.0.0.1:5000",
                           qrcode=payment.qrcode)

if __name__ == '__main__':
    app.run(debug=True)