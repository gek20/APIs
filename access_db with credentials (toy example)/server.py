from models import Base, User, Object
from flask import Flask, jsonify, request, abort, g
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///database_name.db?check_same_thread=False')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# verify_password is called when we add the decorator @auth.login_required
@auth.verify_password
def verify_password(username, password):
    print("Looking for user %s" % username)
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get("username")
    password = request.json.get("password")
    if username is None or password is None:
        abort(400)
    if session.query(User).filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    session.add(user)  # add to db
    session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/users/access')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/resources', methods=['GET', 'POST'])
@auth.login_required
def access_resources():
    if request.method == 'GET':
        bagels = session.query(Object).all()
        return jsonify(bagels=[bagel.serialize for bagel in bagels])
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
