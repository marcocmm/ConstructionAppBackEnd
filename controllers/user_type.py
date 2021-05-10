from flask import Blueprint, current_app, session, request, make_response
from controllers.login import tokenReq
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_user_type = Blueprint('user_type', __name__, url_prefix='/user_type')

@bp_user_type.route('/user_type', methods=['POST'])
@tokenReq
def insertUserType():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'permissao_id': request_data['permissao_id'],
        }
        db.db.users_type.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_user_type.route('/<_id>', methods=['GET'])
@tokenReq
def getUserType(_id):
    try:
        user_type = list(db.db.users_type.find({"_id": int(_id)}))
        return send({"result": user_type}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_user_type.route('/<_id>', methods=['DELETE'])
@tokenReq
def deleteUserType(_id):
    try:
        cursor = db.db.users_type.find_one_and_delete({"_id": int(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_user_type.route("/all", methods=['GET'])
@tokenReq
def getAllUsersType():
    cursor = db.db.users_type.find({})
    return dumps(list(cursor))


@bp_user_type.route('/<_id>', methods=['PUT'])
@tokenReq
def updateUserType():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'permissao_id': request_data['permissao_id'],
        }
        query = { "_id": int(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.users_type.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)