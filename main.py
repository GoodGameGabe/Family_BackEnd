import os

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from models import db, Person

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(APP, db)
db.init_app(APP)

@APP.route('/')
def hello_world():
    return "lo"

@APP.route('/persons', methods=['GET'])
def allPersons():
    return jsonify(swagger(APP))

@APP.route('/person/<int:id>', methods=['PUT', 'GET', "DELETE"])
def getPerson(id):
    if request.method == 'GET':
        person = Person.query.get(id)
        return jsonify({"data": person.to_dict()})
    elif request.method == 'PUT':
        person = Person.query.get(id)
        return jsonify({"data": person})
    elif request.method == 'DELETE':
        user1 = Person.query.get(id)
        return user1.to_json()
    else:
        return "Invalid Method", 404

@APP.route('/person/add', methods=['POST'])
def addPerson():
    info = request.get_json() or {}
    entity = Person(
        name= info["name"],
        gender = info["gender"],
        dob=info["dob"],
        email = info["email"],
        picture= info["picture"]
        )

    if info["siblings"] is not None:
        for s in info["siblings"]:
            sibling = Person.query.get(s)
            if sibling is not None:
                entity.siblings.append(sibling)
            else:
                return jsonify("error")

    if info["children"] is not None:
        for c in info["children"]:
            child = Person.query.get(c)
            if child is not None:
                entity.children.append(child)
            else:
                return jsonify("error")

    if info["parents"] is not None:
        for p in info["parents"]:
            parent = Person.query.get(p)
            if parent is not None:
                entity.parents.append(sibling)
            else:
                return jsonify("error")

    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"})

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    APP.run(host='0.0.0.0', port=PORT)