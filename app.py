from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient
from bson.json_util import dumps
import db
app = Flask(__name__)

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

@app.route('/')
def flask_mongodb_atlas():
    return "Hello! ConstructAPP!"

@app.route("/allusers")
def getAllUsers():
    cursor = db.db.users.find({})
    return dumps(list(cursor))

@app.route('/users/<_id>', methods=['GET'])
def getUser(_id):
    try:
        lista_users = list(db.db.users.find({"_id": int(_id)}))
        return send({"result": lista_users}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@app.route('/users', methods=['POST']) 
def insertUser():
    try:
        request_data = request.get_json() 
        new_store = {
        '_id': request_data['_id'],
        'login': request_data['login'],
        'senha': request_data['senha'],
        'nome': request_data['nome'],
        'email': request_data['email'],
        }
        db.db.users.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@app.route('/users', methods=['PUT'])
def updateUser():
    try:
        request_data = request.get_json() 
        update_store = {
        '_id': request_data['_id'],
        'login': request_data['login'],
        'senha': request_data['senha'],
        'nome': request_data['nome'],
        'email': request_data['email'],
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.users.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@app.route('/users/<_id>', methods=['DELETE'])
def deleteUser(_id):
    try:
        cursor = db.db.users.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



# Equipamentos
@app.route('/equipment', methods=['POST']) 
def insertEquipment():
    try:
        request_data = request.get_json() 
        new_store = {
        '_id': request_data['_id'],
        'valor': request_data['valor'],
        'nome': request_data['nome'],
        'descricao': request_data['descricao'],
        }
        db.db.equipment_collection.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@app.route("/allequipment")
def getAllEquipments():
    cursor = db.db.equipment_collection.find({})
    return dumps(list(cursor))

@app.route('/equipment', methods=['PUT'])
def updateEquipment():
    try:
        request_data = request.get_json() 
        update_store = {
        '_id': request_data['_id'],
        'valor': request_data['valor'],
        'nome': request_data['nome'],
        'descricao': request_data['descricao'],
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.equipment_collection.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@app.route('/equipment/<_id>', methods=['GET'])
def getEquipment(_id):
    try:
        lista_users = list(db.db.equipment_collection.find({"_id": int(_id)}))
        return send({"result": lista_users}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@app.route('/equipment/<_id>', methods=['DELETE'])
def deleteEquipment(_id):
    try:
        cursor = db.db.equipment_collection.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


#Error Handler 404
@app.errorhandler(404)
def not_found_error(error):
    return send({'error': 'Not found error'}, HTTP_SERVER_ERROR)

#Error Handler 500
@app.errorhandler(500)
def internal_server_error(error):
    return send({'error': 'Internal server error'}, HTTP_SERVER_ERROR)

#Exception
@app.errorhandler(Exception)
def unhandled_exception(error):
    try:
        return send({'error': str(error)}, HTTP_SERVER_ERROR)
    except:
        return send({'error': "Unknown error"}, HTTP_SERVER_ERROR)

def send(data, status_code):
    return make_response(dumps(data), status_code)

if __name__ == '__main__':
    app.run(port=8000)