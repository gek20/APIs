from datetime import timedelta
from models import Base, User, Object
from flask import Flask, jsonify, request, abort, g
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///database_2.db?check_same_thread=False')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# verify_password is called when we add the decorator @auth.login_required
@auth.verify_password
def verify_password(username, password):
    print("Looking for user %s" % username)
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify(message="Access token expired", error=401), 401


@jwt.invalid_token_loader
def invalid_token(token):
    return jsonify(message="Access token required", error=401), 401


@app.route('/users/new', methods=['POST'])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    user.hash_password(password)
    session.add(user)  # add to db
    session.commit()
    access_token = create_access_token(identity=user.username,expires_delta=timedelta(minutes=1))
    return jsonify({'token':access_token}), 201


@app.route('/users/access')
@jwt_required()
def get_resource():
    current_user = get_jwt_identity()
    return jsonify({'data': 'Hello, %s!' % current_user})


@app.route('/resources', methods=['GET', 'POST'])
@jwt_required()
def access_resources():
    if request.method == 'GET':
        obj = session.query(Object).all()
        return jsonify(bagels=[o.serialize for o in obj])
    elif request.method == 'POST':
        name = request.json.get('name')
        description = request.json.get('description')
        quantity = request.json.get('quantity')
        price = request.json.get('price')
        new_object = Object(name=name, description=description, quantity=quantity, price=price)
        session.add(new_object)
        session.commit()
        return jsonify(new_object.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
