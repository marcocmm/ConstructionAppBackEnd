from flask import Blueprint, current_app, session, request, make_response
from bson.objectid import ObjectId
from bson.json_util import dumps
from controllers.login import tokenReq
import db

from  werkzeug.security import generate_password_hash

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_user = Blueprint('user', __name__, url_prefix='/user')

@bp_user.route("/all", methods=['GET'])
@tokenReq
def getAllUsers():
    cursor = db.db.user.find({}, {'senha': False})
    return dumps(list(cursor))

@bp_user.route('', methods=['GET'])
@tokenReq
def getUser():
    try:
        _id = request.args.get('user_id')
        lista_users = list(db.db.user.find({"_id": ObjectId(_id)}))
        return send({"result": lista_users}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_user.route('/user', methods=['POST'])
def insertUser():
    request_data = request.get_json() 
    print(request_data)
    try:
        new_store = {
        'nome': request_data['nome'],
        'senha': generate_password_hash(request_data['senha']),
        'telefone': request_data['telefone'],
        'tipo_usuario_id': request_data['tipo_usuario_id'],
        'nif': request_data['nif'],
        }
        db.db.user.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        print(e)
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_user.route('', methods=['PUT'])
@tokenReq
def updateUser():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'senha': request_data['senha'],
        'telefone': request_data['telefone'],
        'tipo_usuario_id': request_data['tipo_usuario_id'],
        'nif': request_data['nif'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.user.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_user.route('', methods=['DELETE'])
@tokenReq
def deleteUser():
    try:
        _id = request.args.get('user_id')
        cursor = db.db.user.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)