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

bp_provider = Blueprint('provider', __name__, url_prefix='/provider')

@bp_provider.route("/all", methods=['GET'])
@tokenReq
def getAllProviders():
    cursor = db.db.provider.find({})
    return dumps(list(cursor))

@bp_provider.route("/allbyconstruction", methods=['GET'])
@tokenReq
def getAllProvidersByConstruction():
    _id = request.args.get('obra_id')
    provider = list(db.db.provider.find({"obra_id": ObjectId(_id)}))
    return send({"result": provider}, HTTP_SUCCESS_GET_OR_UPDATE)

@bp_provider.route('', methods=['GET'])
@tokenReq
def getProvider():
    try:
        _id = request.args.get('provider_id')
        provider = list(db.db.provider.find({"_id": ObjectId(_id)}))
        return send({"result": provider}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_provider.route('/provider', methods=['POST'])
@tokenReq
def insertProvider():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'endereco': request_data['endereco'],
        'nipc': request_data['nipc'],
        'contratoURL': request_data['contratoURL'],
        'obra_id': ObjectId(request_data['obra_id']),
        }
        db.db.provider.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_provider.route('', methods=['PUT'])
@tokenReq
def updateProvider():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'telefone': request_data['telefone'],
        'endereco': request_data['endereco'],
        'nipc': request_data['nipc'],
        'contratoURL': request_data['contratoURL'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.provider.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_provider.route('', methods=['DELETE'])
@tokenReq
def deleteProvider():
    try:
        _id = request.args.get('provider_id')
        cursor = db.db.provider.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


def send(data, status_code):
    return make_response(dumps(data), status_code)