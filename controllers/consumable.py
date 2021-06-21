from flask import Blueprint, current_app, session, request, make_response
from controllers.login import tokenReq
from bson.objectid import ObjectId
from bson.json_util import dumps
import db

HTTP_SUCCESS_GET_OR_UPDATE = 200
HTTP_SUCCESS_CREATED       = 201
HTTP_SUCCESS_DELETED       = 204
HTTP_SERVER_ERROR          = 500
HTTP_NOT_FOUND             = 404
HTTP_BAD_REQUEST           = 400

bp_consumable = Blueprint('consumable', __name__, url_prefix='/consumable')

@bp_consumable.route("/all", methods=['GET'])
@tokenReq
def getAllConsumable():
    cursor = db.db.consumable.find({})
    return dumps(list(cursor))

@bp_consumable.route("/allbyconstruction", methods=['GET'])
@tokenReq
def getAllConsumableByConstruction():
    _id = request.args.get('obra_id')
    consumable = list(db.db.consumable.find({"obra_id": ObjectId(_id)}))
    return send({"result": consumable}, HTTP_SUCCESS_GET_OR_UPDATE)

@bp_consumable.route('', methods=['GET'])
@tokenReq
def getConsumable():
    try:

        _id = request.args.get('consumable_id')
        consumable = list(db.db.consumable.find({"_id": ObjectId(_id)}))
        return send({"result": consumable}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)


@bp_consumable.route('/consumable', methods=['POST'])
@tokenReq 
def insertConsumable():
    try:
        request_data = request.get_json() 
        new_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'valor': request_data['valor'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'notaFiscalURL': request_data['notaFiscalURL'],
        'obra_id': ObjectId(request_data['obra_id']),
        }
        db.db.consumable.insert(new_store)
        return send({"result": new_store}, HTTP_SUCCESS_CREATED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_consumable.route('', methods=['PUT'])
@tokenReq
def updateConsumable():
    try:
        request_data = request.get_json() 
        update_store = {
        'nome': request_data['nome'],
        'tipo': request_data['tipo'],
        'valor': request_data['valor'],
        'fornecedor_id': request_data['fornecedor_id'],
        'dataCompra': request_data['dataCompra'],
        'notaFiscalURL': request_data['notaFiscalURL'],
        }
        query = { "_id": ObjectId(request_data['_id']) }
        newvalues = { "$set": update_store }
        db.db.consumable.update_one(query, newvalues)
        return send({"result": update_store}, HTTP_SUCCESS_GET_OR_UPDATE)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

@bp_consumable.route('', methods=['DELETE'])
@tokenReq
def deleteConsumable():
    try:
        _id = request.args.get('consumable_id')
        cursor = db.db.consumable.find_one_and_delete({"_id": ObjectId(_id)})
        return send({"result": _id}, HTTP_SUCCESS_DELETED)
    except Exception as e:
        output = {"error": str(e)}
        return send(output, HTTP_BAD_REQUEST)

def send(data, status_code):
    return make_response(dumps(data), status_code)