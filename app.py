from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class UserSecretKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    key = db.Column(db.BigInteger, nullable=False)

    def __init__(self, email, key):
        self.email = email
        self.key = key


@app.route('/users/add/', methods=['POST'])
def add_user():
    data = request.get_json()
    email = data['email']
    key = data['key']
    new_user = UserSecretKey(email, key)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": 'Some error ocurred'}), 400


@app.route('/users/list/', methods=['GET'])
def get_users():
    users = UserSecretKey.query.all()
    users_list = [{"email": user.email, "key": user.key} for user in users]
    return jsonify(users_list), 200


@app.route('/users/<email>/key/', methods=['GET'])
def get_user(email):
    user = UserSecretKey.query.filter_by(email=email).first()
    if user:
        return jsonify({"key": user.key}), 200
    return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
