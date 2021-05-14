from flask import Blueprint, current_app, session, request, make_response
from bson.objectid import ObjectId
from controllers.login import tokenReq
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_client = Blueprint('client', __name__, url_prefix='/client')

@bp_client.route("/all", methods=['GET'])
@tokenReq
def getAllClients():
    cursor = db.db.client.find({})
    return dumps(list(cursor))

@bp_client.route('', methods=['GET'])
@tokenReq
def getClient():
    try:
        _id = request.args.get('client_id')
        client = list(db.db.client.find({"_id": ObjectId(_id)}))
        return send({"result": client}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_client.route('/client', methods=['POST'])
@tokenReq 
def insertClient():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'nipcnif': request_data['nipcnif'],
        }
        db.db.client.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)



@bp_client.route('', methods=['PUT'])
@tokenReq
def updateClient():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'nipcnif': request_data['nipcnif'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.client.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_client.route('', methods=['DELETE'])
@tokenReq
def deleteClient():
    try:
        _id = request.args.get('client_id')
        cursor = db.db.client.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)